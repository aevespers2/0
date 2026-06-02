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


def build_local_status(repo: Path) -> dict[str, Any]:
    root = Path(git(["rev-parse", "--show-toplevel"], repo))
    return {
        "schema": "codex_federation_message.v1",
        "agent": "local_cli",
        "type": "status",
        "workstream": "Autonomous vNext",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "cwd": str(root),
        "branch": git(["branch", "--show-current"], root),
        "commit": git(["rev-parse", "HEAD"], root),
        "status_short": git(["status", "--branch", "--short"], root).splitlines(),
        "remote": git(["remote", "-v"], root),
        "blocker": "",
        "next_action": "Collect safari_cloud and desktop_app status packets through FederationInbox.",
    }


def write_status(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write Local CLI status into FederationInbox/local.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("FederationInbox/local/status.json"))
    parser.add_argument("--print", action="store_true", dest="print_payload")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_local_status(args.repo)
    write_status(payload, args.output)
    if args.print_payload:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
