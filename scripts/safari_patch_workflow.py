from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import write_federation_message
from scripts.verify_patch_proposals import verify_inbox
from scripts.write_patch_bundle import write_patch_bundle


def run_workflow(args: argparse.Namespace) -> dict[str, str | bool | dict]:
    repo = args.repo.resolve()
    state = _snapshot(repo)
    branch = args.branch or state["branch"] or args.fallback_branch
    commit = args.commit or state["commit"]

    bundle_args = argparse.Namespace(
        agent="safari_cloud",
        repo=repo,
        repo_name=args.repo_name,
        base=args.base,
        summary=args.summary,
        file=args.file,
        cwd=str(repo),
        branch=branch,
        commit=commit,
        status_short=state["status_short"],
        remote=state["remote"],
        blocker="",
        next_action=args.next_action,
        workstream="Autonomous VNext",
        patch_dir=args.patch_dir,
        inbox=args.inbox,
        name=args.name,
        message_name=args.message_name,
    )
    patch_bundle = write_patch_bundle(bundle_args)

    if args.authoritative_head:
        verification_target = args.authoritative_head
    else:
        verification_target = commit

    verification = verify_inbox(args.inbox, repo, verification_target)
    blocker = ""
    constraints = () if args.allow_direct_push else ("patch_only_no_direct_push",)
    status_next_action = "Patch-only production cycle active. " + (
        "Do not push directly; local_cli applies patch from "
        f"{patch_bundle['message_path']}."
    )

    status = write_federation_message.build_message(
        argparse.Namespace(
            agent="safari_cloud",
            type="status",
            workstream="Autonomous VNext",
            cwd=state["cwd"],
            branch=branch,
            commit=commit,
            status_short=state["status_short"],
            remote=state["remote"],
            blocker=blocker,
            next_action=f"{status_next_action} Verification valid={verification['valid']}.",
            capability=(),
            constraint=constraints,
            repo=args.repo_name,
            base="",
            summary="",
            file=(),
            patch_path="",
        )
    )
    status.update(
        {
            "patch_bundle_path": patch_bundle["patch_path"],
            "patch_message_path": patch_bundle["message_path"],
        }
    )
    status_file = args.inbox / "safari" / "status.json"
    write_federation_message.write_message(status, status_file)

    if args.enforce_verification and not verification["valid"]:
        raise SystemExit(1)

    return {
        "patch_bundle": patch_bundle,
        "verification": verification,
        "status": status,
        "status_file": str(status_file),
    }


def _snapshot(repo: Path) -> dict[str, str | list[str]]:
    root = Path(_git(["rev-parse", "--show-toplevel"], repo))
    return {
        "cwd": str(root),
        "branch": _git(["branch", "--show-current"], root),
        "commit": _git(["rev-parse", "HEAD"], root),
        "status_short": _git(["status", "--branch", "--short"], root).splitlines(),
        "remote": _git(["remote", "-v"], root),
    }


def _git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safari production workflow: export a patch bundle and emit a status packet."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--repo-name", default="aevespers2/0")
    parser.add_argument("--base", default="")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--file", action="append", default=[], help="Touched files.")
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--patch-dir", type=Path, default=Path("FederationPatches/inbox"))
    parser.add_argument("--name", help="Patch filename.")
    parser.add_argument("--message-name", help="Patch message filename.")
    parser.add_argument("--branch", default="")
    parser.add_argument("--commit", default="")
    parser.add_argument(
        "--authoritative-head",
        default="",
        help="Optional authoritative head for patch verification.",
    )
    parser.add_argument("--fallback-branch", default="work")
    parser.add_argument("--next-action", default="export patch proposal")
    parser.add_argument("--allow-direct-push", action="store_true", help="Allow nonstandard direct push mode.")
    parser.add_argument("--enforce-verification", action="store_true", help="Fail if verification check fails.")
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_workflow(args)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))


if __name__ == "__main__":
    main()
