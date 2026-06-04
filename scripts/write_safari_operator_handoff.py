from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_handoff(
    dashboard: dict[str, Any],
    relay_summary: dict[str, Any],
    nudge: dict[str, Any],
) -> dict[str, Any]:
    expected_path = relay_summary.get("dispatch_expected_path", "FederationInbox/safari/status.json")
    relay_evidence = relay_summary.get("latest_contact_evidence", {})
    nudge_after = nudge.get("after", {})
    target_url = str(relay_evidence.get("target_url") or nudge_after.get("url") or "")
    send_disabled = (
        relay_evidence.get("composer_contains_handoff") == "true"
        and relay_evidence.get("send_button_enabled") == "false"
    ) or (
        nudge_after.get("composer_contains_handoff") is True
        and nudge_after.get("send_button_enabled") is False
    )
    status = "blocked_send_disabled" if send_disabled else str(relay_summary.get("latest_contact_status", "unknown"))
    instructions = [
        "Open the Safari ChatGPT conversation.",
        "Confirm the federation handoff text is still in the composer.",
        "If ChatGPT enables Send, send the handoff.",
        f"After Safari responds, collect or transcribe the status packet to {expected_path}.",
        (
            "If Send remains disabled but a Safari response packet can be copied, copy it and run: "
            "python3 scripts/extract_safari_ack.py --clipboard "
            f"--source-url \"{target_url}\" --write-status --print"
        ),
        (
            "File fallback: python3 scripts/extract_safari_ack.py --text-file <copied-response.txt> "
            f"--source-url \"{target_url}\" --write-status --print"
        ),
        "Do not push directly from Safari; export patch proposals for Local CLI review.",
    ]
    return {
        "schema": "codex_safari_operator_handoff.v1",
        "authoritative_head": dashboard.get("authoritative_head", ""),
        "status": status,
        "ready_for_remote_write": bool(dashboard.get("ready_for_remote_write", False)),
        "expected_packet": expected_path,
        "manual_ingest_command": (
            "python3 scripts/extract_safari_ack.py --clipboard "
            f"--source-url \"{target_url}\" --write-status --print"
        ),
        "manual_file_ingest_command": (
            "python3 scripts/extract_safari_ack.py --text-file <copied-response.txt> "
            f"--source-url \"{target_url}\" --write-status --print"
        ),
        "next_action": dashboard.get("next_action") or relay_summary.get("next_action", ""),
        "target_url": target_url,
        "composer_contains_handoff": (
            relay_evidence.get("composer_contains_handoff") == "true"
            or nudge_after.get("composer_contains_handoff") is True
        ),
        "send_button_enabled": (
            relay_evidence.get("send_button_enabled") == "true"
            or nudge_after.get("send_button_enabled") is True
        ),
        "sendability_nudge_sendable": bool(nudge.get("sendable", False)),
        "nudge_attempt_count": len(nudge.get("attempts", ())),
        "instructions": instructions,
    }


def build_text(payload: dict[str, Any]) -> str:
    instructions = "\n".join(f"- {item}" for item in payload.get("instructions", ()))
    return (
        "Safari Federation Operator Handoff\n"
        f"Head: {payload.get('authoritative_head', '')}\n"
        f"Status: {payload.get('status', '')}\n"
        f"Expected packet: {payload.get('expected_packet', '')}\n"
        f"Next action: {payload.get('next_action', '')}\n\n"
        f"{instructions}\n"
    )


def write_outputs(payload: dict[str, Any], json_output: Path, text_output: Path) -> None:
    json_output.parent.mkdir(parents=True, exist_ok=True)
    text_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    text_output.write_text(build_text(payload), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write concise Safari operator handoff artifacts.")
    parser.add_argument("--dashboard", type=Path, default=Path("reports/federation_dashboard.json"))
    parser.add_argument("--relay-summary", type=Path, default=Path("reports/federation_relay_summary.json"))
    parser.add_argument("--nudge-report", type=Path, default=Path("reports/safari_sendability_nudge_latest.json"))
    parser.add_argument("--json-output", type=Path, default=Path("FederationRelay/safari_operator_handoff.json"))
    parser.add_argument("--text-output", type=Path, default=Path("FederationRelay/safari_operator_handoff.txt"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_handoff(
        load_json(args.dashboard),
        load_json(args.relay_summary),
        load_json(args.nudge_report),
    )
    write_outputs(payload, args.json_output, args.text_output)
    if args.print_result:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(args.json_output)


if __name__ == "__main__":
    main()
