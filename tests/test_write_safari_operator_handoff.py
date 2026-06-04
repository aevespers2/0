from __future__ import annotations

import json

from scripts.write_safari_operator_handoff import build_handoff, build_text, write_outputs


def test_build_handoff_summarizes_send_disabled_state() -> None:
    payload = build_handoff(
        {"authoritative_head": "abc123", "next_action": "send disabled", "ready_for_remote_write": False},
        {
            "dispatch_expected_path": "FederationInbox/safari/status.json",
            "latest_contact_status": "blocked",
            "latest_contact_evidence": {
                "composer_contains_handoff": "true",
                "send_button_enabled": "false",
                "target_url": "https://chatgpt.com/c/example",
            },
        },
        {"sendable": False, "attempts": [{"result": {"strategy": "input_events"}}]},
    )

    assert payload["status"] == "blocked_send_disabled"
    assert payload["expected_packet"] == "FederationInbox/safari/status.json"
    assert payload["nudge_attempt_count"] == 1
    assert payload["composer_contains_handoff"] is True
    assert payload["send_button_enabled"] is False
    assert payload["target_url"] == "https://chatgpt.com/c/example"
    assert "extract_safari_ack.py" in payload["manual_ingest_command"]
    assert "--write-status" in payload["manual_ingest_command"]
    assert any("copied-response.txt" in item for item in payload["instructions"])


def test_build_text_includes_next_action() -> None:
    text = build_text(
        {
            "authoritative_head": "abc123",
            "status": "blocked_send_disabled",
            "expected_packet": "FederationInbox/safari/status.json",
            "next_action": "send it",
            "manual_ingest_command": "python3 scripts/extract_safari_ack.py --text-file copied.txt",
            "instructions": ["one", "two"],
        }
    )

    assert "Safari Federation Operator Handoff" in text
    assert "send it" in text
    assert "- one" in text


def test_write_outputs_creates_json_and_text(tmp_path) -> None:
    json_output = tmp_path / "handoff.json"
    text_output = tmp_path / "handoff.txt"

    write_outputs({"schema": "example", "instructions": []}, json_output, text_output)

    assert json.loads(json_output.read_text(encoding="utf-8"))["schema"] == "example"
    assert "Safari Federation" in text_output.read_text(encoding="utf-8")
