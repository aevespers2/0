from __future__ import annotations

import json
import sys

import pytest

from autonomous_vnext.audit import ActionRecord, AuditLogWriter
from autonomous_vnext.itensor_adapter import ITensorUnavailableError, best_plan_with_itensor
from autonomous_vnext.planner import CandidatePlan, generate_candidate_plans, select_lowest_risk_plan
from autonomous_vnext.policy import PolicyEvaluator


def test_schemas_are_valid_json() -> None:
    for filename in ["mission_contract.schema.json", "action_record.schema.json"]:
        with open(filename, encoding="utf-8") as handle:
            assert json.load(handle)["type"] == "object"


def test_policy_denies_empty_and_unknown_commands() -> None:
    policy = PolicyEvaluator(allowed_command_prefixes=(("pytest", "-q"),))
    assert not policy.evaluate("").allowed
    assert not policy.evaluate("git push").allowed


def test_policy_allows_configured_prefix() -> None:
    policy = PolicyEvaluator(allowed_command_prefixes=(("pytest", "-q"),))
    assert policy.evaluate("pytest -q").allowed


def test_policy_require_allowed_raises() -> None:
    policy = PolicyEvaluator(allowed_command_prefixes=(("pytest", "-q"),))
    with pytest.raises(PermissionError):
        policy.require_allowed("git push")


def test_audit_log_writer_appends_jsonl(tmp_path) -> None:
    path = tmp_path / "audit.jsonl"
    writer = AuditLogWriter(path)
    writer.append(
        ActionRecord(
            action_id="act-001",
            mission_id="mission-001",
            step_id="step-001",
            actor="test",
            action_type="check",
            status="pass",
            summary="ok",
        )
    )
    writer.append(
        ActionRecord(
            action_id="act-002",
            mission_id="mission-001",
            step_id="step-002",
            actor="test",
            action_type="check",
            status="blocked",
            summary="blocked",
        )
    )
    assert len(path.read_text(encoding="utf-8").splitlines()) == 2


def test_lowest_risk_plan_selection() -> None:
    plans = generate_candidate_plans("ship x")
    selected = select_lowest_risk_plan(plans)
    assert selected.plan_id == "plan-read-first"


def test_itensor_unavailable_path(monkeypatch) -> None:
    monkeypatch.setitem(sys.modules, "itensor", None)
    with pytest.raises(ITensorUnavailableError):
        best_plan_with_itensor([CandidatePlan("p", ("inspect",), 1)])


def test_itensor_mocked_best_plan(monkeypatch) -> None:
    class FakeITensor:
        pass

    monkeypatch.setitem(sys.modules, "itensor", FakeITensor())
    plans = [CandidatePlan("riskier", ("push",), 8), CandidatePlan("safer", ("inspect",), 1)]
    assert best_plan_with_itensor(plans).plan_id == "safer"
