from __future__ import annotations

import argparse
import json

from scripts import extract_safari_ack


def test_iter_json_objects_ignores_invalid_braces_and_preserves_nested_json() -> None:
    text = 'noise {bad} {"schema":"x","nested":{"value":"brace } inside"}} tail'

    objects = extract_safari_ack.iter_json_objects(text)

    assert objects == ({"schema": "x", "nested": {"value": "brace } inside"}},)


def test_extract_candidate_requires_safari_message_and_authoritative_head() -> None:
    payload = {
        "schema": "codex_federation_message.v1",
        "agent": "safari_cloud",
        "type": "status",
        "commit": "abc123",
    }
    snapshot = {"messages": [{"role": "assistant", "text": json.dumps(payload)}]}

    assert extract_safari_ack.extract_candidate(snapshot, "abc123") == payload
    assert extract_safari_ack.extract_candidate(snapshot, "def456") is None


def test_write_status_packet_validates_and_targets_safari_status(tmp_path) -> None:
    payload = {
        "schema": "codex_federation_message.v1",
        "agent": "safari_cloud",
        "type": "status",
        "workstream": "Autonomous VNext",
        "cwd": "/workspace/0",
        "branch": "work",
        "commit": "abc123",
        "status_short": [],
        "remote": "",
        "blocker": "",
        "next_action": "Export patch proposals.",
    }

    path = extract_safari_ack.write_status_packet(payload, tmp_path / "FederationInbox")

    assert path == tmp_path / "FederationInbox" / "safari" / "status.json"
    assert json.loads(path.read_text(encoding="utf-8"))["agent"] == "safari_cloud"


def test_run_records_observed_without_candidate(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        extract_safari_ack,
        "run_osascript",
        lambda _script: {
            "url": "https://chatgpt.com/c/test",
            "title": "Cognitive OS Development",
            "message_count": 1,
            "messages": [{"role": "assistant", "text": "no json here"}],
        },
    )
    args = argparse.Namespace(
        dispatch=tmp_path / "missing.json",
        authoritative_head="abc123",
        inbox=tmp_path / "FederationInbox",
        write_status=False,
        log=tmp_path / "contact.jsonl",
        latest=tmp_path / "latest.json",
    )

    result = extract_safari_ack.run(args)

    assert result["candidate"] is None
    assert result["contact_event"]["status"] == "observed"
    assert not (tmp_path / "FederationInbox" / "safari" / "status.json").exists()
