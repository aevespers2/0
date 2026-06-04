from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from typing import Any


def run_command(command: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def parse_json_stdout(result: dict[str, Any]) -> dict[str, Any]:
    if not result["stdout"]:
        return {}
    try:
        return json.loads(result["stdout"])
    except json.JSONDecodeError:
        return {}


def command_succeeded(result: dict[str, Any]) -> bool:
    return int(result.get("returncode", 1)) == 0


def run_refresh(args: argparse.Namespace) -> dict[str, Any]:
    mirror_command = [
        "python3",
        "scripts/verify_public_mirrors.py",
        "--attempts",
        str(args.mirror_attempts),
        "--retry-delay",
        str(args.mirror_retry_delay),
        "--pretty",
    ]
    mirrors = run_command(mirror_command, args.repo)

    routine_command = ["python3", "scripts/run_federation_routine.py", "--print"]
    if args.no_desktop_contact:
        routine_command.append("--no-desktop-contact")
    routine = run_command(routine_command, args.repo)

    safari_sync = {
        "command": [],
        "returncode": 0,
        "stdout": "",
        "stderr": "Safari contact refresh disabled",
        "skipped": True,
    }
    if not args.no_safari_contact:
        safari_sync = run_command(
            [
                "python3",
                "scripts/run_safari_sync_cycle.py",
                "--watch-timeout",
                str(args.safari_watch_timeout),
                "--watch-interval",
                str(args.safari_watch_interval),
                "--print",
            ],
            args.repo,
        )

    contact_report = run_command(["python3", "scripts/write_federation_contact_report.py", "--print"], args.repo)
    dashboard = run_command(
        ["python3", "scripts/write_federation_dashboard.py", "--refresh-mirrors", "--print"],
        args.repo,
    )

    mirror_payload = parse_json_stdout(mirrors)
    contact_payload = parse_json_stdout(contact_report)
    dashboard_payload = parse_json_stdout(dashboard)
    return {
        "schema": "codex_federation_post_push_refresh.v1",
        "commands_succeeded": all(
            command_succeeded(item) for item in (mirrors, routine, safari_sync, contact_report, dashboard)
        ),
        "authoritative_head": dashboard_payload.get(
            "authoritative_head",
            mirror_payload.get("expected_head", ""),
        ),
        "mirrors_synchronized": bool(mirror_payload.get("synchronized", False)),
        "mirror_errors": mirror_payload.get("errors", ()),
        "contact_evidence_fresh": bool(contact_payload.get("all_contacts_fresh", False)),
        "ready_for_remote_write": bool(dashboard_payload.get("ready_for_remote_write", False)),
        "readiness_blockers": dashboard_payload.get("readiness_blockers", ()),
        "next_action": dashboard_payload.get("next_action", ""),
        "mirrors": mirrors,
        "routine": routine,
        "safari_sync": safari_sync,
        "contact_report": contact_report,
        "dashboard": dashboard,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh runtime federation state after local CLI pushes mirrored commits."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--mirror-attempts", type=int, default=3)
    parser.add_argument("--mirror-retry-delay", type=float, default=0.5)
    parser.add_argument("--no-desktop-contact", action="store_true")
    parser.add_argument("--no-safari-contact", action="store_true")
    parser.add_argument("--safari-watch-timeout", type=float, default=3.0)
    parser.add_argument("--safari-watch-interval", type=float, default=1.0)
    parser.add_argument("--output", type=Path, default=Path("reports/federation_post_push_refresh_latest.json"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_refresh(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.output)
    if not result["commands_succeeded"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
