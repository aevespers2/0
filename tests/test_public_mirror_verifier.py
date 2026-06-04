from __future__ import annotations

import json
import subprocess

import pytest

from scripts.verify_public_mirrors import load_manifest, verify_manifest


def write_manifest(tmp_path, branch: str = "main"):
    manifest = tmp_path / "public_mirrors.json"
    manifest.write_text(
        json.dumps(
            {
                "schema": "public_mirrors.v1",
                "branch": branch,
                "mirrors": [
                    {"name": "origin", "url": "git@example:one.git"},
                    {"name": "mirror", "url": "git@example:two.git"},
                ],
            }
        ),
        encoding="utf-8",
    )
    return manifest


def test_load_manifest_rejects_wrong_schema(tmp_path) -> None:
    manifest = tmp_path / "bad.json"
    manifest.write_text(json.dumps({"schema": "wrong"}), encoding="utf-8")

    with pytest.raises(ValueError, match="unsupported"):
        load_manifest(manifest)


def test_verify_manifest_reports_synchronized_heads(monkeypatch, tmp_path) -> None:
    manifest = write_manifest(tmp_path)

    def fake_run(args, cwd, check, text, stdout, stderr):
        if args[:3] == ["git", "rev-parse", "HEAD"]:
            output = "abc123\n"
        elif args[:2] == ["git", "ls-remote"]:
            output = "abc123\trefs/heads/main\n"
        else:
            raise AssertionError(args)
        return subprocess.CompletedProcess(args=args, returncode=0, stdout=output, stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = verify_manifest(manifest, tmp_path)

    assert result["synchronized"]
    assert result["expected_head"] == "abc123"
    assert len(result["mirrors"]) == 2


def test_verify_manifest_reports_mismatched_heads(monkeypatch, tmp_path) -> None:
    manifest = write_manifest(tmp_path)
    calls = []

    def fake_run(args, cwd, check, text, stdout, stderr):
        calls.append(args)
        if args[:3] == ["git", "rev-parse", "HEAD"]:
            output = "abc123\n"
        elif args[:2] == ["git", "ls-remote"]:
            output = ("abc123" if len(calls) == 2 else "def456") + "\trefs/heads/main\n"
        else:
            raise AssertionError(args)
        return subprocess.CompletedProcess(args=args, returncode=0, stdout=output, stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = verify_manifest(manifest, tmp_path)

    assert not result["synchronized"]
    assert result["mismatches"][0]["name"] == "mirror"


def test_verify_manifest_retries_transient_remote_failure(monkeypatch, tmp_path) -> None:
    manifest = write_manifest(tmp_path)
    remote_calls = 0

    def fake_run(args, cwd, check, text, stdout, stderr):
        nonlocal remote_calls
        if args[:3] == ["git", "rev-parse", "HEAD"]:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="abc123\n", stderr="")
        if args[:2] == ["git", "ls-remote"]:
            remote_calls += 1
            if remote_calls == 1:
                raise subprocess.CalledProcessError(128, args, stderr="temporary ssh failure")
            return subprocess.CompletedProcess(
                args=args,
                returncode=0,
                stdout="abc123\trefs/heads/main\n",
                stderr="",
            )
        raise AssertionError(args)

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = verify_manifest(manifest, tmp_path, attempts=2, retry_delay=0)

    assert result["synchronized"] is True
    assert result["errors"] == []
    assert remote_calls == 3


def test_verify_manifest_reports_persistent_remote_failure(monkeypatch, tmp_path) -> None:
    manifest = write_manifest(tmp_path)

    def fake_run(args, cwd, check, text, stdout, stderr):
        if args[:3] == ["git", "rev-parse", "HEAD"]:
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="abc123\n", stderr="")
        if args[:2] == ["git", "ls-remote"]:
            raise subprocess.CalledProcessError(128, args, stderr="ssh failure")
        raise AssertionError(args)

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = verify_manifest(manifest, tmp_path, attempts=2, retry_delay=0)

    assert result["synchronized"] is False
    assert result["mismatches"] == []
    assert len(result["errors"]) == 2
    assert result["errors"][0]["name"] == "origin"
