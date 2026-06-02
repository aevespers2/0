from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from autonomous_vnext.federation_kernel import PatchProposal, collect_patch_proposals, read_inbox


@dataclass(frozen=True)
class PatchVerification:
    source: str
    patch_path: str
    base: str
    valid: bool
    errors: tuple[str, ...]


def git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def resolve_commit(repo: Path, ref: str) -> str:
    return git(["rev-parse", ref], repo)


def check_patch_applies(repo: Path, patch_path: Path) -> tuple[str, ...]:
    result = subprocess.run(
        ["git", "apply", "--check", str(patch_path)],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode == 0:
        return ()
    detail = (result.stderr or result.stdout or "git apply --check failed").strip()
    return (detail,)


def verify_proposal(proposal: PatchProposal, repo: Path, authoritative_head: str) -> PatchVerification:
    errors = list(proposal.validate())
    patch_path = Path(proposal.patch_path)
    if not patch_path.is_absolute():
        patch_path = repo / patch_path

    if not patch_path.exists():
        errors.append(f"patch file not found: {proposal.patch_path}")
    if proposal.base != authoritative_head:
        try:
            resolved = resolve_commit(repo, proposal.base)
        except subprocess.CalledProcessError:
            errors.append(f"patch base is not a known commit: {proposal.base}")
        else:
            if resolved != authoritative_head:
                errors.append(f"patch base {proposal.base} does not match authoritative head {authoritative_head}")

    if patch_path.exists():
        errors.extend(check_patch_applies(repo, patch_path))

    return PatchVerification(
        source=proposal.source,
        patch_path=proposal.patch_path,
        base=proposal.base,
        valid=not errors,
        errors=tuple(errors),
    )


def verify_inbox(inbox: Path, repo: Path, authoritative_head: str) -> dict[str, object]:
    messages = read_inbox(inbox)
    proposals = collect_patch_proposals(messages)
    verifications = tuple(verify_proposal(proposal, repo, authoritative_head) for proposal in proposals)
    return {
        "schema": "codex_patch_proposal_verification.v1",
        "authoritative_head": authoritative_head,
        "proposal_count": len(proposals),
        "valid": all(item.valid for item in verifications),
        "verifications": tuple(asdict(item) for item in verifications),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify federation patch proposals without applying them.")
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--authoritative-head", required=True)
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = verify_inbox(args.inbox, args.repo, args.authoritative_head)
    print(json.dumps(report, indent=2 if args.pretty else None, sort_keys=True))
    if not report["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
