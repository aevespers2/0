from __future__ import annotations

import json

from scripts.stage_safari_dispatch import build_handoff_text, safari_probe_script


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
