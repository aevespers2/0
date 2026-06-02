from __future__ import annotations

import json
from pathlib import Path

from scripts.prune_federation_runtime import run_prune


def write_message(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def base_status(agent: str, commit: str = "abc123", blocker: str = "") -> dict:
    return {
        "schema": "codex_federation_message.v1",
        "agent": agent,
        "type": "status",
        "commit": commit,
        "blocker": blocker,
    }


def base_patch(agent: str, base: str = "abc123") -> dict:
    return {
        "schema": "codex_federation_message.v1",
        "agent": agent,
        "type": "patch_proposal",
        "patch": {
            "schema": "codex_patch_proposal.v1",
            "base": base,
        },
    }


def test_prune_dry_run_identifies_stale_packets(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    write_message(inbox / "safari" / "status.json", base_status("safari_cloud", commit="old"))
    write_message(inbox / "desktop" / "status.json", base_status("desktop_app", commit="old", blocker="wrong_checkout"))
    write_message(inbox / "local" / "status.json", base_status("local_cli", commit="old"))

    report = run_prune(
        inbox=inbox,
        authoritative_head="abc123",
        mode_all=False,
        include_local=False,
        surfaces_arg="",
        delete=False,
        archive_dir=tmp_path / "arch",
    )

    assert report["matched"] == 2
    paths = {item["path"] for item in report["targets"]}
    assert str(inbox / "safari" / "status.json") in paths
    assert str(inbox / "desktop" / "status.json") in paths
    assert all("local" not in path for path in paths)


def test_prune_deletes_and_archives_selected_packets(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    write_message(inbox / "safari" / "status.json", base_status("safari_cloud", commit="old"))
    write_message(inbox / "safari" / "patch.json", base_patch("safari_cloud", base="old"))

    report = run_prune(
        inbox=inbox,
        authoritative_head="abc123",
        mode_all=False,
        include_local=False,
        surfaces_arg="",
        delete=True,
        archive_dir=tmp_path / "arch",
    )

    assert report["matched"] == 2
    assert report["archived"] == 2
    assert not (inbox / "safari" / "status.json").exists()
    assert not (inbox / "safari" / "patch.json").exists()
    assert list((tmp_path / "arch" / "safari").glob("*.json"))


def test_prune_all_mode_can_include_local_without_head(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    write_message(inbox / "local" / "status.json", base_status("local_cli", commit="old"))
    write_message(inbox / "bridge" / "status.json", base_status("chatgpt_bridge", commit="old"))

    report = run_prune(
        inbox=inbox,
        authoritative_head="",
        mode_all=True,
        include_local=True,
        surfaces_arg="",
        delete=False,
        archive_dir=tmp_path / "arch",
    )

    assert report["matched"] == 2
    paths = {item["path"] for item in report["targets"]}
    assert str(inbox / "local" / "status.json") in paths
    assert str(inbox / "bridge" / "status.json") in paths
