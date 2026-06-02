from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_latest_contact_for_surface(
    latest_contact_path: Path,
    contact_log_path: Path,
    surface: str,
) -> dict[str, Any]:
    latest = load_json(latest_contact_path)
    if not surface or latest.get("surface") == surface:
        return latest
    if not contact_log_path.exists():
        return {}
    for line in reversed(contact_log_path.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("surface") == surface:
            return event
    return {}


def build_summary(
    bridge_signal_path: Path,
    dispatch_path: Path,
    latest_contact_path: Path,
    contact_log_path: Path | None = None,
) -> dict[str, Any]:
    bridge = load_json(bridge_signal_path)
    dispatch = load_json(dispatch_path)
    dispatch_body = dispatch.get("dispatch", {})
    contact = load_latest_contact_for_surface(
        latest_contact_path,
        contact_log_path or Path(""),
        str(dispatch_body.get("agent", "")),
    )
    return {
        "schema": "codex_federation_relay_summary.v1",
        "authoritative_head": (
            bridge.get("authoritative_head")
            or dispatch.get("authoritative_head")
            or contact.get("authoritative_head", "")
        ),
        "ready_for_remote_write": bridge.get("ready_for_remote_write", False),
        "required_packets": bridge.get("required_packets", ()),
        "missing_surfaces": bridge.get("missing_surfaces", ()),
        "blocked_surfaces": bridge.get("blocked_surfaces", ()),
        "stale_surfaces": bridge.get("stale_surfaces", ()),
        "dispatch_agent": dispatch_body.get("agent", ""),
        "dispatch_expected_path": dispatch_body.get("expected_path", ""),
        "dispatch_packet_type": dispatch_body.get("packet_type", ""),
        "latest_contact_surface": contact.get("surface", ""),
        "latest_contact_status": contact.get("status", ""),
        "latest_contact_detail": contact.get("detail", ""),
        "latest_contact_evidence": contact.get("evidence", {}),
        "next_action": next_action_for(bridge, dispatch_body, contact),
    }


def next_action_for(
    bridge: dict[str, Any],
    dispatch: dict[str, Any],
    contact: dict[str, Any],
) -> str:
    required = bridge.get("required_packets", ())
    if not required:
        return "No required federation packets are pending."
    agent = dispatch.get("agent") or ", ".join(required)
    expected_path = dispatch.get("expected_path", "")
    status = contact.get("status", "")
    if status == "blocked":
        return f"Wait for {agent} sendability/acknowledgment, then collect {expected_path}."
    if status == "staged":
        return f"Send staged handoff to {agent}, then collect {expected_path}."
    if status == "sent":
        return f"Await {agent} acknowledgment and status packet at {expected_path}."
    if status == "acknowledged":
        return f"Transcribe or collect acknowledged {agent} packet at {expected_path}."
    if status == "observed" and contact.get("evidence", {}).get("candidate_found") == "false":
        return f"Continue watching {agent} sendability/acknowledgment, then collect {expected_path}."
    return f"Dispatch required packet request to {agent}, then collect {expected_path}."


def write_summary(summary: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a compact federation relay summary.")
    parser.add_argument("--bridge-signal", type=Path, default=Path("reports/federation_bridge_signal.json"))
    parser.add_argument("--dispatch", type=Path, default=Path("FederationDispatch/safari/dispatch.json"))
    parser.add_argument("--latest-contact", type=Path, default=Path("reports/federation_contact_latest.json"))
    parser.add_argument("--contact-log", type=Path, default=Path("reports/federation_contact_log.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("reports/federation_relay_summary.json"))
    parser.add_argument("--print", action="store_true", dest="print_summary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_summary(args.bridge_signal, args.dispatch, args.latest_contact, args.contact_log)
    write_summary(summary, args.output)
    if args.print_summary:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
