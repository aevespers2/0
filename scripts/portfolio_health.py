#!/usr/bin/env python3
"""Portfolio-wide GitHub health scanner with fail-closed exact-state semantics."""
from __future__ import annotations

import base64
import json
import os
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
TOKEN = os.getenv("PORTFOLIO_TOKEN") or os.getenv("GITHUB_TOKEN", "")
BAD_RUN_CONCLUSIONS = {
    "failure",
    "cancelled",
    "timed_out",
    "action_required",
    "startup_failure",
    "stale",
    "skipped",
}
SUCCESSFUL_CHECK_CONCLUSIONS = {"success"}


@dataclass(frozen=True)
class Finding:
    severity: str
    repo: str
    kind: str
    summary: str
    url: str = ""


def request(path: str) -> Any:
    req = urllib.request.Request(API + path)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def paginated(path: str, *, requester: Callable[[str], Any] = request) -> list[Any]:
    """Retrieve a list endpoint with a deterministic 100-item page bound."""
    items: list[Any] = []
    separator = "&" if "?" in path else "?"
    for page in range(1, 101):
        payload = requester(f"{path}{separator}per_page=100&page={page}")
        if not isinstance(payload, list):
            raise ValueError(f"paginated endpoint did not return a list: {path}")
        items.extend(payload)
        if len(payload) < 100:
            return items
    raise RuntimeError(f"pagination exceeded 10,000 records: {path}")


def get_text(path: str, *, requester: Callable[[str], Any] = request) -> str | None:
    try:
        payload = requester(path)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    if not isinstance(payload, dict) or not isinstance(payload.get("content"), str):
        raise ValueError(f"content endpoint returned an invalid payload: {path}")
    return base64.b64decode(payload["content"], validate=True).decode("utf-8")


