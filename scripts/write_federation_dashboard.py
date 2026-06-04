from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.verify_public_mirrors import verify_manifest


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def git_head(repo: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def contact_surfaces(contact_report: dict[str, Any]) -> dict[str, str]:
    return {
        str(item.get("surface", "")): str(item.get("actionable_status") or item.get("status", ""))
        for item in contact_report.get("surfaces", ())
        if item.get("surface")
    }


def effective_readiness_blockers(
    state_report: dict[str, Any], mirror_report: dict[str, Any]
) -> tuple[str, ...]:
    blockers = tuple(str(item) for item in state_report.get("readiness_blockers", ()))
    if mirror_report.get("synchronized") is True:
        blockers = tuple(item for item in blockers if item != "public mirrors out of sync")
    return blockers


def build_dashboard(
    state_report: dict[str, Any],
    relay_summary: dict[str, Any],
    contact_report: dict[str, Any],
    mirror_report: dict[str, Any],
    authoritative_head: str,
) -> dict[str, Any]:
    required_packets = tuple(relay_summary.get("required_packets", ()))
    readiness_blockers = effective_readiness_blockers(state_report, mirror_report)
    return {
        "schema": "codex_federation_dashboard.v1",
        "authoritative_head": authoritative_head,
        "ready_for_remote_write": bool(state_report.get("ready_for_remote_write", False)),
        "readiness_blockers": readiness_blockers,
        "mirrors_synchronized": bool(mirror_report.get("synchronized", False)),
        "contact_evidence_fresh": bool(contact_report.get("all_contacts_fresh", False)),
        "contact_surfaces": contact_surfaces(contact_report),
        "relay_target": relay_summary.get("dispatch_agent", ""),
        "relay_status": relay_summary.get("latest_contact_status", ""),
        "required_packets": required_packets,
        "next_action": relay_summary.get("next_action", ""),
    }


def load_or_verify_mirrors(path: Path, repo: Path, manifest: Path, refresh: bool) -> dict[str, Any]:
    if refresh or not path.exists():
        return verify_manifest(manifest, repo)
    return load_json(path)


def write_dashboard(payload: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a compact Codex federation dashboard.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--authoritative-head", default="")
    parser.add_argument("--state-report", type=Path, default=Path("reports/federation_state_report.json"))
    parser.add_argument("--relay-summary", type=Path, default=Path("reports/federation_relay_summary.json"))
    parser.add_argument("--contact-report", type=Path, default=Path("reports/federation_contact_report.json"))
    parser.add_argument("--mirror-report", type=Path, default=Path("reports/public_mirror_verification.json"))
    parser.add_argument("--mirror-manifest", type=Path, default=Path("public_mirrors.json"))
    parser.add_argument("--refresh-mirrors", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("reports/federation_dashboard.json"))
    parser.add_argument("--print", action="store_true", dest="print_dashboard")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    head = args.authoritative_head or git_head(args.repo)
    dashboard = build_dashboard(
        load_json(args.state_report),
        load_json(args.relay_summary),
        load_json(args.contact_report),
        load_or_verify_mirrors(args.mirror_report, args.repo, args.mirror_manifest, args.refresh_mirrors),
        head,
    )
    write_dashboard(dashboard, args.output)
    if args.print_dashboard:
        print(json.dumps(dashboard, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
