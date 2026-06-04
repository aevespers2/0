from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SURFACE_ORDER = ("local_cli", "safari_cloud", "desktop_app", "mobile", "chatgpt_bridge")
INBOX_SURFACE_DIRS = {
    "local_cli": "local",
    "safari_cloud": "safari",
    "desktop_app": "desktop",
    "mobile": "mobile",
    "chatgpt_bridge": "bridge",
}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def dispatch_by_agent(dispatch: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("agent", "")): item for item in dispatch.get("dispatches", ()) if item.get("agent")}


def contact_by_surface(contact_report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("surface", "")): item for item in contact_report.get("surfaces", ()) if item.get("surface")}


def load_inbox_statuses(inbox: Path) -> dict[str, dict[str, Any]]:
    statuses: dict[str, dict[str, Any]] = {}
    for surface, surface_dir in INBOX_SURFACE_DIRS.items():
        path = inbox / surface_dir / "status.json"
        packet = load_json(path)
        if packet:
            packet["_path"] = str(path)
            statuses[surface] = packet
    return statuses


def surface_role(dispatch: dict[str, Any], surface: str) -> dict[str, Any]:
    return dispatch.get("parallel_work", {}).get("surfaces", {}).get(surface, {})


def command_for_surface(
    surface: str,
    dashboard: dict[str, Any],
    relay_summary: dict[str, Any],
    dispatches: dict[str, dict[str, Any]],
    authoritative_head: str,
) -> str:
    if surface == "safari_cloud" and dashboard.get("relay_status") == "blocked":
        evidence = relay_summary.get("latest_contact_evidence", {})
        source_url = str(evidence.get("target_url") or evidence.get("url") or "")
        source_arg = f' --source-url "{source_url}"' if source_url else ""
        return f"python3 scripts/extract_safari_ack.py --clipboard{source_arg} --write-status --print"
    if surface in dispatches:
        return str(dispatches[surface].get("command", ""))
    if surface == "local_cli":
        return "python3 scripts/run_federation_post_push_refresh.py --print"
    if surface == "desktop_app":
        return "python3 scripts/probe_desktop_codex_app.py --print"
    if surface == "mobile":
        return "python3 scripts/write_mobile_federation_status.py --output FederationInbox/mobile/status.json"
    if surface == "chatgpt_bridge":
        head_arg = f' --authoritative-head "{authoritative_head}"' if authoritative_head else ""
        return f"python3 scripts/emit_bridge_signal.py{head_arg} --print"
    return ""


def next_action_for_surface(
    surface: str,
    dashboard: dict[str, Any],
    relay_summary: dict[str, Any],
    contact: dict[str, Any],
    inbox_status: dict[str, Any],
    dispatches: dict[str, dict[str, Any]],
) -> str:
    if surface in dispatches:
        if surface == "safari_cloud" and dashboard.get("relay_status") == "blocked":
            return str(dashboard.get("next_action") or relay_summary.get("next_action", ""))
        return str(dispatches[surface].get("status_template", {}).get("next_action", ""))
    if surface == "local_cli":
        return str(
            inbox_status.get("next_action")
            or "Remain authoritative for commits, pushes, tests, and integration; continue refreshing runtime federation state."
        )
    if surface == "safari_cloud":
        return str(dashboard.get("next_action") or relay_summary.get("next_action", ""))
    if surface == "desktop_app":
        return str(
            contact.get("actionable_detail")
            or contact.get("detail")
            or inbox_status.get("next_action")
            or "Report Desktop Codex app status only."
        )
    if surface == "mobile":
        return str(
            inbox_status.get("next_action")
            or "Collect user-facing priorities, approvals, blockers, and completion follow-up into FederationInbox/mobile/status.json."
        )
    if surface == "chatgpt_bridge":
        return str(
            inbox_status.get("next_action")
            or "Review coordination state, propose task splits, and return advisory planning feedback without direct pushes."
        )
    return ""


def status_for_surface(
    surface: str,
    dashboard: dict[str, Any],
    contact: dict[str, Any],
    inbox_status: dict[str, Any],
    authoritative_head: str,
) -> str:
    contact_status = dashboard.get("contact_surfaces", {}).get(
        surface,
        contact.get("actionable_status") or contact.get("status", ""),
    )
    packet_stale = packet_is_stale(inbox_status, authoritative_head)
    if packet_stale and inbox_status.get("blocker"):
        return "stale_blocked"
    if packet_stale:
        return "stale"
    if contact_status:
        return str(contact_status)
    if not inbox_status:
        return ""
    if inbox_status.get("blocker"):
        return "blocked"
    if inbox_status.get("type") == "status":
        return "reported"
    return str(inbox_status.get("type") or "reported")


def packet_is_stale(inbox_status: dict[str, Any], authoritative_head: str) -> bool:
    packet_commit = str(inbox_status.get("commit", "") or "")
    return bool(packet_commit and authoritative_head and packet_commit != authoritative_head)


def stale_packet_next_action(surface: str, inbox_status: dict[str, Any], authoritative_head: str) -> str:
    path = str(inbox_status.get("_path", ""))
    packet_commit = str(inbox_status.get("commit", ""))
    surface_name = surface
    return (
        f"Refresh {surface_name} status at {path or 'its FederationInbox status path'} "
        f"from packet commit {packet_commit or 'unknown'} to authoritative head {authoritative_head}; "
        "if the surface cannot write directly, submit an equivalent codex_federation_message.v1 status packet "
        "through Local CLI for validation."
    )


def detail_for_surface(contact: dict[str, Any], inbox_status: dict[str, Any]) -> str:
    if contact.get("actionable_detail") or contact.get("detail"):
        return str(contact.get("actionable_detail") or contact.get("detail"))
    if inbox_status.get("blocker"):
        return str(inbox_status.get("blocker", ""))
    status_short = inbox_status.get("status_short") or ()
    if status_short:
        return "; ".join(str(item) for item in status_short)
    return ""


