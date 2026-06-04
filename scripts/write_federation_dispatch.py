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

PARALLEL_WORK_SCHEMA = "codex_parallel_work_allocation.v1"


def parallel_work_allocation(authoritative_head: str) -> dict[str, Any]:
    """Describe how federation surfaces can work concurrently without shared-write contention."""
    return {
        "schema": PARALLEL_WORK_SCHEMA,
        "authoritative_head": authoritative_head,
        "coordination_rule": (
            "Surfaces may execute bounded work in parallel, but local_cli remains "
            "the authoritative writer for commits, pushes, and final integration."
        ),
        "merge_rule": (
            "Non-local surfaces report status, evidence, and patch proposals. "
            "local_cli validates base commits, applies non-conflicting work, runs tests, "
            "and publishes the synchronized result."
        ),
        "contention_rule": (
            "If two surfaces need the same file or runtime resource, the dispatch owner "
            "is primary and the other surface becomes reviewer or patch proposer."
        ),
        "surfaces": {
            "local_cli": {
                "role": "authoritative_integrator",
                "may_execute": [
                    "repo writes",
                    "tests",
                    "local services",
                    "commits",
                    "approved pushes",
                ],
                "must_report": [
                    "status packet",
                    "validation results",
                    "files changed",
                    "merge decisions",
                ],
                "handoff_type": "direct_commit_or_status",
            },
            "safari_cloud": {
                "role": "patch_first_parallel_builder",
                "may_execute": [
                    "isolated implementation drafts",
                    "architecture review",
                    "diff generation",
                    "patch proposals",
                ],
                "must_report": [
                    "status packet",
                    "base commit",
                    "patch proposal",
                    "files touched",
                    "blockers",
                ],
                "handoff_type": "patch_proposal",
                "constraints": ["patch_only_no_direct_push"],
            },
            "desktop_app": {
                "role": "local_context_observer",
                "may_execute": [
                    "desktop UI observation",
                    "local context relay",
                    "safe checkout status",
                    "sidebar/mobile readiness checks",
                ],
                "must_report": [
                    "status packet",
                    "observed cwd",
                    "observed branch",
                    "observed commit",
                    "UI blockers",
                ],
                "handoff_type": "status_or_observation",
            },
            "mobile": {
                "role": "user_facing_followup",
                "may_execute": [
                    "routine check-ins",
                    "approval prompts",
                    "completion follow-up",
                    "escalation summaries",
                ],
                "must_report": [
                    "status packet",
                    "user priorities",
                    "approval state",
                    "blockers",
                ],
                "handoff_type": "routine_checkin",
            },
            "chatgpt_bridge": {
                "role": "planning_and_dispatch_coordinator",
                "may_execute": [
                    "task decomposition",
                    "parallel work allocation",
                    "status synthesis",
                    "bridge packet drafting",
                    "permission-scoped inspection",
                ],
                "must_report": [
                    "routine_checkin packet",
                    "coordination summary",
                    "recommended task split",
                    "known sandbox constraints",
                ],
                "handoff_type": "routine_checkin_or_status",
                "constraints": ["permission_scoped", "no_direct_push"],
            },
        },
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
            "--constraint patch_only_no_direct_push "
            f"--commit \"$(git rev-parse HEAD)\" --inbox FederationInbox --name {Path(expected_path).name}"
        )
    if agent == "chatgpt_bridge":
        return (
            "python3 scripts/write_federation_message.py --agent chatgpt_bridge --type routine_checkin "
            f"--commit \"$(git rev-parse HEAD)\" --inbox FederationInbox --name {Path(expected_path).name}"
        )
    return f"write required packet to {expected_path}"


