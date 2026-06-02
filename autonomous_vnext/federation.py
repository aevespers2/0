from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


REQUIRED_SURFACES = ("local_cli", "safari_cloud", "desktop_app")
EXTENDED_SURFACES = ("mobile", "chatgpt_bridge")


@dataclass(frozen=True)
class CodexAgentStatus:
    surface: str
    workstream: str
    cwd: str
    branch: str
    head: str
    status_short: tuple[str, ...]
    remote: str
    blocker: str = ""
    next_action: str = ""
    capabilities: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.surface.strip():
            raise ValueError("surface is required")
        if not self.workstream.strip():
            raise ValueError("workstream is required")
        if not self.head.strip():
            raise ValueError("head is required")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> CodexAgentStatus:
        return cls(
            surface=str(payload["surface"]),
            workstream=str(payload["workstream"]),
            cwd=str(payload["cwd"]),
            branch=str(payload["branch"]),
            head=str(payload["head"]),
            status_short=tuple(str(item) for item in payload.get("status_short", ())),
            remote=str(payload.get("remote", "")),
            blocker=str(payload.get("blocker", "")),
            next_action=str(payload.get("next_action", "")),
            capabilities=tuple(str(item) for item in payload.get("capabilities", ())),
            constraints=tuple(str(item) for item in payload.get("constraints", ())),
        )


@dataclass(frozen=True)
class RoleAssignment:
    surface: str
    role: str
    responsibilities: tuple[str, ...]
    boundaries: tuple[str, ...]


@dataclass(frozen=True)
class FederationAssessment:
    synchronized: bool
    authoritative_head: str
    present_surfaces: tuple[str, ...]
    missing_surfaces: tuple[str, ...]
    explicitly_blocked_surfaces: tuple[str, ...]
    stale_surfaces: tuple[str, ...]
    blocked_surfaces: tuple[str, ...]
    assignments: tuple[RoleAssignment, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "synchronized": self.synchronized,
            "authoritative_head": self.authoritative_head,
            "present_surfaces": self.present_surfaces,
            "missing_surfaces": self.missing_surfaces,
            "explicitly_blocked_surfaces": self.explicitly_blocked_surfaces,
            "stale_surfaces": self.stale_surfaces,
            "blocked_surfaces": self.blocked_surfaces,
            "assignments": tuple(asdict(item) for item in self.assignments),
        }


def assess_federation(
    statuses: tuple[CodexAgentStatus, ...],
    authoritative_head: str,
    required_surfaces: tuple[str, ...] = REQUIRED_SURFACES,
) -> FederationAssessment:
    if not authoritative_head.strip():
        raise ValueError("authoritative_head is required")

    latest_by_surface = {status.surface: status for status in statuses}
    present = tuple(surface for surface in required_surfaces if surface in latest_by_surface)
    missing = tuple(surface for surface in required_surfaces if surface not in latest_by_surface)
    explicitly_blocked = tuple(
        surface for surface in present if latest_by_surface[surface].blocker.strip()
    )
    stale = tuple(
        surface for surface in present if latest_by_surface[surface].head != authoritative_head
    )

    blocked: list[str] = []
    seen: set[str] = set()
    for surface in (*explicitly_blocked, *stale):
        if surface not in seen:
            blocked.append(surface)
            seen.add(surface)
    blocked = tuple(blocked)

    synchronized = not missing and not blocked
    return FederationAssessment(
        synchronized=synchronized,
        authoritative_head=authoritative_head,
        present_surfaces=present,
        missing_surfaces=missing,
        explicitly_blocked_surfaces=explicitly_blocked,
        stale_surfaces=stale,
        blocked_surfaces=blocked,
        assignments=assign_roles(statuses),
    )


def assign_roles(statuses: tuple[CodexAgentStatus, ...]) -> tuple[RoleAssignment, ...]:
    surfaces = {status.surface for status in statuses}
    assignments = []

    if "local_cli" in surfaces:
        assignments.append(
            RoleAssignment(
                surface="local_cli",
                role="implementation_authority",
                responsibilities=(
                    "final implementation decisions",
                    "local verification",
                    "commits and deployments",
                ),
                boundaries=("must verify safe repo path", "must preserve user changes"),
            )
        )
    if "safari_cloud" in surfaces:
        assignments.append(
            RoleAssignment(
                surface="safari_cloud",
                role="cloud_planning_review",
                responsibilities=("design review", "diff review", "PR-visible planning"),
                boundaries=("do not treat ephemeral push state as authoritative",),
            )
        )
    if "desktop_app" in surfaces:
        assignments.append(
            RoleAssignment(
                surface="desktop_app",
                role="local_app_observer",
                responsibilities=("desktop UI checks", "macOS accessibility observations", "local context relay"),
                boundaries=("do not push broad personal directories",),
            )
        )
    if "mobile" in surfaces:
        assignments.append(
            RoleAssignment(
                surface="mobile",
                role="routine_checkin",
                responsibilities=("daily user check-ins", "routine reminders", "completion follow-up"),
                boundaries=("no implementation authority without local verification",),
            )
        )
    if "chatgpt_bridge" in surfaces:
        assignments.append(
            RoleAssignment(
                surface="chatgpt_bridge",
                role="design_planning_assist",
                responsibilities=("design critique", "planning assistance", "cross-agent check-ins"),
                boundaries=("advisory only; local_cli has final implementation authority",),
            )
        )

    return tuple(assignments)


def recurring_routines(assessment: FederationAssessment) -> tuple[dict[str, str], ...]:
    cadence = "daily"
    routines = [
        {
            "cadence": cadence,
            "owner": "local_cli",
            "task": "Verify safe repo status, CI state, and active blockers before implementation.",
        },
        {
            "cadence": cadence,
            "owner": "chatgpt_bridge",
            "task": "Review plans and design tradeoffs, then send advisory feedback to local_cli.",
        },
        {
            "cadence": cadence,
            "owner": "mobile",
            "task": "Prompt user-facing check-in for priorities, blockers, and approval needs.",
        },
        {
            "cadence": cadence,
            "owner": "local_cli",
            "task": "Advance fraud-pipeline projects when repo, APIs, credentials, and safety boundaries are explicit.",
        },
    ]
    if assessment.missing_surfaces:
        routines.append(
            {
                "cadence": "until_resolved",
                "owner": "local_cli",
                "task": "Collect missing status packets: " + ", ".join(assessment.missing_surfaces),
            }
        )
    if assessment.stale_surfaces:
        routines.append(
            {
                "cadence": "until_resolved",
                "owner": "local_cli",
                "task": "Collect updated status packets for stale heads: "
                + ", ".join(
                    f"{surface}@{assessment.authoritative_head}" for surface in assessment.stale_surfaces
                ),
            }
        )
    if assessment.explicitly_blocked_surfaces:
        routines.append(
            {
                "cadence": "until_resolved",
                "owner": "local_cli",
                "task": "Resolve blockers for surfaces: " + ", ".join(assessment.explicitly_blocked_surfaces),
            }
        )
    return tuple(routines)