def build_surface_packet(
    surface: str,
    dashboard: dict[str, Any],
    relay_summary: dict[str, Any],
    dispatch: dict[str, Any],
    contacts: dict[str, dict[str, Any]],
    inbox_statuses: dict[str, dict[str, Any]],
    dispatches: dict[str, dict[str, Any]],
    authoritative_head: str,
) -> dict[str, Any]:
    contact = contacts.get(surface, {})
    inbox_status = inbox_statuses.get(surface, {})
    role = surface_role(dispatch, surface)
    packet_stale = packet_is_stale(inbox_status, authoritative_head)
    next_action = next_action_for_surface(surface, dashboard, relay_summary, contact, inbox_status, dispatches)
    if packet_stale:
        next_action = stale_packet_next_action(surface, inbox_status, authoritative_head)
    return {
        "surface": surface,
        "role": role.get("role", ""),
        "handoff_type": role.get("handoff_type", ""),
        "status": status_for_surface(surface, dashboard, contact, inbox_status, authoritative_head),
        "required": surface in dispatches or surface in dashboard.get("required_packets", ()),
        "constraints": role.get("constraints", ()),
        "may_execute": role.get("may_execute", ()),
        "must_report": role.get("must_report", ()),
        "next_action": next_action,
        "command": command_for_surface(surface, dashboard, relay_summary, dispatches, authoritative_head),
        "expected_path": dispatches.get(surface, {}).get("expected_path", inbox_status.get("_path", "")),
        "detail": detail_for_surface(contact, inbox_status),
        "packet_path": inbox_status.get("_path", ""),
        "packet_commit": inbox_status.get("commit", ""),
        "packet_generated_at": inbox_status.get("generated_at", ""),
        "packet_fresh": bool(inbox_status.get("commit")) and not packet_stale,
        "packet_stale": packet_stale,
        "packet_expected_commit": authoritative_head,
        "packet_stale_reason": (
            f"packet commit {inbox_status.get('commit', '')} differs from authoritative head {authoritative_head}"
            if packet_stale
            else ""
        ),
        "blocker": inbox_status.get("blocker", ""),
    }


def build_handoff(
    dashboard: dict[str, Any],
    contact_report: dict[str, Any],
    relay_summary: dict[str, Any],
    dispatch: dict[str, Any],
    inbox_statuses: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    dispatches = dispatch_by_agent(dispatch)
    contacts = contact_by_surface(contact_report)
    inbox_statuses = inbox_statuses or {}
    authoritative_head = str(dashboard.get("authoritative_head") or dispatch.get("authoritative_head", ""))
    surfaces = tuple(
        build_surface_packet(
            surface,
            dashboard,
            relay_summary,
            dispatch,
            contacts,
            inbox_statuses,
            dispatches,
            authoritative_head,
        )
        for surface in SURFACE_ORDER
    )
    return {
        "schema": "codex_federation_operator_handoff.v1",
        "authoritative_head": authoritative_head,
        "ready_for_remote_write": bool(dashboard.get("ready_for_remote_write", False)),
        "readiness_blockers": dashboard.get("readiness_blockers", ()),
        "mirrors_synchronized": bool(dashboard.get("mirrors_synchronized", False)),
        "contact_evidence_fresh": bool(dashboard.get("contact_evidence_fresh", False)),
        "next_action": dashboard.get("next_action", ""),
        "coordination_rule": dispatch.get("parallel_work", {}).get("coordination_rule", ""),
        "merge_rule": dispatch.get("parallel_work", {}).get("merge_rule", ""),
        "surfaces": surfaces,
    }


def build_text(payload: dict[str, Any]) -> str:
    lines = [
        "Federation Operator Handoff",
        f"Head: {payload.get('authoritative_head', '')}",
        f"Ready for remote write: {str(payload.get('ready_for_remote_write', False)).lower()}",
        f"Mirrors synchronized: {str(payload.get('mirrors_synchronized', False)).lower()}",
        f"Next action: {payload.get('next_action', '')}",
        "",
        "Surfaces:",
    ]
    for surface in payload.get("surfaces", ()):
        lines.extend(
            [
                f"- {surface.get('surface', '')}: {surface.get('status', '')} / {surface.get('role', '')}",
                f"  action: {surface.get('next_action', '')}",
                f"  command: {surface.get('command', '')}",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(payload: dict[str, Any], json_output: Path, text_output: Path) -> None:
    json_output.parent.mkdir(parents=True, exist_ok=True)
    text_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    text_output.write_text(build_text(payload), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write an all-surface federation operator handoff.")
    parser.add_argument("--dashboard", type=Path, default=Path("reports/federation_dashboard.json"))
    parser.add_argument("--contact-report", type=Path, default=Path("reports/federation_contact_report.json"))
    parser.add_argument("--relay-summary", type=Path, default=Path("reports/federation_relay_summary.json"))
    parser.add_argument("--dispatch", type=Path, default=Path("FederationDispatch/dispatch.json"))
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--json-output", type=Path, default=Path("reports/federation_operator_handoff_latest.json"))
    parser.add_argument("--text-output", type=Path, default=Path("reports/federation_operator_handoff_latest.txt"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_handoff(
        load_json(args.dashboard),
        load_json(args.contact_report),
        load_json(args.relay_summary),
        load_json(args.dispatch),
        load_inbox_statuses(args.inbox),
    )
    write_outputs(payload, args.json_output, args.text_output)
    if args.print_result:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(args.json_output)


if __name__ == "__main__":
    main()
