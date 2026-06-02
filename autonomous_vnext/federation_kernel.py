from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from autonomous_vnext.federation import CodexAgentStatus, assess_federation, recurring_routines


MESSAGE_SCHEMA = "codex_federation_message.v1"
PATCH_SCHEMA = "codex_patch_proposal.v1"
AUTHORIZED_WRITER = "local_cli"
SURFACE_DIRS = {
    "local": "local_cli",
    "safari": "safari_cloud",
    "desktop": "desktop_app",
    "mobile": "mobile",
    "bridge": "chatgpt_bridge",
}
MESSAGE_TYPES = {"status", "blocker", "patch_proposal", "routine_checkin"}


@dataclass(frozen=True)
class FederationMessage:
    path: str
    agent: str
    message_type: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class PatchProposal:
    source: str
    repo: str
    base: str
    patch_type: str
    summary: str
    files: tuple[str, ...]
    authority: str = AUTHORIZED_WRITER
    patch_path: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> PatchProposal:
        if payload.get("schema") != PATCH_SCHEMA:
            raise ValueError("unsupported patch proposal schema")
        return cls(
            source=str(payload["source"]),
            repo=str(payload["repo"]),
            base=str(payload["base"]),
            patch_type=str(payload["type"]),
            summary=str(payload["summary"]),
            files=tuple(str(item) for item in payload.get("files", ())),
            authority=str(payload.get("authority", AUTHORIZED_WRITER)),
            patch_path=str(payload.get("patch_path", "")),
        )

    def validate(self) -> tuple[str, ...]:
        errors = []
        if self.authority != AUTHORIZED_WRITER:
            errors.append("patch authority must be local_cli")
        if self.source == AUTHORIZED_WRITER:
            errors.append("local_cli should commit directly, not submit patch proposals")
        if self.patch_type != "git_patch":
            errors.append("patch type must be git_patch")
        if not self.base.strip():
            errors.append("patch base is required")
        if not self.summary.strip():
            errors.append("patch summary is required")
        return tuple(errors)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_message(path: Path) -> FederationMessage:
    payload = load_json(path)
    if payload.get("schema") != MESSAGE_SCHEMA:
        raise ValueError(f"{path}: unsupported message schema")
    message_type = str(payload["type"])
    if message_type not in MESSAGE_TYPES:
        raise ValueError(f"{path}: unsupported message type {message_type}")
    agent = str(payload["agent"])
    return FederationMessage(path=str(path), agent=agent, message_type=message_type, payload=payload)


def read_inbox(root: Path) -> tuple[FederationMessage, ...]:
    if not root.exists():
        return ()
    messages = []
    for path in sorted(root.glob("*/*.json")):
        if "/templates/" in str(path):
            continue
        if path.name.endswith("-assignment.json"):
            continue
        messages.append(parse_message(path))
    return tuple(messages)


def message_to_status(message: FederationMessage) -> CodexAgentStatus | None:
    if message.message_type not in {"status", "blocker", "routine_checkin", "patch_proposal"}:
        return None
    payload = message.payload
    return CodexAgentStatus(
        surface=message.agent,
        workstream=str(payload.get("workstream", "Autonomous vNext")),
        cwd=str(payload.get("cwd", "")),
        branch=str(payload.get("branch", "")),
        head=str(payload.get("commit", "unknown")),
        status_short=tuple(str(item) for item in payload.get("status_short", ())),
        remote=str(payload.get("remote", "")),
        blocker=str(payload.get("blocker", "")),
        next_action=str(payload.get("next_action", "")),
        capabilities=tuple(str(item) for item in payload.get("capabilities", ())),
        constraints=tuple(str(item) for item in payload.get("constraints", ())),
    )


def collect_patch_proposals(messages: tuple[FederationMessage, ...]) -> tuple[PatchProposal, ...]:
    proposals = []
    for message in messages:
        if message.message_type == "patch_proposal":
            proposals.append(PatchProposal.from_dict(dict(message.payload["patch"])))
    return tuple(proposals)


def _infer_surface_dir(agent: str) -> str:
    for surface_dir, surface_name in SURFACE_DIRS.items():
        if surface_name == agent:
            return surface_dir
    return agent


def _next_required_packets(
    assessment: dict[str, Any],
    status_by_surface: dict[str, CodexAgentStatus],
    authoritative_head: str,
) -> tuple[dict[str, str], ...]:
    action_payloads = []
    seen: set[str] = set()

    for surface in assessment["missing_surfaces"]:
        if surface in seen:
            continue
        seen.add(surface)
        action_payloads.append(
            {
                "agent": surface,
                "packet_type": "status",
                "priority": "required",
                "details": "status packet missing in FederationInbox",
                "expected_path": f"FederationInbox/{_infer_surface_dir(surface)}/status.json",
            }
        )

    for surface in assessment["stale_surfaces"]:
        if surface in seen:
            continue
        seen.add(surface)
        action_payloads.append(
            {
                "agent": surface,
                "packet_type": "status_refresh",
                "priority": "required",
                "details": (
                    f"status is stale (saw {status_by_surface[surface].head}); "
                    f"refresh to {authoritative_head}"
                ),
                "expected_path": f"FederationInbox/{_infer_surface_dir(surface)}/status.json",
            }
        )

    for surface in assessment["explicitly_blocked_surfaces"]:
        if surface in seen:
            continue
        seen.add(surface)
        action_payloads.append(
            {
                "agent": surface,
                "packet_type": "status_unblock",
                "priority": "required",
                "details": f"active blocker: {status_by_surface[surface].blocker}",
                "expected_path": f"FederationInbox/{_infer_surface_dir(surface)}/status.json",
            }
        )

    return tuple(action_payloads)


def evaluate_kernel(inbox: Path, authoritative_head: str) -> dict[str, Any]:
    messages = read_inbox(inbox)
    statuses = tuple(status for message in messages if (status := message_to_status(message)) is not None)
    status_by_surface = {status.surface: status for status in statuses}
    assessment_obj = assess_federation(statuses, authoritative_head=authoritative_head)
    assessment = assessment_obj.to_dict()
    proposals = collect_patch_proposals(messages)

    patch_errors = {}
    for proposal in proposals:
        errors = proposal.validate()
        if errors:
            patch_errors[proposal.source] = errors

    return {
        "schema": "codex_federation_kernel_report.v1",
        "authoritative_writer": AUTHORIZED_WRITER,
        "authoritative_head": authoritative_head,
        "message_count": len(messages),
        "messages": tuple(asdict(message) for message in messages),
        "assessment": assessment,
        "patch_proposals": tuple(asdict(proposal) for proposal in proposals),
        "patch_errors": patch_errors,
        "next_required_packets": _next_required_packets(
            assessment,
            status_by_surface,
            authoritative_head,
        ),
        "routines": recurring_routines(assessment_obj),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate the Codex federation inbox.")
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--authoritative-head", required=True)
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = evaluate_kernel(args.inbox, args.authoritative_head)
    print(json.dumps(report, indent=2 if args.pretty else None, sort_keys=True))
    if report["patch_errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
