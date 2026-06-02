from __future__ import annotations

import argparse

from scripts import run_federation_routine


def _args(tmp_path, **overrides):
    defaults = {
        "repo": tmp_path,
        "inbox": tmp_path / "FederationInbox",
        "mirror_manifest": tmp_path / "public_mirrors.json",
        "authoritative_head": "abc123",
        "safe_root": str(tmp_path),
        "state_report": tmp_path / "reports" / "federation_state_report.json",
        "bridge_signal": tmp_path / "reports" / "federation_bridge_signal.json",
        "dispatch_root": tmp_path / "FederationDispatch",
        "print_payload": False,
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_run_routine_refreshes_local_surfaces_and_dispatch(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        run_federation_routine,
        "build_local_status",
        lambda repo: {"schema": "codex_federation_message.v1", "agent": "local_cli"},
    )
    monkeypatch.setattr(
        run_federation_routine,
        "build_desktop_status",
        lambda repo, safe_root: {"schema": "codex_federation_message.v1", "agent": "desktop_app"},
    )
    monkeypatch.setattr(
        run_federation_routine,
        "build_mobile_status",
        lambda repo: {"schema": "codex_federation_message.v1", "agent": "mobile"},
    )
    monkeypatch.setattr(
        run_federation_routine,
        "build_state_report",
        lambda repo, inbox, manifest, head: {
            "ready_for_remote_write": False,
            "readiness_blockers": ("required federation packets pending",),
        },
    )
    monkeypatch.setattr(
        run_federation_routine,
        "collect_bridge_signal",
        lambda repo, inbox, manifest, head: {"schema": "codex_bridge_signal.v1"},
    )
    monkeypatch.setattr(
        run_federation_routine,
        "build_dispatch",
        lambda repo, inbox, manifest, head: {
            "schema": "codex_federation_dispatch.v1",
            "generated_at": "2026-06-02T00:00:00Z",
            "authoritative_head": head,
            "ready_for_remote_write": False,
            "readiness_blockers": ("required federation packets pending",),
            "dispatch_count": 0,
            "dispatches": [],
        },
    )

    result = run_federation_routine.run_routine(_args(tmp_path))

    assert result["schema"] == "codex_federation_routine_result.v1"
    assert result["authoritative_head"] == "abc123"
    assert (tmp_path / "FederationInbox" / "local" / "status.json").exists()
    assert (tmp_path / "FederationInbox" / "desktop" / "status.json").exists()
    assert (tmp_path / "FederationInbox" / "mobile" / "status.json").exists()
    assert (tmp_path / "FederationDispatch" / "dispatch.json").exists()
