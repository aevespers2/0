#!/usr/bin/env python3
"""Fail-closed, deduplicated health scan for the aevespers2 GitHub portfolio."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import posixpath
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Iterable

API = "https://api.github.com"
OWNER = os.getenv("PORTFOLIO_OWNER", "aevespers2")
PORTFOLIO_TOKEN = os.getenv("PORTFOLIO_TOKEN", "")
TOKEN = PORTFOLIO_TOKEN or os.getenv("GITHUB_TOKEN", "")
SUCCESS = {"success"}
BAD_RUNS = {"failure", "cancelled", "timed_out", "action_required", "startup_failure", "stale", "skipped"}
DOCS = ("README.md", "taskchain.md", "punchlist.md", "release.md", "changelog.md")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
USES = re.compile(r"(?m)^\s*-?\s*uses:\s*([^\s#]+)")
WRITE_SCOPES = {"actions", "checks", "contents", "deployments", "id-token", "packages", "pages", "security-events"}


@dataclass(frozen=True)
class Finding:
    severity: str
    repo: str
    kind: str
    summary: str
    url: str = ""
    identity: str = ""


def api(path: str) -> Any:
    request = urllib.request.Request(API + path)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if TOKEN:
        request.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def pages(path: str, key: str | None = None, requester: Callable[[str], Any] = api) -> list[Any]:
    output: list[Any] = []
    separator = "&" if "?" in path else "?"
    for page in range(1, 101):
        payload = requester(f"{path}{separator}per_page=100&page={page}")
        values = payload.get(key) if key and isinstance(payload, dict) else payload
        if not isinstance(values, list):
            raise ValueError(f"paginated endpoint did not return a list for {path}")
        output.extend(values)
        if len(values) < 100:
            return output
    raise RuntimeError(f"pagination exceeded 10,000 records for {path}")


def content(path: str, requester: Callable[[str], Any] = api) -> Any | None:
    try:
        return requester(path)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def text(path: str, requester: Callable[[str], Any] = api) -> str | None:
    payload = content(path, requester)
    if payload is None:
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("content"), str):
        raise ValueError(f"invalid content response for {path}")
    return base64.b64decode(payload["content"], validate=True).decode("utf-8")


def newest(items: Iterable[dict[str, Any]], key_fn: Callable[[dict[str, Any]], tuple[Any, ...]], time_key: str) -> list[dict[str, Any]]:
    result: dict[tuple[Any, ...], dict[str, Any]] = {}
    for item in sorted(items, key=lambda row: (str(row.get(time_key) or ""), int(row.get("id") or 0)), reverse=True):
        result.setdefault(key_fn(item), item)
    return list(result.values())


def latest_runs(runs: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return newest(runs, lambda run: (run.get("workflow_id") or run.get("name"), run.get("head_sha"), run.get("event")), "created_at")


def exact_check_problem(checks: Iterable[dict[str, Any]]) -> tuple[str, str] | None:
    latest = newest(checks, lambda check: (((check.get("app") or {}).get("slug") or (check.get("app") or {}).get("id")), check.get("name")), "started_at")
    if not latest:
        return "missing", "no check run is attached to the exact head"
    pending = sorted(str(row.get("name") or "unnamed") for row in latest if row.get("status") != "completed")
    if pending:
        return "pending", f"incomplete exact-head checks: {pending}"
    failed = sorted(f"{row.get('name') or 'unnamed'}={row.get('conclusion')}" for row in latest if row.get("conclusion") not in SUCCESS)
    return ("failed", f"non-success exact-head checks: {failed}") if failed else None


def mergeable(repo: str, number: int, requester: Callable[[str], Any] = api, sleeper: Callable[[float], None] = time.sleep) -> bool | None:
    for attempt in range(5):
        payload = requester(f"/repos/{repo}/pulls/{number}")
        value = payload.get("mergeable") if isinstance(payload, dict) else None
        if isinstance(value, bool):
            return value
        if attempt < 4:
            sleeper(2)
    return None


def permission_problems(source: str) -> list[tuple[str, str]]:
    problems: list[tuple[str, str]] = []
    if re.search(r"(?m)^permissions:\s*write-all\s*$", source):
        problems.append(("unsafe_workflow_permissions", "top-level permissions use write-all"))
    if not re.search(r"(?m)^permissions:\s*(?:$|\{\}\s*$|read-all\s*$|write-all\s*$)", source):
        problems.append(("missing_workflow_permissions", "no explicit top-level permissions block"))
    writes = {match.group(1) for match in re.finditer(r"(?m)^\s+([a-z-]+):\s*write\s*$", source)}
    if re.search(r"(?m)^\s*pull_request_target\s*:", source) and writes:
        problems.append(("unsafe_pull_request_target_permissions", "pull_request_target has write scopes: " + ", ".join(sorted(writes))))
    if re.search(r"(?m)^\s{2}(push|schedule)\s*:", source) and writes & WRITE_SCOPES:
        problems.append(("privileged_automatic_workflow", "automatic trigger has privileged writes: " + ", ".join(sorted(writes & WRITE_SCOPES))))
    return problems


def mutable_actions(source: str) -> list[str]:
    values = []
    for match in USES.finditer(source):
        value = match.group(1).strip("\"'")
        if not value.startswith("./") and "@" in value and not SHA40.fullmatch(value.rsplit("@", 1)[1]):
            values.append(value)
    return sorted(set(values))


def local_links(source: str, source_path: str) -> list[str]:
    targets: set[str] = set()
    for raw in LINK.findall(source):
        target = raw.strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:", "tel:")):
            continue
        target = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source_path), target))
        if resolved and resolved != ".." and not resolved.startswith("../"):
            targets.add(resolved)
    return sorted(targets)


def scan_workflows(
    repo: str,
    ref_name: str,
    label: str | None = None,
    baseline_sources: dict[str, str] | None = None,
    source_repo: str | None = None,
) -> tuple[list[Finding], dict[str, str]]:
    """Scan workflow files at one exact source head, including forked PR heads."""
    findings: list[Finding] = []
    sources: dict[str, str] = {}
    label = label or ref_name
    source_repo = source_repo or repo
    ref = urllib.parse.quote(ref_name, safe="")
    listing = content(f"/repos/{source_repo}/contents/.github/workflows?ref={ref}")
    if listing is None:
        return findings, sources
    if not isinstance(listing, list):
        raise ValueError("workflow directory is malformed")
    for item in listing:
        path = item.get("path") if isinstance(item, dict) else None
        if not isinstance(path, str) or not path.endswith((".yml", ".yaml")):
            continue
        source = text(f"/repos/{source_repo}/contents/{urllib.parse.quote(path, safe='/')}?ref={ref}")
        if source is None:
            continue
        sources[path] = source
        if baseline_sources is not None and baseline_sources.get(path) == source:
            continue
        url = f"https://github.com/{source_repo}/blob/{ref_name}/{path}"
        prefix = f"{label}: {path}"
        source_identity = f"{source_repo}|{ref_name}|{path}"
        for kind, summary in permission_problems(source):
            findings.append(Finding("high" if kind != "missing_workflow_permissions" else "medium", repo, kind, f"{prefix}: {summary}", url, f"{repo}|workflow-source|{source_identity}|{kind}"))
        mutable = mutable_actions(source)
        if mutable:
            findings.append(Finding("medium", repo, "mutable_action_reference", f"{prefix}: {', '.join(mutable)}", url, f"{repo}|workflow-source|{source_identity}|mutable|{'|'.join(mutable)}"))
    return findings, sources


def scan_links(repo: str, branch: str) -> list[Finding]:
    findings: list[Finding] = []
    ref = urllib.parse.quote(branch, safe="")
    exists: dict[str, bool] = {}
    for source_path in DOCS:
        source = text(f"/repos/{repo}/contents/{source_path}?ref={ref}")
        if source is None:
            continue
        for target in local_links(source, source_path):
            if target not in exists:
                exists[target] = content(f"/repos/{repo}/contents/{urllib.parse.quote(target, safe='/')}?ref={ref}") is not None
            if not exists[target]:
                findings.append(Finding("medium", repo, "broken_documentation_link", f"{source_path} links to missing {target}", f"https://github.com/{repo}/blob/{branch}/{source_path}", f"{repo}|link|{source_path}|{target}"))
    return findings


def scan_artifacts(
    repo: str,
    heads: set[str],
    runs: Iterable[dict[str, Any]],
    workflow_sources_by_head: dict[str, dict[str, str]],
    requester: Callable[[str], Any] = api,
) -> list[Finding]:
    """Check declarations from the workflow source at each run's exact head."""
    findings: list[Finding] = []
    paths: dict[int, str] = {}
    for run in runs:
        head_sha = str(run.get("head_sha") or "")
        if head_sha not in heads or run.get("status") != "completed" or run.get("conclusion") != "success":
            continue
        workflow_id, run_id = run.get("workflow_id"), run.get("id")
        if not isinstance(workflow_id, int) or not isinstance(run_id, int):
            continue
        if workflow_id not in paths:
            meta = requester(f"/repos/{repo}/actions/workflows/{workflow_id}")
            paths[workflow_id] = str(meta.get("path") or "") if isinstance(meta, dict) else ""
        source = workflow_sources_by_head.get(head_sha, {}).get(paths[workflow_id], "")
        if "actions/upload-artifact@" not in source:
            continue
        artifacts = requester(f"/repos/{repo}/actions/runs/{run_id}/artifacts?per_page=1")
        if isinstance(artifacts, dict) and artifacts.get("total_count") == 0:
            findings.append(Finding("high", repo, "missing_expected_artifact", f"successful run {run.get('name')} ({run_id}) retained no declared artifact", str(run.get("html_url") or ""), f"{repo}|run|{run_id}|missing-artifact"))
    return findings


