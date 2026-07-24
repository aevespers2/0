from __future__ import annotations

import copy
import hashlib
from pathlib import Path

import pytest

from iris_verifier_contract import (
    ContractError,
    assert_privacy_safe_record,
    project_atomic_consume_and_record,
    strict_json_loads,
    validate_atomic_fixture_case,
    validate_atomic_state,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "iris-verifier" / "atomic-consume-record-vectors.json"
EXPECTED_SHA256 = "5557b6eeec96a2655410a9a60bfddec9c981a10762f0f02eb6b91f07e0379fc5"


def _manifest() -> dict:
    payload = FIXTURE.read_bytes()
    assert hashlib.sha256(payload).hexdigest() == EXPECTED_SHA256
    return strict_json_loads(payload.decode("utf-8"))


def _case_inputs(manifest: dict, case: dict) -> tuple[dict, dict]:
    state = copy.deepcopy(manifest["baseline"]["state"])
    operation = copy.deepcopy(manifest["baseline"]["operation"])
    state.update(copy.deepcopy(case["state_overrides"]))
    operation.update(copy.deepcopy(case["operation_overrides"]))
    return state, operation


def test_shared_atomic_fixture_projects_every_required_outcome() -> None:
    manifest = _manifest()
    assert manifest["synthetic_only"] is True
    assert manifest["operational_authority"] is False

    observed = {}
    for case in manifest["cases"]:
        state, operation = _case_inputs(manifest, case)
        result = validate_atomic_fixture_case(
            state=state,
            operation=operation,
            expected=case["expected"],
        )
        observed[case["case_id"]] = (result["outcome"], result["error"])

    assert observed == {
        "valid-commit": ("accepted", None),
        "replayed-attempt": ("reject", "attempt-replay"),
        "revoked-profile": ("reject", "profile-revoked"),
        "stale-state-version": ("reject", "stale-state-version"),
        "interrupted-before-commit": (
            "interrupted-before-commit",
            "before-commit",
        ),
        "interrupted-after-prepare": (
            "interrupted-before-commit",
            "after-prepare",
        ),
        "committed-before-ack": ("committed-no-ack", None),
        "retry-after-unknown-ack": ("already-committed", None),
        "partial-consume-without-receipt": ("reject", "partial-consume-record"),
        "partial-receipt-without-consume": ("reject", "partial-consume-record"),
    }


def test_precommit_interruptions_leave_state_byte_identical() -> None:
    manifest = _manifest()
    baseline = manifest["baseline"]
    for fault_point in ("before-commit", "after-prepare"):
        operation = dict(baseline["operation"], fault_point=fault_point)
        result = project_atomic_consume_and_record(
            state=baseline["state"],
            operation=operation,
        )
        assert result["outcome"] == "interrupted-before-commit"
        assert result["state"] == baseline["state"]
        assert result["authority_state_mutated"] is False


def test_postcommit_unknown_ack_is_idempotent_on_retry() -> None:
    manifest = _manifest()
    baseline = manifest["baseline"]
    first = project_atomic_consume_and_record(
        state=baseline["state"],
        operation=dict(
            baseline["operation"],
            fault_point="after-commit-before-ack",
        ),
    )
    assert first["outcome"] == "committed-no-ack"

    retry = project_atomic_consume_and_record(
        state=first["state"],
        operation=dict(
            baseline["operation"],
            expected_state_version=first["state"]["state_version"],
        ),
    )
    assert retry["outcome"] == "already-committed"
    assert retry["state"] == first["state"]


def test_partial_consume_or_record_state_fails_closed() -> None:
    manifest = _manifest()
    baseline = manifest["baseline"]["state"]

    consumed_only = copy.deepcopy(baseline)
    consumed_only["seen_attempt_ids"].append("iris-attempt-orphan")
    with pytest.raises(ContractError, match="partial-consume-record"):
        validate_atomic_state(consumed_only)

    receipt_only = copy.deepcopy(baseline)
    receipt_only["receipts"].append(
        {
            "receipt_id": "iris-receipt-orphan",
            "operation_id": "iris-operation-orphan",
            "attempt_id": "iris-attempt-orphan",
            "profile_id": "iris-profile-a",
            "disposition": "accepted",
            "committed_state_version": 7,
        }
    )
    with pytest.raises(ContractError, match="partial-consume-record"):
        validate_atomic_state(receipt_only)


def test_atomic_fixture_is_privacy_safe_and_has_unique_cases() -> None:
    manifest = _manifest()
    assert_privacy_safe_record(manifest)
    case_ids = [case["case_id"] for case in manifest["cases"]]
    assert len(case_ids) == len(set(case_ids))
