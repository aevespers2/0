#!/usr/bin/env python3
"""Gods channel Jira synchronization and Prometheus exposition."""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def escape_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


def prometheus(report: dict[str, Any], output: Path) -> None:
    findings = report.get("findings", [])
    if not isinstance(findings, list):
        raise ValueError("findings must be an array")
    counts = Counter(str(item.get("severity", "unknown")).lower() for item in findings if isinstance(item, dict))
    repos = Counter(str(item.get("repo", "unknown")) for item in findings if isinstance(item, dict))
    errors = report.get("errors", [])
    lines = [
        "# HELP qso_portfolio_findings Repository-health findings by severity.",
        "# TYPE qso_portfolio_findings gauge",
    ]
    for severity in sorted(set(counts) | set(SEVERITY_ORDER)):
        lines.append(f'qso_portfolio_findings{{channel="Gods",severity="{escape_label(severity)}"}} {counts[severity]}')
    lines.extend([
        "# HELP qso_portfolio_repository_findings Findings grouped by repository.",
        "# TYPE qso_portfolio_repository_findings gauge",
    ])
    for repo, count in sorted(repos.items()):
        lines.append(f'qso_portfolio_repository_findings{{channel="Gods",repository="{escape_label(repo)}"}} {count}')
    lines.extend([
        "# HELP qso_portfolio_scan_errors Portfolio scan errors.",
        "# TYPE qso_portfolio_scan_errors gauge",
        f'qso_portfolio_scan_errors{{channel="Gods"}} {len(errors) if isinstance(errors, list) else 1}',
        "# HELP qso_portfolio_release_ready Computed release-readiness gate.",
        "# TYPE qso_portfolio_release_ready gauge",
    ])
    high = sum(count for severity, count in counts.items() if SEVERITY_ORDER.get(severity, 3) >= 3)
    ready = int(high == 0 and not errors)
    lines.append(f'qso_portfolio_release_ready{{channel="Gods"}} {ready}')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def adf(text: str) -> dict[str, Any]:
    return {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": text[:30000]}]}],
    }


def request_json(url: str, method: str, body: dict[str, Any] | None = None) -> Any:
    email = os.environ["JIRA_EMAIL"]
    token = os.environ["JIRA_API_TOKEN"]
    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Basic {auth}")
    req.add_header("Accept", "application/json")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = response.read()
        return json.loads(payload) if payload else None


def jira_sync(report: dict[str, Any], dry_run: bool) -> list[dict[str, Any]]:
    base = os.environ["JIRA_BASE_URL"].rstrip("/")
    project = os.environ["JIRA_PROJECT_KEY"]
    issue_type = os.getenv("JIRA_ISSUE_TYPE", "Task")
    findings = [item for item in report.get("findings", []) if isinstance(item, dict)]
    actions: list[dict[str, Any]] = []
    for finding in findings:
        severity = str(finding.get("severity", "medium")).lower()
        if SEVERITY_ORDER.get(severity, 2) < 2:
            continue
        repo = str(finding.get("repo", "unknown"))
        kind = str(finding.get("kind", "repository-health"))
        summary = f"[{repo}] {kind}: {finding.get('summary', 'attention required')}"[:255]
        marker = re.sub(r"[^a-z0-9-]+", "-", f"gods-{repo}-{kind}".lower()).strip("-")[:200]
        jql = urllib.parse.quote(f'project = "{project}" AND labels = "{marker}" AND statusCategory != Done')
        existing = [] if dry_run else request_json(f"{base}/rest/api/3/search/jql?jql={jql}&maxResults=1&fields=key", "GET").get("issues", [])
        action = {"summary": summary, "label": marker, "existing": bool(existing)}
        actions.append(action)
        if dry_run or existing:
            continue
        payload = {
            "fields": {
                "project": {"key": project},
                "issuetype": {"name": issue_type},
                "summary": summary,
                "description": adf(f"Gods channel Pre-Review Task\n\nRepository: {repo}\nKind: {kind}\nSeverity: {severity}\n\n{finding.get('summary', '')}\n\nSource: {finding.get('url', '')}"),
                "labels": ["portfolio-health", "gods", marker],
            }
        }
        request_json(f"{base}/rest/api/3/issue", "POST", payload)
    return actions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prometheus", "jira"))
    parser.add_argument("--report", type=Path, default=Path("portfolio-health.json"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/gods/portfolio.prom"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = load_json(args.report)
    if args.command == "prometheus":
        prometheus(report, args.output)
        return 0
    actions = jira_sync(report, args.dry_run)
    print(json.dumps(actions, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
