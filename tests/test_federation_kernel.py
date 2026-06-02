from __future__ import annotations

import json

from autonomous_vnext.federation_kernel import evaluate_kernel


def write_message(root, surface: str, name: str, payload: dict) -> None:
    directory = root / surface
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_text(json.dumps(payload), encoding="utf-8")


def base_message(agent: str, message_type: str = "status", head: str = "abc123") -> dict:
    return {
        "schema": "codex_federation_message.v1",
        "agent": agent,
        "type": message_type,
        "workstream": "Autonomous vNext",
        "cwd": "/repo",
        "branch": "main",
        "commit": head,
        "status_short": ["## main"],
        "remote": "git@example:repo.git",
        "blocker": "",
        "next_action": "report status",
    }


def test_kernel_reads_status_messages_and_assesses_sync(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    write_message(inbox, "local", "status.json", base_message("local_cli"))
    write_message(inbox, "safari", "status.json", base_message("safari_cloud"))
    write_message(inbox, "desktop", "status.json", base_message("desktop_app"))

    report = evaluate_kernel(inbox, authoritative_head="abc123")

    assert report["message_count"] == 3
    assert report["assessment"]["synchronized"] is True
    assert report["assessment"]["stale_surfaces"] == ()
    assert report["assessment"]["explicitly_blocked_surfaces"] == ()
    assert report["authoritative_writer"] == "local_cli"


def test_kernel_flags_desktop_until_pointed_at_safe_repo(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    desktop = base_message("desktop_app")
    desktop["cwd"] = "/Users/ALISTAIRE/Documents"
    desktop["blocker"] = "wrong_checkout"
    write_message(inbox, "local", "status.json", base_message("local_cli"))
    write_message(inbox, "desktop", "status.json", desktop)

    report = evaluate_kernel(inbox, authoritative_head="abc123")

    assert report["assessment"]["synchronized"] is False
    assert "desktop_app" in report["assessment"]["blocked_surfaces"]
    assert report["assessment"]["explicitly_blocked_surfaces"] == ("desktop_app",)
    assert report["assessment"]["stale_surfaces"] == ()


def test_kernel_reports_required_packets_for_stale_or_blocked_statuses(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    write_message(inbox, "local", "status.json", base_message("local_cli"))
    write_message(inbox, "safari", "status.json", base_message("safari_cloud", head="stale"))
    desktop = base_message("desktop_app")
    desktop["blocker"] = "wrong_checkout"
    write_message(inbox, "desktop", "status.json", desktop)

    report = evaluate_kernel(inbox, authoritative_head="abc123")

    required = tuple(packet["agent"] for packet in report["next_required_packets"])
    assert "safari_cloud" in required
    assert "desktop_app" in required
    assert any(packet["packet_type"] == "status_refresh" for packet in report["next_required_packets"])
    assert any(packet["packet_type"] == "status_unblock" for packet in report["next_required_packets"])


def test_kernel_accepts_safari_patch_with_local_cli_authority(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    message = base_message("safari_cloud", "patch_proposal")
    message["patch"] = {
        "schema": "codex_patch_proposal.v1",
        "source": "safari_cloud",
        "repo": "aevespers2/0",
        "base": "abc123",
        "type": "git_patch",
        "summary": "propose tests",
        "files": ["tests/test_example.py"],
        "patch_path": "patches/propose-tests.patch",
        "authority": "local_cli",
    }
    write_message(inbox, "safari", "patch.json", message)

    report = evaluate_kernel(inbox, authoritative_head="abc123")

    assert report["patch_proposals"][0]["source"] == "safari_cloud"
    assert report["patch_errors"] == {}


def test_kernel_rejects_patch_with_nonlocal_authority(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    message = base_message("safari_cloud", "patch_proposal")
    message["patch"] = {
        "schema": "codex_patch_proposal.v1",
        "source": "safari_cloud",
        "repo": "aevespers2/0",
        "base": "abc123",
        "type": "git_patch",
        "summary": "propose direct push",
        "files": [],
        "authority": "safari_cloud",
    }
    write_message(inbox, "safari", "patch.json", message)

    report = evaluate_kernel(inbox, authoritative_head="abc123")

    assert report["patch_errors"]["safari_cloud"] == ("patch authority must be local_cli",)
