from __future__ import annotations

from types import SimpleNamespace

from scripts.enforce_federation_remote_write import (
    enforce_remote_write_readiness,
)
from scripts import enforce_federation_remote_write as gate_script


def _write_args(tmp_path, ready=True, blockers=None):
    return SimpleNamespace(
        repo=tmp_path,
        inbox=tmp_path / "FederationInbox",
        mirror_manifest=tmp_path / "public_mirrors.json",
        authoritative_head="abc123",
        output=tmp_path / "reports" / "federation_state_report.json",
        print_report=False,
    ), ready, blockers or ()


def test_gate_readiness_allows_remote_write_when_ready(monkeypatch, tmp_path) -> None:
    args, _, _ = _write_args(tmp_path)

    monkeypatch.setattr(
        gate_script,
        "build_state_report",
        lambda *a, **k: {
            "ready_for_remote_write": True,
            "readiness_blockers": (),
        },
    )
    monkeypatch.setattr(
        gate_script,
        "write_report",
        lambda report, output: None,
    )

    assert enforce_remote_write_readiness(args) == {
        "ready_for_remote_write": True,
        "readiness_blockers": (),
    }


def test_gate_refuses_remote_write_when_blocked(monkeypatch, tmp_path) -> None:
    args, _, blockers = _write_args(tmp_path, ready=False, blockers=("missing packets",))

    monkeypatch.setattr(
        gate_script,
        "build_state_report",
        lambda *a, **k: {
            "ready_for_remote_write": False,
            "readiness_blockers": blockers,
        },
    )
    monkeypatch.setattr(
        gate_script,
        "write_report",
        lambda report, output: None,
    )

    try:
        enforce_remote_write_readiness(args)
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("expected SystemExit")
