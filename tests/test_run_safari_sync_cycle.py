from __future__ import annotations

import argparse
import json

from scripts import run_safari_sync_cycle


def args(tmp_path, **overrides):
    defaults = {
        "repo": tmp_path,
        "watch_timeout": 1,
        "watch_interval": 1,
        "send": False,
        "write_status": False,
        "recover_composer": True,
        "nudge_sendability": True,
        "safari_target": tmp_path / "FederationRelay" / "safari_target.json",
        "safari_url": "",
        "no_focus_safari_target": False,
        "no_open_safari_target": False,
        "output": tmp_path / "reports" / "cycle.json",
        "print_result": False,
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def result(payload: dict, returncode: int = 0) -> dict:
    return {"command": [], "returncode": returncode, "stdout": json.dumps(payload), "stderr": ""}


def test_cycle_runs_watch_extract_and_summary(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("watch_safari_dispatch_send.py" in item for item in command):
            return result({"contact_event": {"status": "blocked", "detail": "stop answering"}})
        if any("extract_safari_ack.py" in item for item in command):
            return result({"candidate": None, "written_path": ""})
        if any("write_federation_relay_summary.py" in item for item in command):
            return result(
                {
                    "next_action": "Continue watching safari_cloud sendability/acknowledgment.",
                    "ready_for_remote_write": False,
                    "required_packets": ["safari_cloud"],
                    "missing_surfaces": ["safari_cloud"],
                }
            )
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": True})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"ready_for_remote_write": False, "next_action": "Continue watching."})
        if any("write_safari_operator_handoff.py" in item for item in command):
            return result({"status": "blocked_send_disabled"})
        return result({})

    monkeypatch.setattr(run_safari_sync_cycle, "run_command", fake_run)

    summary = run_safari_sync_cycle.run_cycle(args(tmp_path))

    assert summary["commands_succeeded"] is True
    assert summary["watch_status"] == "blocked"
    assert summary["ack_candidate_found"] is False
    assert summary["required_packets"] == ["safari_cloud"]
    assert summary["contact_evidence_fresh"] is True
    assert summary["dashboard_next_action"] == "Continue watching."
    assert any("extract_safari_ack.py" in item for command in calls for item in command)
    assert any("write_federation_contact_report.py" in item for command in calls for item in command)
    assert any("write_federation_dashboard.py" in item for command in calls for item in command)
    assert any("focus_safari_target.py" in item for command in calls for item in command)
    assert any("write_safari_operator_handoff.py" in item for command in calls for item in command)
    assert any("reports/safari_operator_handoff_latest.json" in item for command in calls for item in command)
    assert any("reports/safari_operator_handoff_latest.txt" in item for command in calls for item in command)
    assert summary["operator_handoff"]["returncode"] == 0


def test_cycle_passes_send_and_write_status_flags(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("watch_safari_dispatch_send.py" in item for item in command):
            return result({"contact_event": {"status": "sent", "detail": "sent"}})
        if any("extract_safari_ack.py" in item for item in command):
            return result({"candidate": {"agent": "safari_cloud"}, "written_path": "FederationInbox/safari/status.json"})
        if any("write_federation_relay_summary.py" in item for item in command):
            return result({"next_action": "No required federation packets are pending.", "ready_for_remote_write": True})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": True})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"ready_for_remote_write": True, "next_action": "No required federation packets are pending."})
        if any("write_safari_operator_handoff.py" in item for item in command):
            return result({"status": "ready"})
        return result({})

    monkeypatch.setattr(run_safari_sync_cycle, "run_command", fake_run)

    summary = run_safari_sync_cycle.run_cycle(args(tmp_path, send=True, write_status=True))

    assert summary["send_requested"] is True
    assert summary["write_status_requested"] is True
    assert summary["ack_candidate_found"] is True
    assert summary["ack_written_path"] == "FederationInbox/safari/status.json"
    assert summary["ready_for_remote_write"] is True
    assert any("--send" in command for command in calls)
    assert any("--write-status" in command for command in calls)
    assert any("--refresh-mirrors" in command for command in calls)
    assert any("write_safari_operator_handoff.py" in item for command in calls for item in command)
    assert any("focus_safari_target.py" in item for command in calls for item in command)


def test_cycle_refuses_to_stage_stale_dispatch_when_routine_fails(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("run_federation_routine.py" in item for item in command):
            return result({}, returncode=1)
        raise AssertionError(f"unexpected command after routine failure: {command}")

    monkeypatch.setattr(run_safari_sync_cycle, "run_command", fake_run)

    summary = run_safari_sync_cycle.run_cycle(args(tmp_path))

    assert summary["commands_succeeded"] is False
    assert summary["stage_skipped"] is True
    assert "refusing to stage stale dispatch" in summary["skip_reason"]
    assert summary["ready_for_remote_write"] is False
    assert len(calls) == 1


def test_cycle_refuses_to_stage_when_safari_target_focus_fails(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("run_federation_routine.py" in item for item in command):
            return result({})
        if any("focus_safari_target.py" in item for item in command):
            return result({"focused": False, "reason": "target_tab_not_found"}, returncode=1)
        if any("write_federation_relay_summary.py" in item for item in command):
            return result({"next_action": "Restore Safari target.", "ready_for_remote_write": False})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": False})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"ready_for_remote_write": False, "next_action": "Restore Safari target."})
        if any("write_safari_operator_handoff.py" in item for item in command):
            return result({"status": "target_focus_failed"})
        raise AssertionError(command)

    monkeypatch.setattr(run_safari_sync_cycle, "run_command", fake_run)

    summary = run_safari_sync_cycle.run_cycle(args(tmp_path))

    assert summary["commands_succeeded"] is False
    assert summary["target_focus_failed"] is True
    assert "unverified tab" in summary["skip_reason"]
    assert not any("stage_safari_dispatch.py" in item for command in calls for item in command)
    assert not any("watch_safari_dispatch_send.py" in item for command in calls for item in command)


def test_cycle_passes_safari_target_options(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("watch_safari_dispatch_send.py" in item for item in command):
            return result({"contact_event": {"status": "blocked", "detail": "disabled"}})
        if any("nudge_safari_sendability.py" in item for item in command):
            return result({"sendable": False})
        if any("extract_safari_ack.py" in item for item in command):
            return result({"candidate": None, "written_path": ""})
        if any("write_federation_relay_summary.py" in item for item in command):
            return result({"next_action": "Still disabled.", "ready_for_remote_write": False})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": True})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"ready_for_remote_write": False, "next_action": "Still disabled."})
        if any("write_safari_operator_handoff.py" in item for item in command):
            return result({"status": "blocked_send_disabled"})
        return result({})

    monkeypatch.setattr(run_safari_sync_cycle, "run_command", fake_run)

    summary = run_safari_sync_cycle.run_cycle(
        args(
            tmp_path,
            safari_url="https://chatgpt.com/c/example",
            no_open_safari_target=True,
        )
    )

    assert summary["commands_succeeded"] is True
    focus_call = next(command for command in calls if any("focus_safari_target.py" in item for item in command))
    assert "--url" in focus_call
    assert "https://chatgpt.com/c/example" in focus_call
    assert "--no-open-if-missing" in focus_call


def test_cycle_refuses_to_watch_when_stage_semantically_fails(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("run_federation_routine.py" in item for item in command):
            return result({})
        if any("focus_safari_target.py" in item for item in command):
            return result({"focused": True})
        if any("stage_safari_dispatch.py" in item for item in command):
            return result({"contact_event": {"status": "failed", "detail": "composer_not_found"}})
        if any("write_federation_relay_summary.py" in item for item in command):
            return result({"next_action": "Restore Safari composer.", "ready_for_remote_write": False})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": True})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"ready_for_remote_write": False, "next_action": "Restore Safari composer."})
        if any("write_safari_operator_handoff.py" in item for item in command):
            return result({"status": "staging_failed"})
        raise AssertionError(f"unexpected command after stage failure: {command}")

    monkeypatch.setattr(run_safari_sync_cycle, "run_command", fake_run)

    summary = run_safari_sync_cycle.run_cycle(args(tmp_path, recover_composer=False))

    assert summary["commands_succeeded"] is False
    assert summary["stage_failed"] is True
    assert "refusing to watch" in summary["skip_reason"]
    assert summary["dashboard_next_action"] == "Restore Safari composer."
    assert summary["operator_handoff"]["returncode"] == 0
    assert not any("watch_safari_dispatch_send.py" in item for command in calls for item in command)
    assert not any("extract_safari_ack.py" in item for command in calls for item in command)


def test_cycle_recovers_composer_once_after_stage_failure(monkeypatch, tmp_path) -> None:
    calls = []
    stage_calls = 0

    def fake_run(command, cwd):
        nonlocal stage_calls
        calls.append(command)
        if any("run_federation_routine.py" in item for item in command):
            return result({})
        if any("focus_safari_target.py" in item for item in command):
            return result({"focused": True})
        if any("stage_safari_dispatch.py" in item for item in command):
            stage_calls += 1
            if stage_calls == 1:
                return result({"contact_event": {"status": "failed", "detail": "composer_not_found"}})
            return result({"contact_event": {"status": "staged", "detail": "composer restored"}})
        if any("recover_safari_composer.py" in item for item in command):
            return result({"recovered": True})
        if any("watch_safari_dispatch_send.py" in item for item in command):
            return result({"contact_event": {"status": "blocked", "detail": "disabled"}})
        if any("nudge_safari_sendability.py" in item for item in command):
            return result({"sendable": False})
        if any("extract_safari_ack.py" in item for item in command):
            return result({"candidate": None, "written_path": ""})
        if any("write_federation_relay_summary.py" in item for item in command):
            return result({"next_action": "Continue.", "ready_for_remote_write": False})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": True})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"ready_for_remote_write": False, "next_action": "Continue."})
        if any("write_safari_operator_handoff.py" in item for item in command):
            return result({"status": "blocked_send_disabled"})
        raise AssertionError(command)

    monkeypatch.setattr(run_safari_sync_cycle, "run_command", fake_run)

    summary = run_safari_sync_cycle.run_cycle(args(tmp_path))

    assert stage_calls == 2
    assert summary["commands_succeeded"] is True
    assert summary["watch_status"] == "blocked"
    assert any("recover_safari_composer.py" in item for command in calls for item in command)
    assert any("write_safari_operator_handoff.py" in item for command in calls for item in command)


def test_cycle_runs_sendability_nudge_after_blocked_watch(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_run(command, cwd):
        calls.append(command)
        if any("watch_safari_dispatch_send.py" in item for item in command):
            return result({"contact_event": {"status": "blocked", "detail": "disabled"}})
        if any("nudge_safari_sendability.py" in item for item in command):
            return result({"sendable": False})
        if any("extract_safari_ack.py" in item for item in command):
            return result({"candidate": None, "written_path": ""})
        if any("write_federation_relay_summary.py" in item for item in command):
            return result({"next_action": "Still disabled.", "ready_for_remote_write": False})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": True})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"ready_for_remote_write": False, "next_action": "Still disabled."})
        if any("write_safari_operator_handoff.py" in item for item in command):
            return result({"status": "blocked_send_disabled"})
        return result({})

    monkeypatch.setattr(run_safari_sync_cycle, "run_command", fake_run)

    summary = run_safari_sync_cycle.run_cycle(args(tmp_path))

    assert summary["watch_status"] == "blocked"
    assert summary["sendability_nudge"]["returncode"] == 0
    assert summary["operator_handoff"]["returncode"] == 0
    assert sum(any("watch_safari_dispatch_send.py" in item for item in command) for command in calls) == 1


def test_cycle_rewatches_when_sendability_nudge_recovers(monkeypatch, tmp_path) -> None:
    calls = []
    watch_statuses = ["blocked", "staged"]

    def fake_run(command, cwd):
        calls.append(command)
        if any("watch_safari_dispatch_send.py" in item for item in command):
            return result({"contact_event": {"status": watch_statuses.pop(0), "detail": "watch"}})
        if any("nudge_safari_sendability.py" in item for item in command):
            return result({"sendable": True})
        if any("extract_safari_ack.py" in item for item in command):
            return result({"candidate": None, "written_path": ""})
        if any("write_federation_relay_summary.py" in item for item in command):
            return result({"next_action": "Send staged.", "ready_for_remote_write": False})
        if any("write_federation_contact_report.py" in item for item in command):
            return result({"all_contacts_fresh": True})
        if any("write_federation_dashboard.py" in item for item in command):
            return result({"ready_for_remote_write": False, "next_action": "Send staged."})
        if any("write_safari_operator_handoff.py" in item for item in command):
            return result({"status": "staged"})
        return result({})

    monkeypatch.setattr(run_safari_sync_cycle, "run_command", fake_run)

    summary = run_safari_sync_cycle.run_cycle(args(tmp_path))

    assert summary["watch_status"] == "staged"
    assert summary["operator_handoff"]["returncode"] == 0
    assert sum(any("watch_safari_dispatch_send.py" in item for item in command) for command in calls) == 2
