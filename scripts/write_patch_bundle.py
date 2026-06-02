from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from write_federation_message import build_message, output_path, write_message


def git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def build_patch_text(repo: Path, base: str | None) -> str:
    args = ["diff"]
    if base:
        args.append(base)
    patch = git(args, repo)
    if not patch.strip():
        raise ValueError("no diff available to export")
    return patch


def resolve_base(repo: Path, base: str, fallback_commit: str) -> str:
    if not base:
        return fallback_commit
    return git(["rev-parse", base], repo).strip()


def write_patch_file(patch_text: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(patch_text, encoding="utf-8")


def build_patch_message_args(args: argparse.Namespace, patch_path: Path) -> argparse.Namespace:
    base = resolve_base(args.repo, args.base, args.commit)
    return argparse.Namespace(
        agent=args.agent,
        type="patch_proposal",
        workstream=args.workstream,
        cwd=args.cwd,
        branch=args.branch,
        commit=args.commit,
        status_short=args.status_short,
        remote=args.remote,
        blocker=args.blocker,
        next_action=args.next_action,
        repo=args.repo_name,
        base=base,
        summary=args.summary,
        file=args.file,
        patch_path=str(patch_path),
    )


def write_patch_bundle(args: argparse.Namespace) -> dict[str, Any]:
    patch_name = args.name or f"{args.agent}-{utc_stamp()}.patch"
    patch_path = args.patch_dir / patch_name
    patch_text = build_patch_text(args.repo, args.base)
    if not patch_text.strip():
        raise ValueError("no diff available to export")
    write_patch_file(patch_text, patch_path)

    message_args = build_patch_message_args(args, patch_path)
    payload = build_message(message_args)
    message_path = output_path(args.agent, "patch_proposal", args.inbox, args.message_name)
    write_message(payload, message_path)

    return {
        "schema": "codex_patch_bundle.v1",
        "patch_path": str(patch_path),
        "message_path": str(message_path),
        "source": args.agent,
        "authority": payload["patch"]["authority"],
        "base": payload["patch"]["base"],
        "summary": payload["patch"]["summary"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a git diff and matching federation patch proposal.")
    parser.add_argument("--agent", default="safari_cloud", choices=("safari_cloud", "desktop_app", "mobile", "chatgpt_bridge"))
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Local repository path to diff.")
    parser.add_argument("--repo-name", default="aevespers2/0", help="Repository identifier in the patch proposal.")
    parser.add_argument("--base", default="", help="Base commit for git diff. Defaults to unstaged/staged working diff.")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--file", action="append", default=[])
    parser.add_argument("--cwd", default="")
    parser.add_argument("--branch", default="")
    parser.add_argument("--commit", required=True)
    parser.add_argument("--status-short", action="append", default=[])
    parser.add_argument("--remote", default="")
    parser.add_argument("--blocker", default="")
    parser.add_argument("--next-action", default="await local_cli review")
    parser.add_argument("--workstream", default="Autonomous VNext")
    parser.add_argument("--patch-dir", type=Path, default=Path("patches/inbox"))
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--name", help="Patch filename.")
    parser.add_argument("--message-name", help="Patch proposal message filename.")
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = write_patch_bundle(args)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))


if __name__ == "__main__":
    main()
