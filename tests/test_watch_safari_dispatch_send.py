from __future__ import annotations

import argparse

from scripts import watch_safari_dispatch_send
from scripts.watch_safari_dispatch_send import safari_click_send_script, safari_probe_script


def test_probe_script_checks_send_and_stop_state() -> None:
    script = safari_probe_script()

    assert "send_button_visible" in script
    assert "stop_answering_visible" in script
    assert "Federation handoff from Local CLI" in script


def test_click_script_refuses_non_send_button() -> None:
    script = safari_click_send_script(3)

    assert "button_not_send" in script
    assert "button.click()" in script
    assert "toLowerCase().includes('send')" in script


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
