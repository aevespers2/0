from __future__ import annotations

import argparse
import json
import subprocess

from scripts import probe_desktop_codex_app


def args(tmp_path, **overrides):
    defaults = {
        "app_name": "Codex",
        "dispatch": tmp_path / "missing.json",
        "authoritative_head": "abc123",
        "log": tmp_path / "contact.jsonl",
        "latest": tmp_path / "latest.json",
        "print_result": False,
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_status_for_visible_desktop_app() -> None:
    probe = {
        "process_running": True,
        "window_count": 1,
        "frontmost": False,
        "window_titles": ["Codex"],
    }

    assert probe_desktop_codex_app.status_for_probe(probe) == "observed"
    assert "accessible window" in probe_desktop_codex_app.detail_for_probe(probe)


def test_status_for_running_desktop_app_without_accessible_window() -> None:
    probe = {
        "process_running": True,
        "window_count": 0,
        "frontmost": True,
        "window_titles": [],
    }

    assert probe_desktop_codex_app.status_for_probe(probe) == "observed"
    assert "no accessible window" in probe_desktop_codex_app.detail_for_probe(probe)


def test_status_for_missing_desktop_app() -> None:
    probe = {"process_running": False, "window_count": 0}

    assert probe_desktop_codex_app.status_for_probe(probe) == "blocked"
    assert "process was not found" in probe_desktop_codex_app.detail_for_probe(probe)


def test_run_records_observed_contact(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        probe_desktop_codex_app,
        "run_osascript",
        lambda _script: {
            "app_name": "Codex",
            "process_running": True,
            "window_count": 1,
            "frontmost": True,
            "window_titles": ["Autonomous VNext"],
        },
    )

    result = probe_desktop_codex_app.run(args(tmp_path))

    assert result["contact_event"]["status"] == "observed"
    assert result["contact_event"]["surface"] == "desktop_app"
    assert json.loads((tmp_path / "latest.json").read_text(encoding="utf-8"))["status"] == "observed"


def test_run_records_failed_contact_on_probe_error(monkeypatch, tmp_path) -> None:
    def raise_error(_script):
        raise subprocess.CalledProcessError(1, ["osascript"], stderr="no access")

    monkeypatch.setattr(probe_desktop_codex_app, "run_osascript", raise_error)

    result = probe_desktop_codex_app.run(args(tmp_path))

    assert result["contact_event"]["status"] == "failed"
    assert result["probe"]["error"]
