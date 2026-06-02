from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.write_federation_state_report import build_state_report
from scripts.verify_public_mirrors import load_manifest


def collect_bridge_signal(
    repo: Path,
    inbox: Path,
    mirror_manifest: Path,
    authoritative_head: str,
) -> dict:
    report = build_state_report(repo, inbox, mirror_manifest, authoritative_head)
    kernel = report["kernel"]
    assessment = kernel["assessment"]
    manifest = load_manifest(mirror_manifest)
    return {
        "schema": "codex_bridge_signal.v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repo": str(repo.resolve()),
        "authoritative_head": authoritative_head,
        "remote_targets": [mirror.get("web_url", mirror["url"]) for mirror in manifest["mirrors"]],
        "ready_for_remote_write": report["ready_for_remote_write"],
        "readiness_blockers": report["readiness_blockers"],
        "required_packets": [
            packet["agent"]
            for packet in report.get("next_required_packets", ())
            if packet["priority"] == "required"
        ],
        "synchronized": assessment["synchronized"],
        "blocked_surfaces": list(assessment["blocked_surfaces"]),
        "missing_surfaces": list(assessment["missing_surfaces"]),
        "stale_surfaces": list(assessment["stale_surfaces"]),
        "patches_valid": report["patch_proposals"]["valid"],
        "patches_verified_count": report["patch_proposals"]["proposal_count"],
        "kernel_authoritative_writer": report["authoritative_writer"],
        "kernel_message_count": kernel["message_count"],
        "public_mirror_synchronized": report["public_mirrors"]["synchronized"],
    }


def write_signal(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit non-blocking bridge-facing federation signal.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--mirror-manifest", type=Path, default=Path("public_mirrors.json"))
    parser.add_argument("--authoritative-head", required=True)
    parser.add_argument("--output", type=Path, default=Path("reports/federation_bridge_signal.json"))
    parser.add_argument("--print", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = collect_bridge_signal(args.repo, args.inbox, args.mirror_manifest, args.authoritative_head)
    write_signal(args.output, payload)
    if args.print:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
