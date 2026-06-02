from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from autonomous_vnext.federation_kernel import collect_patch_proposals, read_inbox
from scripts.verify_patch_proposals import verify_proposal


def git(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def require_clean_worktree(repo: Path) -> None:
    status = git(["status", "--porcelain"], repo).stdout.strip()
    if status:
        raise ValueError("working tree must be clean before applying a federation patch")


def select_proposal(inbox: Path, patch_path: str | None, source: str | None):
    proposals = collect_patch_proposals(read_inbox(inbox))
    if patch_path:
        proposals = tuple(proposal for proposal in proposals if proposal.patch_path == patch_path)
    if source:
        proposals = tuple(proposal for proposal in proposals if proposal.source == source)
    if not proposals:
        raise ValueError("no matching patch proposal")
    if len(proposals) > 1:
        raise ValueError("multiple matching patch proposals; specify --patch-path")
    return proposals[0]


def apply_verified_patch(
    inbox: Path,
    repo: Path,
    authoritative_head: str,
    patch_path: str | None = None,
    source: str | None = None,
    apply: bool = False,
) -> dict[str, object]:
    proposal = select_proposal(inbox, patch_path, source)
    verification = verify_proposal(proposal, repo, authoritative_head)
    if not verification.valid:
        return {
            "schema": "codex_verified_patch_apply.v1",
            "applied": False,
            "valid": False,
            "proposal": proposal.__dict__,
            "errors": verification.errors,
        }

    if not apply:
        return {
            "schema": "codex_verified_patch_apply.v1",
            "applied": False,
            "valid": True,
            "proposal": proposal.__dict__,
            "errors": (),
        }

    require_clean_worktree(repo)
    path = Path(proposal.patch_path)
    if not path.is_absolute():
        path = repo / path
    git(["apply", str(path)], repo)
    return {
        "schema": "codex_verified_patch_apply.v1",
        "applied": True,
        "valid": True,
        "proposal": proposal.__dict__,
        "errors": (),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify and optionally apply one federation patch proposal.")
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--authoritative-head", required=True)
    parser.add_argument("--patch-path")
    parser.add_argument("--source")
    parser.add_argument("--apply", action="store_true", help="Apply the patch after verification.")
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = apply_verified_patch(
            inbox=args.inbox,
            repo=args.repo,
            authoritative_head=args.authoritative_head,
            patch_path=args.patch_path,
            source=args.source,
            apply=args.apply,
        )
    except ValueError as error:
        result = {
            "schema": "codex_verified_patch_apply.v1",
            "applied": False,
            "valid": False,
            "proposal": None,
            "errors": (str(error),),
        }
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
