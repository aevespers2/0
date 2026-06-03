from __future__ import annotations

import json

import argparse

from scripts.stage_safari_dispatch import build_handoff_text, safari_probe_script, stage_dispatch


def dispatch_payload() -> dict:
    return {
        "authoritative_head": "abc123",
        "dispatch": {
            "packet_type": "status",
            "expected_path": "FederationInbox/safari/status.json",
            "command": "python3 scripts/write_federation_message.py",
            "status_template": {
                "schema": "codex_federation_message.v1",
                "agent": "safari_cloud",
                "commit": "abc123",
            },
        },
    }


def test_build_handoff_text_uses_current_dispatch_head() -> None:
    text = build_handoff_text(dispatch_payload())

    assert "Current repo head: abc123" in text
    assert "FederationInbox/safari/status.json" in text
    assert '"agent": "safari_cloud"' in text


def test_safari_probe_script_embeds_json_escaped_handoff() -> None:
    text = 'hello "quoted" handoff'
    script = safari_probe_script(text)

    assert json.dumps(text) in script
    assert "composer_contains_handoff" in script
    assert "HTMLTextAreaElement.prototype" in script
    assert "send_button_enabled" in script


def test_stage_dispatch_reports_disabled_send_button(monkeypatch, tmp_path) -> None:
    dispatch = tmp_path / "dispatch.json"
    dispatch.write_text(json.dumps(dispatch_payload()), encoding="utf-8")

    monkeypatch.setattr(
        "scripts.stage_safari_dispatch.run_osascript",
        lambda script: {
            "staged": True,
            "title": "ChatGPT",
            "url": "https://chatgpt.com/c/example",
            "composer_contains_handoff": True,
            "send_button_visible": True,
            "send_button_enabled": False,
            "stop_answering_visible": False,
        },
    )

    result = stage_dispatch(
        argparse.Namespace(
            dispatch=dispatch,
            log=tmp_path / "contact.jsonl",
            latest=tmp_path / "latest.json",
            print_result=True,
        )
    )

    event = result["contact_event"]
    assert event["status"] == "staged"
    assert "visible but disabled" in event["detail"]
    assert event["evidence"]["send_button_enabled"] == "false"
