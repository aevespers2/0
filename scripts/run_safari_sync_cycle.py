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


def contact_status(result: dict[str, Any]) -> str:
    payload = parse_json_stdout(result)
    contact = payload.get("contact_event", {})
    return str(contact.get("status", ""))


def stage_succeeded(result: dict[str, Any]) -> bool:
    status = contact_status(result)
    return command_succeeded(result) and status != "failed"


def skipped_command(reason: str) -> dict[str, Any]:
    return {
        "command": [],
        "returncode": 1,
        "stdout": "",
        "stderr": reason,
        "skipped": True,
    }


def run_cycle(args: argparse.Namespace) -> dict[str, Any]:
    routine = run_command(["python3", "scripts/run_federation_routine.py", "--print"], args.repo)
    if not command_succeeded(routine):
        reason = "federation routine failed; refusing to stage stale dispatch"
        skipped = skipped_command(reason)
        return {
            "schema": "codex_safari_sync_cycle.v1",
            "send_requested": args.send,
            "write_status_requested": args.write_status,
            "commands_succeeded": False,
            "stage_skipped": True,
            "skip_reason": reason,
            "watch_status": "",
            "watch_detail": "",
            "ack_candidate_found": False,
            "ack_written_path": "",
            "relay_next_action": "Fix federation routine failure before staging Safari dispatch.",
            "ready_for_remote_write": False,
            "required_packets": (),
            "missing_surfaces": (),
            "contact_evidence_fresh": False,
            "dashboard_next_action": "",
            "routine": routine,
            "stage": skipped,
            "watch": skipped,
            "extract": skipped,
            "relay_summary": skipped,
            "contact_report": skipped,
            "dashboard": skipped,
        }

    stage = run_command(["python3", "scripts/stage_safari_dispatch.py", "--print"], args.repo)
    recovery = skipped_command("Safari dispatch staging succeeded; recovery not needed")
    if not stage_succeeded(stage) and args.recover_composer:
        recovery = run_command(["python3", "scripts/recover_safari_composer.py", "--print"], args.repo)
        if command_succeeded(recovery):
            recovery_payload = parse_json_stdout(recovery)
            if recovery_payload.get("recovered"):
                stage = run_command(["python3", "scripts/stage_safari_dispatch.py", "--print"], args.repo)
    if not stage_succeeded(stage):
        reason = "Safari dispatch staging failed; refusing to watch or extract stale state"
        skipped = skipped_command(reason)
        summary = run_command(["python3", "scripts/write_federation_relay_summary.py", "--print"], args.repo)
        contact_report = run_command(["python3", "scripts/write_federation_contact_report.py", "--print"], args.repo)
        dashboard = run_command(
            ["python3", "scripts/write_federation_dashboard.py", "--refresh-mirrors", "--print"],
            args.repo,
        )
        summary_payload = parse_json_stdout(summary)
        contact_payload = parse_json_stdout(contact_report)
        dashboard_payload = parse_json_stdout(dashboard)
        return {
            "schema": "codex_safari_sync_cycle.v1",
            "send_requested": args.send,
            "write_status_requested": args.write_status,
            "commands_succeeded": False,
            "stage_failed": True,
            "skip_reason": reason,
            "watch_status": "",
            "watch_detail": "",
            "ack_candidate_found": False,
            "ack_written_path": "",
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
            "recovery": recovery,
            "watch": skipped,
            "extract": skipped,
            "relay_summary": summary,
            "contact_report": contact_report,
            "dashboard": dashboard,
        }

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
    sendability_nudge = skipped_command("Safari watch did not require sendability nudge")
    if contact_status(watch) == "blocked" and args.nudge_sendability:
        sendability_nudge = run_command(["python3", "scripts/nudge_safari_sendability.py", "--print"], args.repo)
        if command_succeeded(sendability_nudge):
            nudge_payload = parse_json_stdout(sendability_nudge)
            if nudge_payload.get("sendable"):
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
        "recovery": recovery,
        "watch": watch,
        "sendability_nudge": sendability_nudge,
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
    parser.add_argument("--no-recover-composer", action="store_false", dest="recover_composer")
    parser.set_defaults(recover_composer=True)
    parser.add_argument("--no-nudge-sendability", action="store_false", dest="nudge_sendability")
    parser.set_defaults(nudge_sendability=True)
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
