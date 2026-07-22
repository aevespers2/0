from __future__ import annotations

import copy
import hashlib
from pathlib import Path

import pytest

from iris_verifier_contract import (
    ContractError,
    assert_privacy_safe_record,
    reconcile_journal,
    strict_json_loads,
    validate_journal_fixture_case,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "iris-verifier" / "crash-recovery-journal-vectors.json"
EXPECTED_SHA256 = "f255438eab406bba71ab23fad60d34b2a7d3a580e90583e1517d432d8e03b89a"


def _manifest() -> dict:
    payload = FIXTURE.read_bytes()
    assert hashlib.sha256(payload).hexdigest() == EXPECTED_SHA256
    return strict_json_loads(payload.decode("utf-8"))


def test_shared_journal_fixture_projects_every_required_outcome() -> None:
    manifest = _manifest()
    assert manifest["synthetic_only"] is True
    assert manifest["operational_authority"] is False
    observed = {}
    for case in manifest["cases"]:
        result = validate_journal_fixture_case(
            authority_state=case["authority_state"],
            records=case["journal_records"],
            expected=case["expected"],
        )
        observed[case["case_id"]] = (result["outcome"], result["error"])
    assert observed == {
        "clean-no-journal": ("clean", None),
        "prepared-only-rolls-back": ("rolled-back", None),
        "committed-without-ack-recovers": ("recovered-committed", None),
        "acknowledged-journal-recovers-stale-state": ("recovered-committed", None),
        "committed-state-replay-is-idempotent": ("already-recovered", None),
        "corrupted-record-digest": ("reject", "journal-record-digest-mismatch"),
        "journal-sequence-gap": ("reject", "journal-sequence-gap"),
        "revoked-before-recovery": ("reject", "profile-revoked-before-recovery"),
        "duplicate-receipt-in-target-state": ("reject", "duplicate receipt"),
        "prepared-prior-digest-mismatch": ("reject", "journal-prior-state-mismatch"),
    }


def test_reconciliation_is_pure_and_idempotent() -> None:
    manifest = _manifest()
    case = next(
        item for item in manifest["cases"]
        if item["case_id"] == "committed-without-ack-recovers"
    )
    original = copy.deepcopy(case["authority_state"])
    first = reconcile_journal(
        authority_state=case["authority_state"],
        records=case["journal_records"],
    )
    assert case["authority_state"] == original
    assert first["authority_state_mutated"] is False
    second = reconcile_journal(
        authority_state=first["state"],
        records=case["journal_records"],
    )
    assert second["outcome"] == "already-recovered"
    assert second["state"] == first["state"]


def test_malformed_phase_order_and_record_limit_fail_closed() -> None:
    manifest = _manifest()
    case = next(
        item for item in manifest["cases"]
        if item["case_id"] == "acknowledged-journal-recovers-stale-state"
    )
    with pytest.raises(ContractError, match="journal-phase-order-invalid"):
        reconcile_journal(
            authority_state=case["authority_state"],
            records=case["journal_records"][1:],
        )
    with pytest.raises(ContractError, match="journal-record-limit-exceeded"):
        reconcile_journal(
            authority_state=case["authority_state"],
            records=case["journal_records"] * 6,
        )


def test_journal_fixture_is_privacy_safe_and_unique() -> None:
    manifest = _manifest()
    assert_privacy_safe_record(manifest)
    case_ids = [case["case_id"] for case in manifest["cases"]]
    assert len(case_ids) == len(set(case_ids))
