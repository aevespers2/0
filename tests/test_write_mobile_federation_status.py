from __future__ import annotations

from scripts.write_mobile_federation_status import build_status


def test_mobile_status_builds_expected_shape(tmp_path, monkeypatch) -> None:
    def fake_git(args, cwd):
        if args == ["rev-parse", "--show-toplevel"]:
            return "/Users/ALISTAIRE/aevespers2-0"
        if args == ["branch", "--show-current"]:
            return "main"
        if args == ["rev-parse", "HEAD"]:
            return "abc123"
        if args == ["status", "--branch", "--short"]:
            return "## main\n M file.txt\n"
        if args == ["remote", "-v"]:
            return "origin\thttps://example.com/repo.git (fetch)\n"
        raise AssertionError(f"unexpected git command: {args}")

    monkeypatch.setattr("scripts.write_mobile_federation_status.git", fake_git)

    payload = build_status(tmp_path)

    assert payload["agent"] == "mobile"
    assert payload["type"] == "status"
    assert payload["branch"] == "main"
    assert payload["commit"] == "abc123"
    assert payload["status_short"] == ["## main", " M file.txt"]
    assert payload["next_action"].startswith("Collect user-facing priorities")
