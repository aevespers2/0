from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.emit_bridge_signal import collect_bridge_signal, write_signal
from scripts import recover_desktop_codex_app
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


def skipped_desktop_contact() -> dict[str, Any]:
    return {
        "schema": "codex_desktop_app_recovery.v1",
        "skipped": True,
        "reason": "desktop contact refresh disabled",
    }


def refresh_desktop_contact(args: argparse.Namespace, authoritative_head: str) -> dict[str, Any]:
    if not args.refresh_desktop_contact:
        return skipped_desktop_contact()
    recovery_args = argparse.Namespace(
        app_name=args.desktop_app_name,
        dispatch=args.dispatch_root / "desktop" / "dispatch.json",
        authoritative_head=authoritative_head,
        wait=args.desktop_recovery_wait,
        force_open=args.force_desktop_open,
        log=args.contact_log,
        latest=args.contact_latest,
        output=args.desktop_recovery_output,
        print_result=False,
    )
    result = recover_desktop_codex_app.recover(recovery_args)
    args.desktop_recovery_output.parent.mkdir(parents=True, exist_ok=True)
    args.desktop_recovery_output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


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
    desktop_contact = refresh_desktop_contact(args, authoritative_head)

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
        "desktop_contact": desktop_contact,
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
    parser.add_argument("--desktop-app-name", default="Codex")
    parser.add_argument("--desktop-recovery-wait", type=float, default=2.0)
    parser.add_argument("--force-desktop-open", action="store_true")
    parser.add_argument("--no-desktop-contact", action="store_false", dest="refresh_desktop_contact")
    parser.set_defaults(refresh_desktop_contact=True)
    parser.add_argument("--contact-log", type=Path, default=Path("reports/federation_contact_log.jsonl"))
    parser.add_argument("--contact-latest", type=Path, default=Path("reports/federation_contact_latest.json"))
    parser.add_argument("--desktop-recovery-output", type=Path, default=Path("reports/desktop_codex_recovery_latest.json"))
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
