from __future__ import annotations

import argparse
import json

from scripts import run_federation_post_push_refresh


def args(tmp_path, **overrides):
    defaults = {
        "repo": tmp_path,
        "mirror_attempts": 3,
        "mirror_retry_delay": 0,
        "no_desktop_contact": False,
        "no_safari_contact": False,
        "safari_watch_timeout": 3,
        "safari_watch_interval": 1,
        "output": tmp_path / "reports" / "post_push.json",
        "print_result": False,
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def result(payload: dict, returncode: int = 0) -> dict:
    return {"command": [], "returncode": returncode, "stdout": json.dumps(payload), "stderr": ""}


def test_post_push_refresh_runs_runtime_refresh_sequence(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("verify_public_mirrors.py" in item for item in command):
            return result({"expected_head": "abc123", "synchronized": True, "errors": []})
        if any("run_federation_routine.py" in item for item in command):
            return result({"authoritative_head": "abc123"})
        if any("run_safari_sync_cycle.py" in item for item in command):
            return result({"commands_succeeded": True})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": True})
        if any("write_federation_dashboard.py" in item for item in command):
            return result(
                {
                    "authoritative_head": "abc123",
                    "ready_for_remote_write": False,
                    "readiness_blockers": ["required federation packets pending"],
                    "next_action": "Collect Safari status.",
                }
            )
        raise AssertionError(command)

    monkeypatch.setattr(run_federation_post_push_refresh, "run_command", fake_run)

    summary = run_federation_post_push_refresh.run_refresh(args(tmp_path))

    assert summary["commands_succeeded"] is True
    assert summary["authoritative_head"] == "abc123"
    assert summary["mirrors_synchronized"] is True
    assert summary["contact_evidence_fresh"] is True
    assert summary["readiness_blockers"] == ["required federation packets pending"]
    assert summary["next_action"] == "Collect Safari status."
    assert any("--attempts" in command for command in calls)
    assert any("--refresh-mirrors" in command for command in calls)
    assert any("run_safari_sync_cycle.py" in item for command in calls for item in command)
    assert any("--watch-timeout" in command for command in calls)


def test_post_push_refresh_can_skip_desktop_contact(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("verify_public_mirrors.py" in item for item in command):
            return result({"expected_head": "abc123", "synchronized": True, "errors": []})
        if any("run_federation_routine.py" in item for item in command):
            return result({"authoritative_head": "abc123"})
        if any("run_safari_sync_cycle.py" in item for item in command):
            return result({"commands_succeeded": True})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": True})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"authoritative_head": "abc123", "readiness_blockers": []})
        raise AssertionError(command)

    monkeypatch.setattr(run_federation_post_push_refresh, "run_command", fake_run)

    summary = run_federation_post_push_refresh.run_refresh(args(tmp_path, no_desktop_contact=True))

    assert summary["commands_succeeded"] is True
    assert any("--no-desktop-contact" in command for command in calls)


def test_post_push_refresh_can_skip_safari_contact(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("verify_public_mirrors.py" in item for item in command):
            return result({"expected_head": "abc123", "synchronized": True, "errors": []})
        if any("run_federation_routine.py" in item for item in command):
            return result({"authoritative_head": "abc123"})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": True})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"authoritative_head": "abc123", "readiness_blockers": []})
        raise AssertionError(command)

    monkeypatch.setattr(run_federation_post_push_refresh, "run_command", fake_run)

    summary = run_federation_post_push_refresh.run_refresh(args(tmp_path, no_safari_contact=True))

    assert summary["commands_succeeded"] is True
    assert summary["safari_sync"]["skipped"] is True
    assert not any("run_safari_sync_cycle.py" in item for command in calls for item in command)


def test_post_push_refresh_preserves_failed_command_status(monkeypatch, tmp_path) -> None:
    def fake_run(command, cwd):
        if any("verify_public_mirrors.py" in item for item in command):
            return result({"expected_head": "abc123", "synchronized": False, "errors": [{"name": "origin"}]}, 1)
        if any("run_federation_routine.py" in item for item in command):
            return result({})
        if any("run_safari_sync_cycle.py" in item for item in command):
            return result({})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": False})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"authoritative_head": "abc123", "readiness_blockers": ["public mirrors out of sync"]})
        raise AssertionError(command)

    monkeypatch.setattr(run_federation_post_push_refresh, "run_command", fake_run)

    summary = run_federation_post_push_refresh.run_refresh(args(tmp_path))

    assert summary["commands_succeeded"] is False
    assert summary["mirrors_synchronized"] is False
    assert summary["mirror_errors"] == [{"name": "origin"}]
