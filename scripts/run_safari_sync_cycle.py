from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.run_safari_relay_retry import parse_json_stdout, run_command


def command_succeeded(result: dict[str, Any]) -> bool:
    return int(result.get("returncode", 1)) == 0


def run_cycle(args: argparse.Namespace) -> dict[str, Any]:
    routine = run_command(["python3", "scripts/run_federation_routine.py", "--print"], args.repo)
    stage = run_command(["python3", "scripts/stage_safari_dispatch.py", "--print"], args.repo)

    watch_command = [
        "python3",
        "scripts/watch_safari_dispatch_send.py",
        "--timeout",
        str(args.watch_timeout),
        "--interval",
        str(args.watch_interval),
        "--print",
    ]
    if args.send:
        watch_command.append("--send")
    watch = run_command(watch_command, args.repo)

    extract_command = ["python3", "scripts/extract_safari_ack.py", "--print"]
    if args.write_status:
        extract_command.append("--write-status")
    extract = run_command(extract_command, args.repo)
    summary = run_command(["python3", "scripts/write_federation_relay_summary.py", "--print"], args.repo)
    contact_report = run_command(["python3", "scripts/write_federation_contact_report.py", "--print"], args.repo)
    dashboard = run_command(
        ["python3", "scripts/write_federation_dashboard.py", "--refresh-mirrors", "--print"],
        args.repo,
    )

    watch_payload = parse_json_stdout(watch)
    extract_payload = parse_json_stdout(extract)
    summary_payload = parse_json_stdout(summary)
    contact_payload = parse_json_stdout(contact_report)
    dashboard_payload = parse_json_stdout(dashboard)
    contact = watch_payload.get("contact_event", {})
    candidate = extract_payload.get("candidate")
    return {
        "schema": "codex_safari_sync_cycle.v1",
        "send_requested": args.send,
        "write_status_requested": args.write_status,
        "commands_succeeded": all(
            command_succeeded(item)
            for item in (routine, stage, watch, extract, summary, contact_report, dashboard)
        ),
        "watch_status": contact.get("status", ""),
        "watch_detail": contact.get("detail", ""),
        "ack_candidate_found": candidate is not None,
        "ack_written_path": extract_payload.get("written_path", ""),
        "relay_next_action": summary_payload.get("next_action", ""),
        "ready_for_remote_write": dashboard_payload.get(
            "ready_for_remote_write",
            summary_payload.get("ready_for_remote_write", False),
        ),
        "required_packets": summary_payload.get("required_packets", ()),
        "missing_surfaces": summary_payload.get("missing_surfaces", ()),
        "contact_evidence_fresh": contact_payload.get("all_contacts_fresh", False),
        "dashboard_next_action": dashboard_payload.get("next_action", ""),
        "routine": routine,
        "stage": stage,
        "watch": watch,
        "extract": extract,
        "relay_summary": summary,
        "contact_report": contact_report,
        "dashboard": dashboard,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one Safari federation synchronization cycle."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--watch-timeout", type=float, default=5.0)
    parser.add_argument("--watch-interval", type=float, default=1.0)
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--write-status", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("reports/safari_sync_cycle_latest.json"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_cycle(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
