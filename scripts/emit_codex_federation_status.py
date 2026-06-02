from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def build_status(repo: Path) -> dict[str, Any]:
    root = Path(git(["rev-parse", "--show-toplevel"], repo))
    remotes: dict[str, dict[str, str]] = {}
    for line in git(["remote", "-v"], root).splitlines():
        parts = line.split()
        if len(parts) >= 3:
            remotes.setdefault(parts[0], {})[parts[2].strip("()")] = parts[1]
    return {
        "schema": "codex_federation_status.v1",
        "surface": "local_cli",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repo_root": str(root),
        "branch": git(["branch", "--show-current"], root),
        "head": git(["rev-parse", "HEAD"], root),
        "status_short": git(["status", "--branch", "--short"], root).splitlines(),
        "remotes": remotes,
        "coordination": {
            "safe_repo_hint": "/Users/ALISTAIRE/aevespers2-0",
            "workstream": "Autonomous vNext cognitive engine continuous integration",
            "known_surfaces": [
                "local_cli",
                "safari_cloud",
                "desktop_app",
                "mobile",
                "chatgpt_bridge",
            ],
            "required_checks": [
                "pytest -q",
                "python3 -m autonomous_vnext.cognitive_runtime \"ci federation coordination smoke\" --output /tmp/cognitive_runtime_report.json",
            ],
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit machine-readable Codex federation status.")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repository path to inspect.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    status = build_status(args.repo)
    indent = 2 if args.pretty else None
    print(json.dumps(status, indent=indent, sort_keys=True))


if __name__ == "__main__":
    main()
