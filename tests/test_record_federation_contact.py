from __future__ import annotations

import argparse
import json

import pytest

from scripts.record_federation_contact import build_contact_event, parse_evidence, write_contact_event


def test_parse_evidence_requires_key_value() -> None:
    assert parse_evidence(["title=Cognitive OS Development", "composer=true"]) == {
        "title": "Cognitive OS Development",
        "composer": "true",
    }
    with pytest.raises(ValueError, match="key=value"):
        parse_evidence(["bad"])


def test_build_contact_event_loads_dispatch(tmp_path) -> None:
    dispatch = tmp_path / "dispatch.json"
    dispatch.write_text(json.dumps({"schema": "codex_federation_surface_dispatch.v1"}), encoding="utf-8")
    args = argparse.Namespace(
        surface="safari_cloud",
        channel="safari_chatgpt",
        status="staged",
        authoritative_head="abc123",
        dispatch=str(dispatch),
        detail="handoff inserted",
        evidence=["composer=true"],
    )

    event = build_contact_event(args)

    assert event["schema"] == "codex_federation_contact.v1"
    assert event["surface"] == "safari_cloud"
    assert event["dispatch"]["schema"] == "codex_federation_surface_dispatch.v1"
    assert event["evidence"] == {"composer": "true"}


def test_write_contact_event_appends_log_and_latest(tmp_path) -> None:
    event = {"schema": "codex_federation_contact.v1", "surface": "desktop_app"}
    log = tmp_path / "reports" / "contact.jsonl"
    latest = tmp_path / "reports" / "latest.json"

    write_contact_event(event, log, latest)
    write_contact_event(event, log, latest)

    assert len(log.read_text(encoding="utf-8").splitlines()) == 2
    assert json.loads(latest.read_text(encoding="utf-8"))["surface"] == "desktop_app"
