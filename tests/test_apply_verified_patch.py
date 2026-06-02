from __future__ import annotations

import json
import subprocess

import pytest

from scripts.apply_verified_patch import apply_verified_patch, require_clean_worktree, select_proposal
from scripts import apply_verified_patch as apply_cli


def write_patch_message(root, patch_path: str, source: str = "safari_cloud") -> None:
    directory = root / "safari"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "patch.json").write_text(
        json.dumps(
            {
                "schema": "codex_federation_message.v1",
                "agent": source,
                "type": "patch_proposal",
                "workstream": "Autonomous VNext",
                "cwd": "/workspace/0",
                "branch": "work",
                "commit": "abc123",
                "patch": {
                    "schema": "codex_patch_proposal.v1",
                    "source": source,
                    "repo": "aevespers2/0",
                    "base": "abc123",
                    "type": "git_patch",
                    "summary": "propose docs",
                    "files": ["README.md"],
                    "patch_path": patch_path,
                    "authority": "local_cli",
                },
            }
        ),
        encoding="utf-8",
    )


def test_select_proposal_by_source_and_path(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    write_patch_message(inbox, "patches/proposal.patch")

    proposal = select_proposal(inbox, "patches/proposal.patch", "safari_cloud")

    assert proposal.source == "safari_cloud"


def test_select_proposal_requires_match(tmp_path) -> None:
    with pytest.raises(ValueError, match="no matching"):
        select_proposal(tmp_path / "FederationInbox", None, None)


def test_require_clean_worktree_rejects_dirty_status(monkeypatch, tmp_path) -> None:
    def fake_run(args, cwd, check=True, text=True, stdout=None, stderr=None):
        return subprocess.CompletedProcess(args=args, returncode=0, stdout=" M README.md\n", stderr="")

    monkeypatch.setattr("scripts.apply_verified_patch.subprocess.run", fake_run)

    with pytest.raises(ValueError, match="clean"):
        require_clean_worktree(tmp_path)


def test_apply_verified_patch_check_only(monkeypatch, tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    patch = tmp_path / "patches" / "proposal.patch"
    patch.parent.mkdir(parents=True)
    patch.write_text("diff --git a/README.md b/README.md\n", encoding="utf-8")
    write_patch_message(inbox, "patches/proposal.patch")

    def fake_run(args, cwd, check=False, text=True, stdout=None, stderr=None):
        if args[:3] == ["git", "rev-parse", "abc123"]:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="abc123\n", stderr="")
        if args[:3] == ["git", "apply", "--check"]:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="", stderr="")
        raise AssertionError(args)

    monkeypatch.setattr("scripts.verify_patch_proposals.subprocess.run", fake_run)

    result = apply_verified_patch(inbox, tmp_path, "abc123", apply=False)

    assert result["valid"]
    assert not result["applied"]


def test_apply_verified_patch_returns_verification_errors(monkeypatch, tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    write_patch_message(inbox, "patches/missing.patch")

    result = apply_verified_patch(inbox, tmp_path, "abc123")

    assert not result["valid"]
    assert not result["applied"]


def test_apply_verified_patch_cli_reports_no_matching_proposal(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "apply_verified_patch.py",
            "--inbox",
            "/tmp/no-inbox",
            "--authoritative-head",
            "abc123",
        ],
    )

    with pytest.raises(SystemExit):
        apply_cli.main()

    assert "no matching patch proposal" in capsys.readouterr().out
