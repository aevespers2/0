from __future__ import annotations

from autonomous_vnext.federation import CodexAgentStatus, assess_federation, recurring_routines


def status(surface: str, head: str = "abc123", blocker: str = "") -> CodexAgentStatus:
    return CodexAgentStatus(
        surface=surface,
        workstream="Autonomous vNext",
        cwd="/repo",
        branch="main",
        head=head,
        status_short=("## main...origin/main",),
        remote="git@example:repo.git",
        blocker=blocker,
        next_action="report status",
    )


def test_assess_federation_requires_three_core_surfaces() -> None:
    assessment = assess_federation((status("local_cli"),), authoritative_head="abc123")

    assert not assessment.synchronized
    assert assessment.present_surfaces == ("local_cli",)
    assert assessment.missing_surfaces == ("safari_cloud", "desktop_app")
    assert assessment.blocked_surfaces == ()


def test_assess_federation_detects_stale_or_blocked_surface() -> None:
    assessment = assess_federation(
        (
            status("local_cli"),
            status("safari_cloud", head="stale"),
            status("desktop_app", blocker="missing token"),
        ),
        authoritative_head="abc123",
    )

    assert not assessment.synchronized
    assert set(assessment.blocked_surfaces) == {"safari_cloud", "desktop_app"}
    assert assessment.stale_surfaces == ("safari_cloud",)
    assert assessment.explicitly_blocked_surfaces == ("desktop_app",)


def test_assess_federation_assigns_surface_specific_roles() -> None:
    assessment = assess_federation(
        (
            status("local_cli"),
            status("safari_cloud"),
            status("desktop_app"),
            status("mobile"),
            status("chatgpt_bridge"),
        ),
        authoritative_head="abc123",
    )

    roles = {assignment.surface: assignment.role for assignment in assessment.assignments}
    assert assessment.synchronized
    assert roles["local_cli"] == "implementation_authority"
    assert roles["mobile"] == "routine_checkin"
    assert roles["chatgpt_bridge"] == "design_planning_assist"


def test_recurring_routines_include_fraud_pipeline_focus_and_missing_surfaces() -> None:
    assessment = assess_federation((status("local_cli"),), authoritative_head="abc123")
    routines = recurring_routines(assessment)

    assert any("fraud-pipeline" in item["task"] for item in routines)
    assert routines[-1]["owner"] == "local_cli"
    assert "safari_cloud" in routines[-1]["task"]
