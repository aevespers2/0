from pathlib import Path

import pytest

from autonomous_vnext.core import (
    AuditLogWriter,
    PolicyEvaluator,
    PolicyViolationError,
    pick_lowest_risk_plan,
    risk_score,
)
from autonomous_vnext.itensor_adapter import (
    ITensorUnavailableError,
    best_plan_with_itensor,
    score_plans_with_itensor,
)
from autonomous_vnext.cognitive_hilbert import (
    HilbertSpaceSpec,
    build_cognitive_backbone,
    require_itensor_backbone,
)


def test_policy_evaluator_deny_by_default() -> None:
    evaluator = PolicyEvaluator(allow_commands={"pytest", "git"})
    decision = evaluator.evaluate("rm -rf /")
    assert not decision.allowed


def test_policy_evaluator_path_guard() -> None:
    evaluator = PolicyEvaluator(allow_commands={"git"}, allow_path_prefixes=("src/", "tests/"))
    decision = evaluator.evaluate("git add .", touched_paths=["docs/readme.md"])
    assert not decision.allowed


def test_policy_evaluator_require_allowed() -> None:
    evaluator = PolicyEvaluator(allow_commands={"pytest"})
    with pytest.raises(PolicyViolationError):
        evaluator.require_allowed("curl https://example.com")


def test_audit_log_writer_appends_jsonl(tmp_path: Path) -> None:
    log_path = tmp_path / "audit.jsonl"
    writer = AuditLogWriter(log_path)
    writer.append({"step_id": "exec-1", "result": "pass"})
    writer.append({"step_id": "exec-2", "result": "fail"})

    lines = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    assert '"step_id": "exec-1"' in lines[0]


def test_plan_selection_prefers_lowest_risk() -> None:
    plan = pick_lowest_risk_plan("Add health endpoint")
    assert plan["id"] == "plan-1"
    assert risk_score(plan) == 5


def test_policy_evaluator_empty_command_denied() -> None:
    evaluator = PolicyEvaluator(allow_commands={"git"})
    decision = evaluator.evaluate("   ")
    assert not decision.allowed


def test_policy_evaluator_allowed_path_prefix() -> None:
    evaluator = PolicyEvaluator(allow_commands={"git"}, allow_path_prefixes=("tests/",))
    decision = evaluator.evaluate("git add tests/test_core.py", touched_paths=["tests/test_core.py"])
    assert decision.allowed


def test_itensor_scoring_requires_dependency() -> None:
    with pytest.raises(ITensorUnavailableError):
        score_plans_with_itensor({"plan-1": [1.0, 2.0]}, [0.5, 0.5])


def test_itensor_best_plan_when_available(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("autonomous_vnext.itensor_adapter.itensor_available", lambda: True)
    best = best_plan_with_itensor(
        {
            "plan-1": [1.0, 1.0, 1.0],
            "plan-2": [2.0, 2.0, 2.0],
            "plan-3": [0.2, 0.4, 0.1],
        },
        [1.0, 1.0, 1.0],
    )
    assert best.plan_id == "plan-3"



def test_build_cognitive_backbone_dimension() -> None:
    backbone = build_cognitive_backbone(
        [
            HilbertSpaceSpec(name="planning", dimensions=(4, 8)),
            HilbertSpaceSpec(name="memory", dimensions=(16, 16, 4)),
        ]
    )
    assert backbone.rank == 5
    assert backbone.total_dimension == (4 * 8) * (16 * 16 * 4)


def test_build_cognitive_backbone_rejects_invalid_dims() -> None:
    with pytest.raises(ValueError):
        build_cognitive_backbone([HilbertSpaceSpec(name="bad", dimensions=(8, 0))])


def test_require_itensor_backbone(monkeypatch: pytest.MonkeyPatch) -> None:
    backbone = build_cognitive_backbone([HilbertSpaceSpec(name="planning", dimensions=(2, 2, 2))])
    with pytest.raises(ITensorUnavailableError):
        require_itensor_backbone(backbone)

    monkeypatch.setattr("autonomous_vnext.cognitive_hilbert.require_itensor", lambda: None)
    require_itensor_backbone(backbone)
