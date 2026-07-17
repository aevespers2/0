#!/usr/bin/env python3
"""Portfolio-wide GitHub health scanner with deterministic JSON/Markdown output."""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any

API = "https://api.github.com"
OWNER = os.getenv("PORTFOLIO_OWNER", "aevespers2")
TOKEN = os.getenv("PORTFOLIO_TOKEN") or os.getenv("GITHUB_TOKEN", "")
STALE_DAYS = int(os.getenv("STALE_DAYS", "14"))

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


def get_text(path: str) -> str | None:
    try:
        payload = request(path)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    import base64
    return base64.b64decode(payload["content"]).decode("utf-8")


def scan_repo(repo: dict[str, Any]) -> list[Finding]:
    name = repo["name"]
    full = repo["full_name"]
    default = repo.get("default_branch", "main")
    findings: list[Finding] = []

    runs = request(f"/repos/{full}/actions/runs?per_page=20").get("workflow_runs", [])
    failed = [r for r in runs if r.get("conclusion") in {"failure", "cancelled", "timed_out", "action_required", "startup_failure"}]
    if failed:
        latest = failed[0]
        findings.append(Finding("high", full, "failed_ci", f"{len(failed)} recent unsuccessful workflow run(s); latest: {latest.get('name')}", latest.get("html_url", "")))

    prs = request(f"/repos/{full}/pulls?state=open&per_page=100")
    for pr in prs:
        sha = pr["head"]["sha"]
        statuses = request(f"/repos/{full}/commits/{sha}/check-runs?per_page=100").get("check_runs", [])
        if not statuses:
            findings.append(Finding("medium", full, "missing_exact_head_ci", f"PR #{pr['number']} has no check run attached to head {sha[:12]}", pr["html_url"]))
        mergeable = pr.get("mergeable")
        if mergeable is False:
            findings.append(Finding("high", full, "non_mergeable_pr", f"PR #{pr['number']} is non-mergeable", pr["html_url"]))

    issues = request(f"/repos/{full}/issues?state=open&per_page=100")
    real_issues = [i for i in issues if "pull_request" not in i]
    severe = [i for i in real_issues if any((label.get("name", "").lower() in {"critical", "security", "incident", "p0", "blocker"}) for label in i.get("labels", []))]
    if severe:
        findings.append(Finding("high", full, "blocking_issue", f"{len(severe)} open security/incident/P0 issue(s)", severe[0]["html_url"]))

    release = get_text(f"/repos/{full}/contents/release.md?ref={urllib.parse.quote(default)}")
    if release:
        branch = request(f"/repos/{full}/branches/{urllib.parse.quote(default)}")
        head = branch["commit"]["sha"]
        sha_mentions = set(re.findall(r"\b[0-9a-f]{40}\b", release))
        candidate_lines = [line for line in release.splitlines() if "candidate head" in line.lower() or "exact-head" in line.lower()]
        candidate_shas = {sha for line in candidate_lines for sha in re.findall(r"\b[0-9a-f]{40}\b", line)}
        if candidate_shas and head not in candidate_shas:
            findings.append(Finding("medium", full, "stale_provenance", f"release.md candidate/exact-head evidence does not name current {default} head {head[:12]}", f"https://github.com/{full}/blob/{default}/release.md"))
        if "no workflow" in release.lower() and runs:
            findings.append(Finding("medium", full, "metadata_contradiction", "release.md says no workflow exists, but Actions runs are present", f"https://github.com/{full}/blob/{default}/release.md"))

    return findings


def main() -> int:
    repos = request(f"/users/{OWNER}/repos?per_page=100&type=owner&sort=full_name")
    findings: list[Finding] = []
    errors: list[str] = []
    for repo in repos:
        if repo.get("archived"):
            continue
        try:
            findings.extend(scan_repo(repo))
        except Exception as exc:  # fail closed but continue portfolio scan
            errors.append(f"{repo['full_name']}: {type(exc).__name__}: {exc}")

    findings.sort(key=lambda f: ({"high": 0, "medium": 1, "low": 2}.get(f.severity, 9), f.repo, f.kind))
    report = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owner": OWNER,
        "finding_count": len(findings),
        "errors": errors,
        "findings": [asdict(f) for f in findings],
    }
    with open("portfolio-health.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    lines = ["# Portfolio Health", "", f"Findings: **{len(findings)}**", f"Scan errors: **{len(errors)}**", ""]
    if findings:
        for f in findings:
            link = f" ([source]({f.url}))" if f.url else ""
            lines.append(f"- **{f.severity.upper()}** `{f.repo}` / `{f.kind}` — {f.summary}{link}")
    else:
        lines.append("No significant repository-health findings.")
    if errors:
        lines.extend(["", "## Scan errors", *[f"- {e}" for e in errors]])
    markdown = "\n".join(lines) + "\n"
    with open("portfolio-health.md", "w", encoding="utf-8") as fh:
        fh.write(markdown)
    summary = os.getenv("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(markdown)
    print(markdown)
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
