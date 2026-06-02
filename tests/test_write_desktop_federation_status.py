from __future__ import annotations

from scripts.write_desktop_federation_status import build_status


def test_desktop_status_marks_no_blocker_on_safe_root(tmp_path, monkeypatch) -> None:
    def fake_git(args, cwd):
        if args == ["rev-parse", "--show-toplevel"]:
            return "/Users/ALISTAIRE/aevespers2-0"
        if args == ["branch", "--show-current"]:
            return "main"
        if args == ["rev-parse", "HEAD"]:
            return "abc123"
        if args == ["status", "--branch", "--short"]:
            return "## main...origin/main\n M file.txt"
        if args == ["remote", "-v"]:
            return "origin\thttps://example.com/repo.git (fetch)\n"
        raise AssertionError(f"unexpected git command: {args}")

    monkeypatch.setattr("scripts.write_desktop_federation_status.git", fake_git)

    payload = build_status(tmp_path, "/Users/ALISTAIRE/aevespers2-0")

    assert payload["blocker"] == ""
    assert payload["agent"] == "desktop_app"
    assert payload["cwd"] == "/Users/ALISTAIRE/aevespers2-0"
    assert payload["safe_repo_root"] == "/Users/ALISTAIRE/aevespers2-0"
    assert payload["status_short"] == ["## main...origin/main", " M file.txt"]


def test_desktop_status_blocks_wrong_checkout(tmp_path, monkeypatch) -> None:
    def fake_git(args, cwd):
        if args == ["rev-parse", "--show-toplevel"]:
            return "/Users/ALISTAIRE/Documents"
        if args == ["branch", "--show-current"]:
            return "main"
        if args == ["rev-parse", "HEAD"]:
            return "abc123"
        if args == ["status", "--branch", "--short"]:
            return ""
        if args == ["remote", "-v"]:
            return ""
        raise AssertionError(f"unexpected git command: {args}")

    monkeypatch.setattr("scripts.write_desktop_federation_status.git", fake_git)

    payload = build_status(tmp_path, "/Users/ALISTAIRE/aevespers2-0")

    assert payload["blocker"] == "wrong_checkout"
    assert payload["blocker"] == "wrong_checkout"
    assert "switch to safe checkout" in payload["next_action"]
