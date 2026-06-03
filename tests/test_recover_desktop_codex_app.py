from __future__ import annotations

import argparse
import subprocess
import sys

from scripts import recover_desktop_codex_app


def args(tmp_path, **overrides):
    defaults = {
        "app_name": "Codex",
        "dispatch": tmp_path / "missing.json",
        "authoritative_head": "abc123",
        "wait": 0,
        "force_open": False,
        "log": tmp_path / "contact.jsonl",
        "latest": tmp_path / "latest.json",
        "output": tmp_path / "recovery.json",
        "print_result": False,
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_recover_opens_app_when_window_missing(monkeypatch, tmp_path) -> None:
    probes = [
        {"probe": {"process_running": True, "window_count": 0}},
        {"probe": {"process_running": True, "window_count": 1}},
    ]
    opened = []

    monkeypatch.setattr(recover_desktop_codex_app.probe_desktop_codex_app, "run", lambda _args: probes.pop(0))
    monkeypatch.setattr(recover_desktop_codex_app, "open_app", lambda app_name: opened.append(app_name) or {"returncode": 0})

    result = recover_desktop_codex_app.recover(args(tmp_path))

    assert opened == ["Codex"]
    assert result["opened"] is True
    assert result["recovered"] is True


def test_recover_skips_open_when_window_present(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        recover_desktop_codex_app.probe_desktop_codex_app,
        "run",
        lambda _args: {"probe": {"process_running": True, "window_count": 1}},
    )
    monkeypatch.setattr(recover_desktop_codex_app, "open_app", lambda app_name: (_ for _ in ()).throw(AssertionError(app_name)))

    result = recover_desktop_codex_app.recover(args(tmp_path))

    assert result["opened"] is False
    assert result["recovered"] is True


def test_script_help_runs_as_direct_entrypoint() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/recover_desktop_codex_app.py", "--help"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 0
    assert "Recover the macOS Codex desktop app window" in result.stdout
