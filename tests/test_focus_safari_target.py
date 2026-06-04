from __future__ import annotations

import argparse
import json
import subprocess

import pytest

from scripts.focus_safari_target import focus_script, focus_target, load_target


def test_load_target_rejects_wrong_schema(tmp_path) -> None:
    target = tmp_path / "target.json"
    target.write_text(json.dumps({"schema": "wrong"}), encoding="utf-8")

    with pytest.raises(ValueError, match="unsupported"):
        load_target(target)


def test_focus_script_embeds_target_and_open_policy() -> None:
    script = focus_script("https://chatgpt.com/c/example", False)

    assert json.dumps("https://chatgpt.com/c/example") in script
    assert "openIfMissing" in script
    assert "currentTab.url = targetUrl" in script
    assert "target_tab_not_found" in script


def test_focus_target_uses_manifest_url(monkeypatch, tmp_path) -> None:
    target = tmp_path / "target.json"
    target.write_text(
        json.dumps(
            {
                "schema": "codex_safari_target.v1",
                "target_url": "https://chatgpt.com/c/example",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "scripts.focus_safari_target.run_osascript",
        lambda script: {"focused": True, "opened": False, "matched": True, "url": "https://chatgpt.com/c/example"},
    )

    result = focus_target(
        argparse.Namespace(
            target=target,
            url="",
            open_if_missing=True,
        )
    )

    assert result["target_url"] == "https://chatgpt.com/c/example"
    assert result["focused"] is True


def test_focus_target_reports_missing_url(tmp_path) -> None:
    result = focus_target(
        argparse.Namespace(
            target=tmp_path / "missing.json",
            url="",
            open_if_missing=True,
        )
    )

    assert result["focused"] is False
    assert result["reason"] == "target_url_missing"


def test_focus_target_reports_osascript_failure(monkeypatch, tmp_path) -> None:
    target = tmp_path / "target.json"
    target.write_text(
        json.dumps(
            {
                "schema": "codex_safari_target.v1",
                "target_url": "https://chatgpt.com/c/example",
            }
        ),
        encoding="utf-8",
    )

    def fail(script):
        raise subprocess.CalledProcessError(1, ["osascript"], stderr="bad safari")

    monkeypatch.setattr("scripts.focus_safari_target.run_osascript", fail)

    result = focus_target(
        argparse.Namespace(
            target=target,
            url="",
            open_if_missing=True,
        )
    )

    assert result["focused"] is False
    assert result["reason"] == "osascript_failed"
    assert result["error"] == "bad safari"
