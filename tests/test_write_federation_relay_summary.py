from __future__ import annotations

import json

from scripts.write_federation_relay_summary import build_summary, next_action_for, write_summary


def write_json(path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_build_summary_combines_bridge_dispatch_and_contact(tmp_path) -> None:
    bridge = tmp_path / "bridge.json"
    dispatch = tmp_path / "dispatch.json"
    contact = tmp_path / "contact.json"
    write_json(
        bridge,
        {
            "authoritative_head": "abc123",
            "ready_for_remote_write": False,
            "required_packets": ["safari_cloud"],
            "missing_surfaces": ["safari_cloud"],
        },
    )
    write_json(
        dispatch,
        {
            "dispatch": {
                "agent": "safari_cloud",
                "expected_path": "FederationInbox/safari/status.json",
                "packet_type": "status",
            }
        },
    )
    write_json(
        contact,
        {
            "surface": "safari_cloud",
            "status": "blocked",
            "detail": "send unavailable",
            "evidence": {"stop_answering_visible": "true"},
        },
    )

    summary = build_summary(bridge, dispatch, contact)

    assert summary["schema"] == "codex_federation_relay_summary.v1"
    assert summary["authoritative_head"] == "abc123"
    assert summary["latest_contact_status"] == "blocked"
    assert "Wait for safari_cloud" in summary["next_action"]


def test_next_action_tracks_staged_and_sent_states() -> None:
    bridge = {"required_packets": ["safari_cloud"]}
    dispatch = {"agent": "safari_cloud", "expected_path": "FederationInbox/safari/status.json"}

    assert next_action_for(bridge, dispatch, {"status": "staged"}).startswith("Send staged handoff")
    assert next_action_for(bridge, dispatch, {"status": "sent"}).startswith("Await safari_cloud")
    assert next_action_for({"required_packets": []}, dispatch, {}).startswith("No required")


def test_write_summary_creates_output(tmp_path) -> None:
    output = tmp_path / "reports" / "summary.json"

    write_summary({"schema": "example"}, output)

    assert json.loads(output.read_text(encoding="utf-8"))["schema"] == "example"
