from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.emit_bridge_signal import collect_bridge_signal, write_signal
from scripts.write_desktop_federation_status import build_status as build_desktop_status
from scripts.write_desktop_federation_status import write_status as write_desktop_status
from scripts.write_federation_dispatch import build_dispatch, write_dispatch
from scripts.write_federation_state_report import build_state_report, write_report
from scripts.write_local_federation_status import build_local_status, write_status as write_local_status
from scripts.write_mobile_federation_status import build_status as build_mobile_status
from scripts.write_mobile_federation_status import write_status as write_mobile_status


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


def run_routine(args: argparse.Namespace) -> dict[str, Any]:
    repo = args.repo.resolve()
    authoritative_head = args.authoritative_head or git(["rev-parse", "HEAD"], repo)

    local_path = args.inbox / "local" / "status.json"
    desktop_path = args.inbox / "desktop" / "status.json"
    mobile_path = args.inbox / "mobile" / "status.json"

    write_local_status(build_local_status(repo), local_path)
    write_desktop_status(build_desktop_status(repo, args.safe_root), desktop_path)
    write_mobile_status(build_mobile_status(repo), mobile_path)

    state_report = build_state_report(repo, args.inbox, args.mirror_manifest, authoritative_head)
    write_report(state_report, args.state_report)

    bridge_signal = collect_bridge_signal(repo, args.inbox, args.mirror_manifest, authoritative_head)
    write_signal(args.bridge_signal, bridge_signal)

    dispatch = build_dispatch(repo, args.inbox, args.mirror_manifest, authoritative_head)
    dispatch_paths = write_dispatch(dispatch, args.dispatch_root)

    return {
        "schema": "codex_federation_routine_result.v1",
        "authoritative_head": authoritative_head,
        "status_packets": {
            "local_cli": str(local_path),
            "desktop_app": str(desktop_path),
            "mobile": str(mobile_path),
        },
        "state_report": str(args.state_report),
        "bridge_signal": str(args.bridge_signal),
        "dispatch": dispatch_paths,
        "ready_for_remote_write": state_report["ready_for_remote_write"],
        "readiness_blockers": state_report["readiness_blockers"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local federation status/dispatch routine.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--mirror-manifest", type=Path, default=Path("public_mirrors.json"))
    parser.add_argument("--authoritative-head", default="")
    parser.add_argument("--safe-root", default="/Users/ALISTAIRE/aevespers2-0")
    parser.add_argument("--state-report", type=Path, default=Path("reports/federation_state_report.json"))
    parser.add_argument("--bridge-signal", type=Path, default=Path("reports/federation_bridge_signal.json"))
    parser.add_argument("--dispatch-root", type=Path, default=Path("FederationDispatch"))
    parser.add_argument("--print", action="store_true", dest="print_payload")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_routine(args)
    if args.print_payload:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.state_report)


if __name__ == "__main__":
    main()
