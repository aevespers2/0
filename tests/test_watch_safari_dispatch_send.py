from __future__ import annotations

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