def latest_workflow_states(runs: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep only the newest run for each workflow/head/event state key."""
    newest: dict[tuple[Any, Any, Any], dict[str, Any]] = {}
    ordered = sorted(
        runs,
        key=lambda run: (run.get("created_at", ""), run.get("id", 0)),
        reverse=True,
    )
    for run in ordered:
        key = (run.get("workflow_id") or run.get("name"), run.get("head_sha"), run.get("event"))
        newest.setdefault(key, run)
    return list(newest.values())


def latest_check_states(checks: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    newest: dict[tuple[Any, Any], dict[str, Any]] = {}
    ordered = sorted(
        checks,
        key=lambda check: (check.get("started_at", ""), check.get("id", 0)),
        reverse=True,
    )
    for check in ordered:
        app = check.get("app") or {}
        key = (app.get("slug") or app.get("id"), check.get("name"))
        newest.setdefault(key, check)
    return list(newest.values())


def exact_head_check_problem(checks: Iterable[dict[str, Any]]) -> tuple[str, str] | None:
    """Return a fail-closed problem for missing, pending, failed, or skipped checks."""
    latest = latest_check_states(checks)
    if not latest:
        return ("missing", "no check run is attached to the exact head")
    pending = [check for check in latest if check.get("status") != "completed"]
    if pending:
        names = sorted(str(check.get("name", "unnamed")) for check in pending)
        return ("pending", f"incomplete exact-head checks: {names}")
    unsuccessful = [
        check
        for check in latest
        if check.get("conclusion") not in SUCCESSFUL_CHECK_CONCLUSIONS
    ]
    if unsuccessful:
        states = sorted(
            f"{check.get('name', 'unnamed')}={check.get('conclusion')}"
            for check in unsuccessful
        )
        return ("failed", f"non-success exact-head checks: {states}")
    return None


def resolve_mergeable(
    full_name: str,
    pr_number: int,
    *,
    requester: Callable[[str], Any] = request,
    sleeper: Callable[[float], None] = time.sleep,
) -> bool | None:
    """Use the authoritative per-PR endpoint and bounded retries for UNKNOWN."""
    for attempt in range(5):
        detail = requester(f"/repos/{full_name}/pulls/{pr_number}")
        value = detail.get("mergeable") if isinstance(detail, dict) else None
        if isinstance(value, bool):
            return value
        if attempt < 4:
            sleeper(2.0)
    return None


def scan_repo(repo: dict[str, Any]) -> list[Finding]:
    full = repo["full_name"]
    default = repo.get("default_branch") or "main"
    findings: list[Finding] = []

    runs_payload = request(f"/repos/{full}/actions/runs?per_page=100")
    runs = runs_payload.get("workflow_runs", []) if isinstance(runs_payload, dict) else []
    if not isinstance(runs, list):
        raise ValueError("workflow-runs response is malformed")
    latest_runs = latest_workflow_states(runs)
    failed = [
        run
        for run in latest_runs
        if run.get("status") == "completed" and run.get("conclusion") in BAD_RUN_CONCLUSIONS
    ]
    for run in failed:
        findings.append(
            Finding(
                "high",
                full,
                "failed_ci",
                f"latest applicable run failed: {run.get('name')} on {str(run.get('head_sha', 'unknown'))[:12]} ({run.get('conclusion')})",
                run.get("html_url", ""),
            )
        )

    branch = request(f"/repos/{full}/branches/{urllib.parse.quote(default, safe='')}")
    default_sha = branch["commit"]["sha"]
    default_checks_payload = request(f"/repos/{full}/commits/{default_sha}/check-runs?per_page=100")
    default_checks = default_checks_payload.get("check_runs", [])
    default_problem = exact_head_check_problem(default_checks)
    if default_problem:
        state, summary = default_problem
        findings.append(
            Finding(
                "high" if state == "failed" else "medium",
                full,
                f"default_head_ci_{state}",
                f"{default}@{default_sha[:12]}: {summary}",
                f"https://github.com/{full}/commit/{default_sha}",
            )
        )

    prs = paginated(f"/repos/{full}/pulls?state=open")
    for pr in prs:
        number = int(pr["number"])
        sha = pr["head"]["sha"]
        checks_payload = request(f"/repos/{full}/commits/{sha}/check-runs?per_page=100")
        checks = checks_payload.get("check_runs", [])
        problem = exact_head_check_problem(checks)
        if problem:
            state, summary = problem
            findings.append(
                Finding(
                    "high" if state == "failed" else "medium",
                    full,
                    f"pr_exact_head_ci_{state}",
                    f"PR #{number} at {sha[:12]}: {summary}",
                    pr["html_url"],
                )
            )

        mergeable = resolve_mergeable(full, number)
        if mergeable is False:
            findings.append(
                Finding("high", full, "non_mergeable_pr", f"PR #{number} has merge conflicts", pr["html_url"])
            )
        elif mergeable is None:
            findings.append(
                Finding("medium", full, "unknown_mergeability", f"PR #{number} mergeability remained unknown after bounded retries", pr["html_url"])
            )

        if not pr.get("draft", False) and problem:
            findings.append(
                Finding("medium", full, "unverified_pr_not_draft", f"PR #{number} is not draft while exact-head validation is unresolved", pr["html_url"])
            )

    issues = paginated(f"/repos/{full}/issues?state=open")
    real_issues = [item for item in issues if "pull_request" not in item]
    severe = [
        item
        for item in real_issues
        if any(
            label.get("name", "").lower() in {"critical", "security", "incident", "p0", "blocker"}
            for label in item.get("labels", [])
        )
    ]
    for issue in severe:
        findings.append(
            Finding("high", full, "blocking_issue", f"blocking issue #{issue['number']}: {issue['title']}", issue["html_url"])
        )

    release = get_text(
        f"/repos/{full}/contents/release.md?ref={urllib.parse.quote(default, safe='')}"
    )
    if release:
        candidate_lines = [
            line
            for line in release.splitlines()
            if "candidate head" in line.lower() or "exact-head" in line.lower()
        ]
        candidate_shas = {
            sha
            for line in candidate_lines
            for sha in re.findall(r"\b[0-9a-f]{40}\b", line)
        }
        if candidate_shas and default_sha not in candidate_shas:
            findings.append(
                Finding(
                    "medium",
                    full,
                    "stale_provenance",
                    f"release.md exact-head evidence does not name current {default} head {default_sha[:12]}",
                    f"https://github.com/{full}/blob/{default}/release.md",
                )
            )
        if "no workflow" in release.lower() and runs:
            findings.append(
                Finding(
                    "medium",
                    full,
                    "metadata_contradiction",
                    "release.md says no workflow exists, but Actions runs are present",
                    f"https://github.com/{full}/blob/{default}/release.md",
                )
            )

    return findings


def generated_at() -> str:
    epoch = os.getenv("SOURCE_DATE_EPOCH")
    if epoch is not None:
        return datetime.fromtimestamp(int(epoch), timezone.utc).isoformat()
    return datetime.now(timezone.utc).isoformat()


def owned_repositories() -> list[dict[str, Any]]:
    if TOKEN:
        return paginated("/user/repos?affiliation=owner&visibility=all&sort=full_name")
    return paginated(f"/users/{OWNER}/repos?type=owner&sort=full_name")


def main() -> int:
    repos = owned_repositories()
    findings: list[Finding] = []
    errors: list[str] = []
    for repo in repos:
        if repo.get("archived"):
            continue
        try:
            findings.extend(scan_repo(repo))
        except Exception as exc:  # fail closed but continue portfolio scan
            errors.append(f"{repo.get('full_name', 'unknown')}: {type(exc).__name__}: {exc}")

    findings.sort(
        key=lambda item: (
            {"high": 0, "medium": 1, "low": 2}.get(item.severity, 9),
            item.repo,
            item.kind,
            item.summary,
        )
    )
    report = {
        "schema_version": "2.0.0",
        "generated_at": generated_at(),
        "owner": OWNER,
        "finding_count": len(findings),
        "errors": errors,
        "findings": [asdict(item) for item in findings],
    }
    with open("portfolio-health.json", "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")

    lines = [
        "# Portfolio Health",
        "",
        f"Findings: **{len(findings)}**",
        f"Scan errors: **{len(errors)}**",
        "",
    ]
    if findings:
        for finding in findings:
            link = f" ([source]({finding.url}))" if finding.url else ""
            lines.append(
                f"- **{finding.severity.upper()}** `{finding.repo}` / `{finding.kind}` — {finding.summary}{link}"
            )
    else:
        lines.append("No significant repository-health findings.")
    if errors:
        lines.extend(["", "## Scan errors", *[f"- {error}" for error in errors]])
    markdown = "\n".join(lines) + "\n"
    with open("portfolio-health.md", "w", encoding="utf-8") as handle:
        handle.write(markdown)
    summary = os.getenv("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(markdown)
    print(markdown)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
