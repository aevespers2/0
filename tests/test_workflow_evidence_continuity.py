from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = {
    "comment-style": ROOT / ".github/workflows/comment-style.yml",
    "gods-observability": ROOT / ".github/workflows/gods-observability.yml",
    "autonomous-vnext": ROOT / ".github/workflows/autonomous-vnext-ci.yml",
    "clan-terraform": ROOT / ".github/workflows/clan-terraform.yml",
}
EXACT_HEAD_EXPRESSION = "github.event.pull_request.head.sha || github.sha"
UPLOAD_ARTIFACT_PIN = (
    "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02"
)


def read_workflow(name: str) -> str:
    return WORKFLOWS[name].read_text(encoding="utf-8")


def test_target_workflows_isolate_exact_heads_without_cancellation() -> None:
    for name in WORKFLOWS:
        text = read_workflow(name)
        assert EXACT_HEAD_EXPRESSION in text, name
        assert "cancel-in-progress: false" in text, name
        assert "cancel-in-progress: true" not in text, name
        assert "persist-credentials: false" in text, name
        assert UPLOAD_ARTIFACT_PIN in text, name


def test_comment_style_retains_failure_evidence_and_fails_closed() -> None:
    text = read_workflow("comment-style")
    assert "continue-on-error: true" in text
    assert "Upload exact-head evidence" in text
    assert "if: always()" in text
    assert "Fail closed on validation failure" in text
    assert "comment-style-${{ env.SUBMITTED_SHA }}" in text


def test_python_test_runners_are_pinned_where_installed() -> None:
    for name in ("gods-observability", "autonomous-vnext"):
        text = read_workflow(name)
        assert "pytest==8.4.2" in text, name
        assert "pip install --disable-pip-version-check pytest\n" not in text, name


def test_terraform_boundary_is_plan_only_and_retained_on_failure() -> None:
    text = read_workflow("clan-terraform")
    assert "automatic_apply=false" in text
    assert "Record plan-only boundary\n        if: always()" in text
    assert "Upload plan-only evidence\n        if: always()" in text
