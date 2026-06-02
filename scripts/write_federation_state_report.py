from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from autonomous_vnext.federation_kernel import evaluate_kernel
from scripts.verify_patch_proposals import verify_inbox as verify_patch_inbox
from scripts.verify_public_mirrors import verify_manifest as verify_public_mirrors


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_state_report(
    repo: Path,
    inbox: Path,
    mirror_manifest: Path,
    authoritative_head: str,
) -> dict[str, Any]:
    kernel = evaluate_kernel(inbox, authoritative_head)
    mirrors = verify_public_mirrors(mirror_manifest, repo)
    patches = verify_patch_inbox(inbox, repo, authoritative_head)
    assessment = kernel["assessment"]
    next_required_packets = kernel.get("next_required_packets", ())
    return {
        "schema": "codex_federation_state_report.v1",
        "generated_at": utc_now(),
        "authoritative_head": authoritative_head,
        "authoritative_writer": kernel["authoritative_writer"],
        "kernel": kernel,
        "public_mirrors": mirrors,
        "patch_proposals": patches,
        "next_required_packets": next_required_packets,
        "ready_for_remote_write": bool(
            mirrors["synchronized"]
            and patches["valid"]
            and not kernel["patch_errors"]
            and not assessment["blocked_surfaces"]
            and not assessment["missing_surfaces"]
            and not next_required_packets
        ),
        "readiness_blockers": tuple(
            reason
            for reason in (
                None if mirrors["synchronized"] else "public mirrors out of sync",
                None if patches["valid"] else "unverified/invalid patch proposals",
                None if not kernel["patch_errors"] else "patch proposal validation errors",
                None
                if (not assessment["blocked_surfaces"] and not assessment["missing_surfaces"])
                else "missing/blocked federation surfaces",
                None if not next_required_packets else "required federation packets pending",
            )
            if reason is not None
        ),
    }


def write_report(report: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a durable Codex federation state report.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--mirror-manifest", type=Path, default=Path("public_mirrors.json"))
    parser.add_argument("--authoritative-head", required=True)
    parser.add_argument("--output", type=Path, default=Path("reports/federation_state_report.json"))
    parser.add_argument("--print", action="store_true", dest="print_report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_state_report(args.repo, args.inbox, args.mirror_manifest, args.authoritative_head)
    write_report(report, args.output)
    if args.print_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(args.output)
    if not report["ready_for_remote_write"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