def scan_repo(repository: dict[str, Any]) -> list[Finding]:
    repo = repository["full_name"]
    branch = repository.get("default_branch") or "main"
    branch_data = api(f"/repos/{repo}/branches/{urllib.parse.quote(branch, safe='')}")
    default_sha = branch_data["commit"]["sha"]
    prs = pages(f"/repos/{repo}/pulls?state=open")
    heads = {default_sha, *(str(pr["head"]["sha"]) for pr in prs if isinstance(pr.get("head"), dict) and pr["head"].get("sha"))}
    findings: list[Finding] = []

    runs = latest_runs(pages(f"/repos/{repo}/actions/runs", "workflow_runs"))
    for run in runs:
        if run.get("head_sha") in heads and run.get("status") == "completed" and run.get("conclusion") in BAD_RUNS:
            findings.append(Finding("high", repo, "failed_ci", f"{run.get('name')} on {str(run.get('head_sha'))[:12]}: {run.get('conclusion')}", str(run.get("html_url") or ""), f"{repo}|workflow|{run.get('workflow_id')}|{run.get('head_sha')}|{run.get('event')}|{run.get('id')}|{run.get('conclusion')}"))

    checks = api(f"/repos/{repo}/commits/{default_sha}/check-runs?per_page=100").get("check_runs", [])
    problem = exact_check_problem(checks)
    if problem:
        state, summary = problem
        findings.append(Finding("high" if state == "failed" else "medium", repo, f"default_head_ci_{state}", f"{branch}@{default_sha[:12]}: {summary}", f"https://github.com/{repo}/commit/{default_sha}", f"{repo}|default|{default_sha}|ci|{state}"))

    for pr in prs:
        number, sha = int(pr["number"]), str(pr["head"]["sha"])
        problem = exact_check_problem(api(f"/repos/{repo}/commits/{sha}/check-runs?per_page=100").get("check_runs", []))
        if problem:
            state, summary = problem
            findings.append(Finding("high" if state == "failed" else "medium", repo, f"pr_exact_head_ci_{state}", f"PR #{number} at {sha[:12]}: {summary}", pr["html_url"], f"{repo}|pr|{number}|{sha}|ci|{state}"))
        state = mergeable(repo, number)
        if state is False:
            findings.append(Finding("high", repo, "non_mergeable_pr", f"PR #{number} has merge conflicts", pr["html_url"], f"{repo}|pr|{number}|{sha}|conflict"))
        elif state is None:
            findings.append(Finding("medium", repo, "unknown_mergeability", f"PR #{number} mergeability remained unknown", pr["html_url"], f"{repo}|pr|{number}|{sha}|unknown"))
        if problem and not pr.get("draft", False):
            findings.append(Finding("medium", repo, "unverified_pr_not_draft", f"PR #{number} is review-ready with unresolved exact-head validation", pr["html_url"], f"{repo}|pr|{number}|{sha}|not-draft"))

    for issue in (item for item in pages(f"/repos/{repo}/issues?state=open") if "pull_request" not in item):
        labels = {label.get("name", "").lower() for label in issue.get("labels", [])}
        if labels & {"critical", "security", "incident", "p0", "blocker"}:
            findings.append(Finding("high", repo, "blocking_issue", f"issue #{issue['number']}: {issue['title']}", issue["html_url"], f"{repo}|issue|{issue['number']}|blocking"))

    workflow_sources_by_head: dict[str, dict[str, str]] = {}
    workflow_findings, default_sources = scan_workflows(repo, default_sha, f"{branch}@{default_sha[:12]}")
    workflow_sources_by_head[default_sha] = default_sources
    findings.extend(workflow_findings)

    scanned_pr_heads: set[tuple[str, str]] = set()
    for pr in prs:
        number, sha = int(pr["number"]), str(pr["head"]["sha"])
        head_repo = (pr.get("head") or {}).get("repo") or {}
        source_repo = head_repo.get("full_name") if isinstance(head_repo, dict) else None
        if not isinstance(source_repo, str) or not source_repo:
            findings.append(Finding("high", repo, "unavailable_pr_head_source", f"PR #{number} at {sha[:12]} has no readable source repository identity", pr["html_url"], f"{repo}|pr|{number}|{sha}|workflow-source-unavailable"))
            continue
        source_key = (source_repo, sha)
        if source_key in scanned_pr_heads:
            continue
        scanned_pr_heads.add(source_key)
        pr_findings, pr_sources = scan_workflows(
            repo,
            sha,
            f"PR #{number}@{sha[:12]}",
            baseline_sources=default_sources,
            source_repo=source_repo,
        )
        workflow_sources_by_head[sha] = pr_sources
        findings.extend(pr_findings)

    findings.extend(scan_artifacts(repo, heads, runs, workflow_sources_by_head))
    findings.extend(scan_links(repo, branch))

    release = text(f"/repos/{repo}/contents/release.md?ref={urllib.parse.quote(branch, safe='')}")
    if release:
        relevant = [line for line in release.splitlines() if "candidate head" in line.lower() or "exact-head" in line.lower()]
        named = {sha for line in relevant for sha in re.findall(r"\b[0-9a-f]{40}\b", line)}
        if named and default_sha not in named:
            findings.append(Finding("medium", repo, "stale_provenance", f"release.md does not name current {branch} head {default_sha[:12]}", f"https://github.com/{repo}/blob/{branch}/release.md", f"{repo}|release|{default_sha}|stale"))
        if "no workflow" in release.lower() and runs:
            findings.append(Finding("medium", repo, "metadata_contradiction", "release.md says no workflow exists although Actions runs exist", f"https://github.com/{repo}/blob/{branch}/release.md", f"{repo}|release|workflow-contradiction"))
    return findings


