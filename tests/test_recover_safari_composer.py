from __future__ import annotations

import argparse

from scripts import recover_safari_composer


def args(tmp_path, **overrides):
    defaults = {
        "wait": 0,
        "force_reload": False,
        "output": tmp_path / "reports" / "recovery.json",
        "print_result": False,
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_recover_reloads_when_composer_missing(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(script):
        calls.append(script)
        if "location.reload" in script:
            return {"reloaded": True}
        if len(calls) == 1:
            return {"composer_found": False}
        return {"composer_found": True}

    monkeypatch.setattr(recover_safari_composer, "run_osascript", fake_run)

    result = recover_safari_composer.recover(args(tmp_path))

    assert result["reloaded"] is True
    assert result["recovered"] is True
    assert len(calls) == 3


def test_recover_skips_reload_when_composer_present(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        recover_safari_composer,
        "run_osascript",
        lambda script: {"composer_found": True},
    )

    result = recover_safari_composer.recover(args(tmp_path))

    assert result["reloaded"] is False
    assert result["recovered"] is True
