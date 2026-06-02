from __future__ import annotations

import json
import subprocess

from scripts.verify_patch_proposals import verify_inbox


def write_patch_message(root, patch_path: str, base: str = "abc123") -> None:
    directory = root / "safari"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "patch.json").write_text(
        json.dumps(
            {
                "schema": "codex_federation_message.v1",
                "agent": "safari_cloud",
                "type": "patch_proposal",
                "workstream": "Autonomous VNext",
                "cwd": "/workspace/0",
                "branch": "work",
                "commit": base,
                "patch": {
                    "schema": "codex_patch_proposal.v1",
                    "source": "safari_cloud",
                    "repo": "aevespers2/0",
                    "base": base,
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


def test_verify_inbox_reports_missing_patch_file(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    write_patch_message(inbox, "patches/missing.patch")

    report = verify_inbox(inbox, tmp_path, "abc123")

    assert not report["valid"]
    assert "patch file not found" in report["verifications"][0]["errors"][0]


def test_verify_inbox_checks_base_and_git_apply(monkeypatch, tmp_path) -> None:
    patch = tmp_path / "patches" / "proposal.patch"
    patch.parent.mkdir(parents=True)
    patch.write_text("diff --git a/README.md b/README.md\n", encoding="utf-8")
    inbox = tmp_path / "FederationInbox"
    write_patch_message(inbox, "patches/proposal.patch")

    def fake_run(args, cwd, check=False, text=True, stdout=None, stderr=None):
        if args[:3] == ["git", "rev-parse", "abc123"]:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="abc123\n", stderr="")
        if args[:3] == ["git", "apply", "--check"]:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="", stderr="")
        raise AssertionError(args)

    monkeypatch.setattr(subprocess, "run", fake_run)

    report = verify_inbox(inbox, tmp_path, "abc123")

    assert report["valid"]
    assert report["proposal_count"] == 1


def test_verify_inbox_rejects_stale_base(monkeypatch, tmp_path) -> None:
    patch = tmp_path / "patches" / "proposal.patch"
    patch.parent.mkdir(parents=True)
    patch.write_text("diff --git a/README.md b/README.md\n", encoding="utf-8")
    inbox = tmp_path / "FederationInbox"
    write_patch_message(inbox, "patches/proposal.patch", base="old")

    def fake_run(args, cwd, check=False, text=True, stdout=None, stderr=None):
        if args[:3] == ["git", "rev-parse", "old"]:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="old\n", stderr="")
        if args[:3] == ["git", "apply", "--check"]:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="", stderr="")
        raise AssertionError(args)

    monkeypatch.setattr(subprocess, "run", fake_run)

    report = verify_inbox(inbox, tmp_path, "abc123")

    assert not report["valid"]
    assert "does not match authoritative head" in report["verifications"][0]["errors"][0]
