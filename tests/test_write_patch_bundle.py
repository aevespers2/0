from __future__ import annotations

import argparse
import json

import pytest

from scripts.write_patch_bundle import build_patch_message_args, write_patch_bundle


def args(tmp_path, **overrides):
    defaults = {
        "agent": "safari_cloud",
        "repo": tmp_path,
        "repo_name": "aevespers2/0",
        "base": "",
        "summary": "propose docs",
        "file": ["README.md"],
        "cwd": "/workspace/0",
        "branch": "work",
        "commit": "abc123",
        "status_short": [],
        "remote": "",
        "blocker": "no_remote",
        "next_action": "await local_cli review",
        "workstream": "Autonomous VNext",
        "patch_dir": tmp_path / "patches" / "inbox",
        "inbox": tmp_path / "FederationInbox",
        "name": "proposal.patch",
        "message_name": "proposal.json",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_build_patch_message_args_forces_patch_proposal(tmp_path) -> None:
    parsed = args(tmp_path)
    message_args = build_patch_message_args(parsed, tmp_path / "patches" / "proposal.patch")

    assert message_args.type == "patch_proposal"
    assert message_args.agent == "safari_cloud"
    assert message_args.patch_path.endswith("proposal.patch")


def test_write_patch_bundle_exports_patch_and_message(monkeypatch, tmp_path) -> None:
    def fake_patch_text(repo, base):
        return "diff --git a/README.md b/README.md\n+hello\n"

    monkeypatch.setattr("scripts.write_patch_bundle.build_patch_text", fake_patch_text)

    result = write_patch_bundle(args(tmp_path))
    patch_path = tmp_path / "patches" / "inbox" / "proposal.patch"
    message_path = tmp_path / "FederationInbox" / "safari" / "proposal.json"

    assert patch_path.exists()
    assert message_path.exists()
    payload = json.loads(message_path.read_text(encoding="utf-8"))
    assert payload["type"] == "patch_proposal"
    assert payload["patch"]["authority"] == "local_cli"
    assert result["authority"] == "local_cli"


def test_write_patch_bundle_rejects_empty_diff(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr("scripts.write_patch_bundle.build_patch_text", lambda repo, base: "")

    with pytest.raises(ValueError, match="no diff"):
        write_patch_bundle(args(tmp_path))