def fingerprint(findings: Iterable[Finding], errors: Iterable[str]) -> str:
    body = json.dumps({"findings": [asdict(item) for item in findings], "errors": sorted(errors)}, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(body).hexdigest()


def render(report: dict[str, Any]) -> str:
    lines = [f"<!-- portfolio_fingerprint={report['portfolio_fingerprint']} -->", "# Portfolio Health", "", f"Repositories inspected: **{report.get('repository_count', 0)}**", f"Findings: **{report['finding_count']}**", f"Scan errors: **{len(report['errors'])}**", ""]
    if report["errors"]:
        lines += ["## Scan errors", "", *(f"- {value}" for value in report["errors"]), ""]
    if report["findings"]:
        lines += ["## Current findings", ""]
        for item in report["findings"]:
            link = f" — {item['url']}" if item["url"] else ""
            lines.append(f"- **{item['severity'].upper()}** `{item['repo']}` `{item['kind']}`: {item['summary']}{link}")
        lines.append("")
    else:
        lines += ["No current findings were detected.", ""]
    lines += ["Only the latest semantic fingerprint is current; older runs and comments are historical evidence.", "Successful validation grants no merge, release, publication, deployment, credential, destructive-history, or infrastructure authority.", ""]
    return "\n".join(lines)


def owned() -> list[dict[str, Any]]:
    if PORTFOLIO_TOKEN:
        return pages("/user/repos?affiliation=owner&visibility=all&sort=full_name")
    return pages(f"/users/{OWNER}/repos?type=owner&sort=full_name")


# Compatibility names retained for the prior reviewed scanner test surface.
latest_workflow_states = latest_runs
exact_head_check_problem = exact_check_problem
resolve_mergeable = mergeable
paginated = lambda path, requester=api: pages(path, requester=requester)
paginated_key = lambda path, key, requester=api: pages(path, key, requester)
workflow_permission_problems = permission_problems
mutable_action_references = mutable_actions
markdown_targets = local_links
semantic_fingerprint = fingerprint
render_markdown = render


def main() -> int:
    repositories = [repo for repo in owned() if not repo.get("archived")]
    findings: list[Finding] = []
    errors: list[str] = []
    for repository in repositories:
        try:
            findings.extend(scan_repo(repository))
        except Exception as exc:
            errors.append(f"{repository.get('full_name', 'unknown')}: {type(exc).__name__}: {exc}")
    findings.sort(key=lambda item: ({"high": 0, "medium": 1, "low": 2}.get(item.severity, 9), item.repo, item.kind, item.identity, item.summary))
    report = {
        "schema_version": "3.1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owner": OWNER,
        "coverage_mode": "owner_all_visibility" if PORTFOLIO_TOKEN else "public_owner_repositories",
        "repository_count": len(repositories),
        "finding_count": len(findings),
        "portfolio_fingerprint": fingerprint(findings, errors),
        "errors": errors,
        "findings": [asdict(item) for item in findings],
    }
    with open("portfolio-health.json", "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True); handle.write("\n")
    with open("portfolio-health.md", "w", encoding="utf-8") as handle:
        handle.write(render(report))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
