from __future__ import annotations

import argparse

from scripts import nudge_safari_sendability


def test_nudge_scripts_are_bounded_to_input_events() -> None:
    input_script = nudge_safari_sendability.input_nudge_script()
    exec_script = nudge_safari_sendability.exec_command_nudge_script()

    assert "KeyboardEvent" in input_script
    assert "InputEvent" in input_script
    assert "execCommand('insertText'" in exec_script
    assert "button.click" not in input_script + exec_script


def test_run_nudges_stops_after_send_enabled(monkeypatch, tmp_path) -> None:
    probes = [
        {"send_button_enabled": False, "stop_answering_visible": False},
        {"send_button_enabled": True, "stop_answering_visible": False},
    ]
    scripts = []

    def fake_run(script):
        scripts.append(script)
        if "composer_contains_handoff" in script:
            return probes.pop(0)
        return {"applied": True}

    monkeypatch.setattr(nudge_safari_sendability, "run_osascript", fake_run)

    result = nudge_safari_sendability.run_nudges(argparse.Namespace(wait=0, output=tmp_path / "out.json", print_result=False))

    assert result["sendable"] is True
    assert len(result["attempts"]) == 1
    assert any("KeyboardEvent" in script for script in scripts)
