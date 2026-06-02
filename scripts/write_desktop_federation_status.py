from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SAFE_REPO_ROOT = "/Users/ALISTAIRE/aevespers2-0"


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


def build_status(
    repo: Path,
    safe_root: str,
) -> dict[str, Any]:
    root = Path(git(["rev-parse", "--show-toplevel"], repo))
    cwd = str(root)
    blocked = cwd != safe_root
    next_action = "Report status only; switch to safe checkout and refresh for write authority."
    if blocked:
        blocker = "wrong_checkout"
    else:
        blocker = ""
        next_action = "Collect safari_cloud and mobile status packets through FederationInbox."
    return {
        "schema": "codex_federation_message.v1",
        "agent": "desktop_app",
        "type": "status",
        "workstream": "Autonomous VNext",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "cwd": cwd,
        "branch": git(["branch", "--show-current"], repo),
        "commit": git(["rev-parse", "HEAD"], repo),
        "status_short": git(["status", "--branch", "--short"], root).splitlines(),
        "remote": git(["remote", "-v"], root),
        "blocker": "wrong_checkout" if blocked else "",
        "next_action": next_action,
        "safe_repo_root": safe_root,
    }


def write_status(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write Desktop CLI status into FederationInbox/desktop with safe-check contract."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--safe-root", default=SAFE_REPO_ROOT)
    parser.add_argument("--output", type=Path, default=Path("FederationInbox/desktop/status.json"))
    parser.add_argument("--print", action="store_true", dest="print_payload")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_status(args.repo, args.safe_root)
    write_status(payload, args.output)
    if args.print_payload:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
