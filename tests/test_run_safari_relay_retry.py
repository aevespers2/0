from __future__ import annotations

import argparse
import json

from scripts import run_safari_relay_retry


def args(tmp_path, **overrides):
    defaults = {
        "repo": tmp_path,
        "attempts": 3,
        "interval": 0,
        "watch_timeout": 1,
        "watch_interval": 1,
        "send": False,
        "output": tmp_path / "reports" / "retry.json",
        "print_result": False,
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def result(payload: dict, returncode: int = 0) -> dict:
    return {"command": [], "returncode": returncode, "stdout": json.dumps(payload), "stderr": ""}


def test_retry_stops_when_sent(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("watch_safari_dispatch_send.py" in item for item in command):
            return result({"contact_event": {"status": "sent", "detail": "sent"}, "send_result": {"clicked": True}})
        return result({})

    monkeypatch.setattr(run_safari_relay_retry, "run_command", fake_run)

    summary = run_safari_relay_retry.run_retry(args(tmp_path, attempts=3, send=True))

    assert summary["attempt_count"] == 1
    assert summary["final_status"] == "sent"
    assert summary["send_requested"] is True
    assert any("--send" in command for command in calls)


def test_retry_continues_until_attempts_exhausted(monkeypatch, tmp_path) -> None:
    def fake_run(command, cwd):
        if any("watch_safari_dispatch_send.py" in item for item in command):
            return result({"contact_event": {"status": "blocked", "detail": "stop answering"}})
        return result({})

    monkeypatch.setattr(run_safari_relay_retry, "run_command", fake_run)
    monkeypatch.setattr(run_safari_relay_retry.time, "sleep", lambda seconds: None)

    summary = run_safari_relay_retry.run_retry(args(tmp_path, attempts=2))

    assert summary["attempt_count"] == 2
    assert summary["final_status"] == "blocked"


def test_parse_json_stdout_handles_bad_output() -> None:
    assert run_safari_relay_retry.parse_json_stdout({"returncode": 1, "stdout": ""}) == {}
    assert run_safari_relay_retry.parse_json_stdout({"returncode": 0, "stdout": "not-json"}) == {}
