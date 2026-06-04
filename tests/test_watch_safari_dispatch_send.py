from __future__ import annotations

import argparse

from scripts import watch_safari_dispatch_send
from scripts.watch_safari_dispatch_send import safari_click_send_script, safari_probe_script


def test_probe_script_checks_send_and_stop_state() -> None:
    script = safari_probe_script()

    assert "send_button_visible" in script
    assert "stop_answering_visible" in script
    assert "Federation handoff from Local CLI" in script
    assert "send-button" in script
    assert "composer-submit-button" in script
    assert "sendButton.disabled" in script
    assert "ariaDisabled" in script
    assert "send_button_disabled" in script
    assert "send_button_label" in script
    assert "send_button_id" in script
    assert "send_button_testid" in script


def test_click_script_refuses_non_send_button() -> None:
    script = safari_click_send_script(3)

    assert "button_not_send" in script
    assert "button.click()" in script
    assert "send-button" in script
    assert "composer-submit-button" in script
    assert "aria-disabled" in script


def test_wait_for_sendable_waits_for_enabled_send_button(monkeypatch) -> None:
    probes = [
        {
            "send_button_visible": True,
            "send_button_enabled": False,
            "stop_answering_visible": False,
        },
        {
            "send_button_visible": True,
            "send_button_enabled": True,
            "stop_answering_visible": False,
        },
    ]
    monkeypatch.setattr(watch_safari_dispatch_send, "run_osascript", lambda _script: probes.pop(0))
    monkeypatch.setattr(watch_safari_dispatch_send.time, "sleep", lambda _interval: None)

    probe = watch_safari_dispatch_send.wait_for_sendable(1, 0)

    assert probe["send_button_enabled"] is True


def test_watch_fails_closed_when_current_tab_does_not_match_target(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        watch_safari_dispatch_send,
        "wait_for_sendable",
        lambda timeout, interval: {
            "url": "https://chatgpt.com/c/wrong",
            "title": "ChatGPT",
            "composer_contains_handoff": True,
            "send_button_visible": True,
            "send_button_enabled": True,
            "send_button_index": 1,
            "stop_answering_visible": False,
        },
    )

    def fail_if_send(script):
        raise AssertionError("watch must not click send in the wrong tab")

    monkeypatch.setattr(watch_safari_dispatch_send, "run_osascript", fail_if_send)
    result = watch_safari_dispatch_send.watch(
        argparse.Namespace(
            timeout=0,
            interval=0,
            send=True,
            dispatch=tmp_path / "dispatch.json",
            authoritative_head="abc123",
            target=tmp_path / "missing-target.json",
            url="https://chatgpt.com/c/expected",
            log=tmp_path / "contact.jsonl",
            latest=tmp_path / "latest.json",
        )
    )

    event = result["contact_event"]
    assert event["status"] == "failed"
    assert "wrong tab" in event["detail"]
    assert event["evidence"]["target_url_matched"] == "false"
    assert result["send_result"] is None


def test_watch_reports_visible_disabled_send_as_blocked(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        watch_safari_dispatch_send,
        "wait_for_sendable",
        lambda timeout, interval: {
            "url": "https://chatgpt.com/c/expected",
            "title": "ChatGPT",
            "composer_contains_handoff": True,
            "send_button_visible": True,
            "send_button_enabled": False,
            "send_button_disabled": True,
            "send_button_label": "Send prompt",
            "send_button_id": "composer-submit-button",
            "send_button_testid": "send-button",
            "send_button_aria_disabled": "",
            "send_button_index": 1,
            "stop_answering_visible": False,
        },
    )
    result = watch_safari_dispatch_send.watch(
        argparse.Namespace(
            timeout=0,
            interval=0,
            send=False,
            dispatch=tmp_path / "dispatch.json",
            authoritative_head="abc123",
            target=tmp_path / "missing-target.json",
            url="https://chatgpt.com/c/expected",
            log=tmp_path / "contact.jsonl",
            latest=tmp_path / "latest.json",
        )
    )

    event = result["contact_event"]
    assert event["status"] == "blocked"
    assert event["evidence"]["send_button_visible"] == "true"
    assert event["evidence"]["send_button_enabled"] == "false"
    assert event["evidence"]["send_button_disabled"] == "true"
    assert event["evidence"]["send_button_label"] == "Send prompt"
    assert event["evidence"]["send_button_id"] == "composer-submit-button"
    assert event["evidence"]["send_button_testid"] == "send-button"
