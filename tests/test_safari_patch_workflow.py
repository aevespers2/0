from __future__ import annotations

import argparse
import json

import pytest

from scripts import safari_patch_workflow


def _args(tmp_path, **overrides):
    defaults = {
        "repo": tmp_path,
        "repo_name": "aevespers2/0",
        "base": "",
        "summary": "propose helper updates",
        "file": ["README.md"],
        "inbox": tmp_path / "FederationInbox",
        "patch_dir": tmp_path / "patches" / "inbox",
        "name": None,
        "message_name": None,
        "branch": "",
        "commit": "",
        "authoritative_head": "",
        "fallback_branch": "work",
        "next_action": "await local_cli review",
        "allow_direct_push": False,
        "enforce_verification": False,
        "pretty": False,
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def _snapshot() -> dict[str, str | list[str]]:
    return {
        "cwd": "/workspace/0",
        "branch": "work",
        "commit": "abc123",
        "status_short": ["## work", " M scripts/agent.py"],
        "remote": "origin\thttps://example.com/repo.git (fetch)",
    }


def test_safari_workflow_writes_status_and_status_only_blocker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(safari_patch_workflow, "_snapshot", lambda repo: _snapshot())
    monkeypatch.setattr(
        safari_patch_workflow,
        "write_patch_bundle",
        lambda args: {
            "schema": "codex_patch_bundle.v1",
            "patch_path": "patches/inbox/proposal.patch",
            "message_path": "FederationInbox/safari/proposal.json",
            "source": "safari_cloud",
            "authority": "local_cli",
            "base": "abc123",
            "summary": "propose helper updates",
        },
    )
    monkeypatch.setattr(
        safari_patch_workflow,
        "verify_inbox",
        lambda inbox, repo, authoritative_head: {
            "schema": "codex_patch_proposal_verification.v1",
            "authoritative_head": authoritative_head,
            "proposal_count": 1,
            "valid": True,
            "verifications": (),
        },
    )

    result = safari_patch_workflow.run_workflow(_args(tmp_path))

    status_file = tmp_path / "FederationInbox" / "safari" / "status.json"
    assert status_file.exists()
    status = json.loads(status_file.read_text(encoding="utf-8"))
    assert status["agent"] == "safari_cloud"
    assert status["blocker"] == "safari_patch_only"
    assert status["patch_bundle_path"] == "patches/inbox/proposal.patch"
    assert result["verification"]["valid"] is True
    assert result["patch_bundle"]["authority"] == "local_cli"


def test_safari_workflow_can_allow_direct_push_blocker_override(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(safari_patch_workflow, "_snapshot", lambda repo: _snapshot())
    monkeypatch.setattr(
        safari_patch_workflow,
        "write_patch_bundle",
        lambda args: {
            "schema": "codex_patch_bundle.v1",
            "patch_path": "patches/inbox/proposal.patch",
            "message_path": "FederationInbox/safari/proposal.json",
            "source": "safari_cloud",
            "authority": "local_cli",
            "base": "abc123",
            "summary": "propose helper updates",
        },
    )
    monkeypatch.setattr(
        safari_patch_workflow,
        "verify_inbox",
        lambda inbox, repo, authoritative_head: {
            "schema": "codex_patch_proposal_verification.v1",
            "authoritative_head": authoritative_head,
            "proposal_count": 1,
            "valid": True,
            "verifications": (),
        },
    )

    result = safari_patch_workflow.run_workflow(_args(tmp_path, allow_direct_push=True))

    status = json.loads((tmp_path / "FederationInbox" / "safari" / "status.json").read_text(encoding="utf-8"))
    assert status["agent"] == "safari_cloud"
    assert status["blocker"] == ""


def test_safari_workflow_enforce_verification_raises_on_failure(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(safari_patch_workflow, "_snapshot", lambda repo: _snapshot())
    monkeypatch.setattr(
        safari_patch_workflow,
        "write_patch_bundle",
        lambda args: {
            "schema": "codex_patch_bundle.v1",
            "patch_path": "patches/inbox/proposal.patch",
            "message_path": "FederationInbox/safari/proposal.json",
            "source": "safari_cloud",
            "authority": "local_cli",
            "base": "abc123",
            "summary": "propose helper updates",
        },
    )
    monkeypatch.setattr(
        safari_patch_workflow,
        "verify_inbox",
        lambda inbox, repo, authoritative_head: {
            "schema": "codex_patch_proposal_verification.v1",
            "authoritative_head": authoritative_head,
            "proposal_count": 1,
            "valid": False,
            "verifications": (),
        },
    )

    with pytest.raises(SystemExit):
        safari_patch_workflow.run_workflow(_args(tmp_path, enforce_verification=True))
