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


def test_run_ingests_copied_text_file_and_writes_status(tmp_path) -> None:
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
    text_file = tmp_path / "safari-response.txt"
    text_file.write_text(f"Here is the packet:\n{json.dumps(payload)}\n", encoding="utf-8")
    args = argparse.Namespace(
        dispatch=tmp_path / "missing.json",
        authoritative_head="abc123",
        inbox=tmp_path / "FederationInbox",
        write_status=True,
        text_file=text_file,
        stdin=False,
        source_url="https://chatgpt.com/c/test",
        target=tmp_path / "missing-target.json",
        url="",
        log=tmp_path / "contact.jsonl",
        latest=tmp_path / "latest.json",
    )

    result = extract_safari_ack.run(args)

    status_path = tmp_path / "FederationInbox" / "safari" / "status.json"
    assert result["written_path"] == str(status_path)
    assert result["contact_event"]["status"] == "acknowledged"
    assert json.loads(status_path.read_text(encoding="utf-8")) == payload


def test_snapshot_source_rejects_multiple_manual_inputs(tmp_path) -> None:
    args = argparse.Namespace(
        text_file=tmp_path / "safari-response.txt",
        stdin=True,
        source_url="",
        target=tmp_path / "missing-target.json",
        url="",
    )

    try:
        extract_safari_ack.snapshot_from_source(args)
    except ValueError as exc:
        assert str(exc) == "choose only one manual input source"
    else:
        raise AssertionError("expected manual input conflict to fail closed")


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
        text_file=None,
        stdin=False,
        source_url="",
        target=tmp_path / "missing-target.json",
        url="",
        log=tmp_path / "contact.jsonl",
        latest=tmp_path / "latest.json",
    )

    result = extract_safari_ack.run(args)

    assert result["candidate"] is None
    assert result["contact_event"]["status"] == "observed"
    assert not (tmp_path / "FederationInbox" / "safari" / "status.json").exists()


def test_run_refuses_to_extract_from_wrong_target_url(monkeypatch, tmp_path) -> None:
    payload = {
        "schema": "codex_federation_message.v1",
        "agent": "safari_cloud",
        "type": "status",
        "commit": "abc123",
    }
    monkeypatch.setattr(
        extract_safari_ack,
        "run_osascript",
        lambda _script: {
            "url": "https://chatgpt.com/c/wrong",
            "title": "ChatGPT",
            "message_count": 1,
            "messages": [{"role": "assistant", "text": json.dumps(payload)}],
        },
    )
    args = argparse.Namespace(
        dispatch=tmp_path / "missing.json",
        authoritative_head="abc123",
        inbox=tmp_path / "FederationInbox",
        write_status=True,
        text_file=None,
        stdin=False,
        source_url="",
        target=tmp_path / "missing-target.json",
        url="https://chatgpt.com/c/expected",
        log=tmp_path / "contact.jsonl",
        latest=tmp_path / "latest.json",
    )

    result = extract_safari_ack.run(args)

    assert result["candidate"] is None
    assert result["contact_event"]["status"] == "failed"
    assert result["contact_event"]["evidence"]["target_url_matched"] == "false"
    assert not (tmp_path / "FederationInbox" / "safari" / "status.json").exists()