def status_template_for(
    agent: str,
    packet_type: str,
    authoritative_head: str,
    expected_path: str,
) -> dict[str, Any]:
    surface_defaults = {
        "local_cli": {
            "cwd": "/Users/ALISTAIRE/aevespers2-0",
            "branch": "main",
            "blocker": "",
            "next_action": "Refresh local_cli status and continue authoritative implementation.",
        },
        "desktop_app": {
            "cwd": "/Users/ALISTAIRE/aevespers2-0",
            "branch": "main",
            "blocker": "",
            "next_action": "Refresh desktop_app status from the safe checkout only.",
        },
        "mobile": {
            "cwd": "/Users/ALISTAIRE/aevespers2-0",
            "branch": "main",
            "blocker": "",
            "next_action": "Report user-facing priorities, blockers, approvals, and completion follow-up.",
        },
        "safari_cloud": {
            "cwd": "/workspace/0",
            "branch": "work",
            "blocker": "",
            "next_action": "Refresh Safari status, export diffs as patch proposals, and do not push directly.",
            "constraints": ["patch_only_no_direct_push"],
        },
        "chatgpt_bridge": {
            "cwd": "",
            "branch": "",
            "blocker": "",
            "next_action": "Review coordination state and return advisory planning feedback.",
        },
    }
    defaults = surface_defaults.get(agent, surface_defaults["chatgpt_bridge"])
    template = {
        "schema": "codex_federation_message.v1",
        "agent": agent,
        "type": "routine_checkin" if agent == "chatgpt_bridge" else "status",
        "workstream": "Autonomous VNext",
        "cwd": defaults["cwd"],
        "branch": defaults["branch"],
        "commit": authoritative_head,
        "status_short": [],
        "remote": "",
        "blocker": defaults["blocker"],
        "next_action": defaults["next_action"],
        "expected_path": expected_path,
    }
    constraints = defaults.get("constraints", [])
    if constraints:
        template["constraints"] = constraints
    return template


def handoff_text_for(dispatch: dict[str, Any], authoritative_head: str) -> str:
    template = json.dumps(dispatch["status_template"], indent=2, sort_keys=True)
    return (
        f"Federation dispatch for {dispatch['agent']}.\n"
        f"Required packet: {dispatch['packet_type']} at {dispatch['expected_path']}.\n"
        f"Authoritative head: {authoritative_head}.\n"
        f"Details: {dispatch['details']}.\n"
        f"Suggested command: {dispatch['command']}.\n"
        "If the command cannot run in this surface, emit the equivalent JSON packet:\n"
        f"{template}"
    )


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
        dispatch = {
            "agent": agent,
            "surface_dir": SURFACE_TO_DIR.get(agent, agent),
            "packet_type": packet["packet_type"],
            "priority": packet["priority"],
            "details": packet["details"],
            "expected_path": expected_path,
            "command": command_for(agent, expected_path),
            "status_template": status_template_for(
                agent,
                str(packet["packet_type"]),
                authoritative_head,
                expected_path,
            ),
        }
        dispatch["handoff_text"] = handoff_text_for(dispatch, authoritative_head)
        dispatches.append(dispatch)

    return {
        "schema": "codex_federation_dispatch.v1",
        "generated_at": utc_now(),
        "authoritative_head": authoritative_head,
        "parallel_work": parallel_work_allocation(authoritative_head),
        "ready_for_remote_write": report["ready_for_remote_write"],
        "readiness_blockers": report["readiness_blockers"],
        "dispatch_count": len(dispatches),
        "dispatches": dispatches,
    }


def prune_stale_surface_dispatches(output_root: Path, active_surface_dirs: set[str]) -> tuple[str, ...]:
    pruned: list[str] = []
    for surface_dir in set(SURFACE_TO_DIR.values()):
        if surface_dir in active_surface_dirs:
            continue
        path = output_root / surface_dir / "dispatch.json"
        if path.exists():
            path.unlink()
            pruned.append(str(path))
    return tuple(sorted(pruned))


def write_dispatch(payload: dict[str, Any], output_root: Path) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    aggregate = output_root / "dispatch.json"
    aggregate.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written: dict[str, Any] = {"aggregate": str(aggregate)}
    active_surface_dirs = {str(dispatch["surface_dir"]) for dispatch in payload["dispatches"]}

    for dispatch in payload["dispatches"]:
        surface_dir = output_root / dispatch["surface_dir"]
        surface_dir.mkdir(parents=True, exist_ok=True)
        path = surface_dir / "dispatch.json"
        surface_payload = {
            "schema": "codex_federation_surface_dispatch.v1",
            "generated_at": payload["generated_at"],
            "authoritative_head": payload["authoritative_head"],
            "parallel_work": payload["parallel_work"],
            "dispatch": dispatch,
        }
        path.write_text(json.dumps(surface_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written[dispatch["agent"]] = str(path)

    pruned = prune_stale_surface_dispatches(output_root, active_surface_dirs)
    if pruned:
        written["pruned"] = pruned

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
