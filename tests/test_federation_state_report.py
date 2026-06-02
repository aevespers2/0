from __future__ import annotations

from scripts.write_federation_state_report import build_state_report, write_report


def test_build_state_report_combines_subreports(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        "scripts.write_federation_state_report.evaluate_kernel",
        lambda inbox, authoritative_head: {
            "authoritative_writer": "local_cli",
            "patch_errors": {},
            "assessment": {"synchronized": True, "blocked_surfaces": (), "missing_surfaces": ()},
        },
    )
    monkeypatch.setattr(
        "scripts.write_federation_state_report.verify_public_mirrors",
        lambda manifest, repo: {"synchronized": True},
    )
    monkeypatch.setattr(
        "scripts.write_federation_state_report.verify_patch_inbox",
        lambda inbox, repo, authoritative_head: {"valid": True},
    )

    report = build_state_report(tmp_path, tmp_path / "FederationInbox", tmp_path / "public_mirrors.json", "abc123")

    assert report["schema"] == "codex_federation_state_report.v1"
    assert report["authoritative_writer"] == "local_cli"
    assert report["ready_for_remote_write"] is True


def test_state_report_blocks_remote_write_when_surface_blocked(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        "scripts.write_federation_state_report.evaluate_kernel",
        lambda inbox, authoritative_head: {
            "authoritative_writer": "local_cli",
            "patch_errors": {},
            "assessment": {"blocked_surfaces": ("desktop_app",), "missing_surfaces": ()},
        },
    )
    monkeypatch.setattr(
        "scripts.write_federation_state_report.verify_public_mirrors",
        lambda manifest, repo: {"synchronized": True},
    )
    monkeypatch.setattr(
        "scripts.write_federation_state_report.verify_patch_inbox",
        lambda inbox, repo, authoritative_head: {"valid": True},
    )

    report = build_state_report(tmp_path, tmp_path / "FederationInbox", tmp_path / "public_mirrors.json", "abc123")

    assert report["ready_for_remote_write"] is False


def test_state_report_blocks_remote_write_when_patch_verification_fails(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        "scripts.write_federation_state_report.evaluate_kernel",
        lambda inbox, authoritative_head: {
            "authoritative_writer": "local_cli",
            "patch_errors": {},
            "assessment": {"blocked_surfaces": (), "missing_surfaces": ()},
        },
    )
    monkeypatch.setattr(
        "scripts.write_federation_state_report.verify_public_mirrors",
        lambda manifest, repo: {"synchronized": True},
    )
    monkeypatch.setattr(
        "scripts.write_federation_state_report.verify_patch_inbox",
        lambda inbox, repo, authoritative_head: {"valid": False},
    )

    report = build_state_report(tmp_path, tmp_path / "FederationInbox", tmp_path / "public_mirrors.json", "abc123")

    assert report["ready_for_remote_write"] is False


def test_write_report_creates_parent_directory(tmp_path) -> None:
    output = tmp_path / "reports" / "state.json"

    write_report({"schema": "example"}, output)

    assert output.read_text(encoding="utf-8").strip()
