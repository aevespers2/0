from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.write_federation_state_report import build_state_report


SURFACE_TO_DIR = {
    "local_cli": "local",
    "safari_cloud": "safari",
    "desktop_app": "desktop",
    "mobile": "mobile",
    "chatgpt_bridge": "bridge",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def command_for(agent: str, expected_path: str) -> str:
    if agent == "local_cli":
        return f"python3 scripts/write_local_federation_status.py --output {expected_path}"
    if agent == "desktop_app":
        return f"python3 scripts/write_desktop_federation_status.py --output {expected_path}"
    if agent == "mobile":
        return f"python3 scripts/write_mobile_federation_status.py --output {expected_path}"
    if agent == "safari_cloud":
        return (
            "python3 scripts/write_federation_message.py --agent safari_cloud --type status "
            f"--commit \"$(git rev-parse HEAD)\" --inbox FederationInbox --name {Path(expected_path).name}"
        )
    if agent == "chatgpt_bridge":
        return (
            "python3 scripts/write_federation_message.py --agent chatgpt_bridge --type routine_checkin "
            f"--commit \"$(git rev-parse HEAD)\" --inbox FederationInbox --name {Path(expected_path).name}"
        )
    return f"write required packet to {expected_path}"


def build_dispatch(
    repo: Path,
    inbox: Path,
    mirror_manifest: Path,
    authoritative_head: str,
) -> dict[str, Any]:
    report = build_state_report(repo, inbox, mirror_manifest, authoritative_head)
    dispatches = []
    for packet in report.get("next_required_packets", ()):
        agent = str(packet["agent"])
        expected_path = str(packet["expected_path"])
        dispatches.append(
            {
                "agent": agent,
                "surface_dir": SURFACE_TO_DIR.get(agent, agent),
                "packet_type": packet["packet_type"],
                "priority": packet["priority"],
                "details": packet["details"],
                "expected_path": expected_path,
                "command": command_for(agent, expected_path),
            }
        )

    return {
        "schema": "codex_federation_dispatch.v1",
        "generated_at": utc_now(),
        "authoritative_head": authoritative_head,
        "ready_for_remote_write": report["ready_for_remote_write"],
        "readiness_blockers": report["readiness_blockers"],
        "dispatch_count": len(dispatches),
        "dispatches": dispatches,
    }


def write_dispatch(payload: dict[str, Any], output_root: Path) -> dict[str, str]:
    output_root.mkdir(parents=True, exist_ok=True)
    aggregate = output_root / "dispatch.json"
    aggregate.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written = {"aggregate": str(aggregate)}

    for dispatch in payload["dispatches"]:
        surface_dir = output_root / dispatch["surface_dir"]
        surface_dir.mkdir(parents=True, exist_ok=True)
        path = surface_dir / "dispatch.json"
        surface_payload = {
            "schema": "codex_federation_surface_dispatch.v1",
            "generated_at": payload["generated_at"],
            "authoritative_head": payload["authoritative_head"],
            "dispatch": dispatch,
        }
        path.write_text(json.dumps(surface_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written[dispatch["agent"]] = str(path)

    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write per-surface federation dispatch packets.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--mirror-manifest", type=Path, default=Path("public_mirrors.json"))
    parser.add_argument("--authoritative-head", required=True)
    parser.add_argument("--output-root", type=Path, default=Path("FederationDispatch"))
    parser.add_argument("--print", action="store_true", dest="print_payload")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_dispatch(args.repo, args.inbox, args.mirror_manifest, args.authoritative_head)
    written = write_dispatch(payload, args.output_root)
    if args.print_payload:
        print(json.dumps({"dispatch": payload, "written": written}, indent=2, sort_keys=True))
    else:
        print(written["aggregate"])


if __name__ == "__main__":
    main()
