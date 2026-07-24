from __future__ import annotations

import copy
import hashlib
from collections.abc import Mapping
from typing import Any

from .contract import (
    ContractError,
    _require_exact_keys,
    _require_identifier,
    canonical_json_bytes,
)


_STATE_KEYS = {
    "schema",
    "state_version",
    "seen_attempt_ids",
    "revoked_profile_ids",
    "receipts",
}
_OPERATION_KEYS = {
    "schema",
    "operation_id",
    "attempt_id",
    "profile_id",
    "expected_state_version",
    "proposed_receipt_id",
    "fault_point",
}
_RECEIPT_KEYS = {
    "receipt_id",
    "operation_id",
    "attempt_id",
    "profile_id",
    "disposition",
    "committed_state_version",
}
_EXPECTED_KEYS = {
    "outcome",
    "error",
    "state_version",
    "seen_attempt_ids",
    "receipt_count",
    "state_sha256",
}
_ALLOWED_FAULT_POINTS = {
    "none",
    "before-commit",
    "after-prepare",
    "after-commit-before-ack",
}


def atomic_state_sha256(state: Mapping[str, Any]) -> str:
    """Hash one validated synthetic authority-state snapshot."""

    normalized = validate_atomic_state(state)
    return hashlib.sha256(canonical_json_bytes(normalized)).hexdigest()


def validate_atomic_state(state: Mapping[str, Any]) -> dict[str, Any]:
    """Reject state snapshots that expose a partial consume/record commit."""

    normalized = _require_exact_keys("atomic state", state, _STATE_KEYS)
    if normalized["schema"] != "qso.iris-authority-state.v0":
        raise ContractError("unsupported atomic state schema")

    state_version = normalized["state_version"]
    if type(state_version) is not int or state_version < 1:
        raise ContractError("atomic state version must be a positive integer")

    for field in ("seen_attempt_ids", "revoked_profile_ids"):
        values = normalized[field]
        if not isinstance(values, list) or not all(
            isinstance(value, str) for value in values
        ):
            raise ContractError(f"{field} must be a list of identifiers")
        for value in values:
            _require_identifier(field, value)
        if len(values) != len(set(values)):
            raise ContractError(f"{field} must not contain duplicates")

    receipts = normalized["receipts"]
    if not isinstance(receipts, list):
        raise ContractError("receipts must be a list")

    receipt_ids: set[str] = set()
    operation_ids: set[str] = set()
    receipt_attempt_ids: list[str] = []
    normalized_receipts: list[dict[str, Any]] = []
    for receipt in receipts:
        receipt = _require_exact_keys("receipt", receipt, _RECEIPT_KEYS)
        for field in (
            "receipt_id",
            "operation_id",
            "attempt_id",
            "profile_id",
        ):
            _require_identifier(field, receipt[field])
        if receipt["receipt_id"] in receipt_ids:
            raise ContractError("duplicate receipt id")
        if receipt["operation_id"] in operation_ids:
            raise ContractError("duplicate operation id")
        receipt_ids.add(receipt["receipt_id"])
        operation_ids.add(receipt["operation_id"])
        receipt_attempt_ids.append(receipt["attempt_id"])

        if receipt["disposition"] != "accepted":
            raise ContractError("receipt disposition must be accepted")
        committed_version = receipt["committed_state_version"]
        if (
            type(committed_version) is not int
            or committed_version < 1
            or committed_version > state_version
        ):
            raise ContractError("receipt committed_state_version is invalid")
        normalized_receipts.append(receipt)

    if sorted(receipt_attempt_ids) != sorted(normalized["seen_attempt_ids"]):
        raise ContractError("partial-consume-record")

    normalized["receipts"] = normalized_receipts
    return normalized


def validate_atomic_operation(operation: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a synthetic consume-and-record proposal without executing it."""

    normalized = _require_exact_keys("atomic operation", operation, _OPERATION_KEYS)
    if normalized["schema"] != "qso.iris-consume-record-operation.v0":
        raise ContractError("unsupported atomic operation schema")
    for field in (
        "operation_id",
        "attempt_id",
        "profile_id",
        "proposed_receipt_id",
    ):
        _require_identifier(field, normalized[field])
    expected_version = normalized["expected_state_version"]
    if type(expected_version) is not int or expected_version < 1:
        raise ContractError("expected_state_version must be a positive integer")
    if normalized["fault_point"] not in _ALLOWED_FAULT_POINTS:
        raise ContractError("unsupported fault point")
    return normalized


def project_atomic_consume_and_record(
    *,
    state: Mapping[str, Any],
    operation: Mapping[str, Any],
) -> dict[str, Any]:
    """Project one synthetic authority transaction without writing authority state.

    The function is deliberately pure. It demonstrates the required all-or-nothing
    outcome but does not persist replay, revocation, receipt, or identity state.
    """

    normalized_state = validate_atomic_state(state)
    normalized_operation = validate_atomic_operation(operation)

    existing = [
        receipt
        for receipt in normalized_state["receipts"]
        if receipt["operation_id"] == normalized_operation["operation_id"]
    ]
    if existing:
        receipt = existing[0]
        if (
            receipt["attempt_id"] == normalized_operation["attempt_id"]
            and receipt["profile_id"] == normalized_operation["profile_id"]
            and receipt["receipt_id"] == normalized_operation["proposed_receipt_id"]
        ):
            return {
                "outcome": "already-committed",
                "error": None,
                "state": copy.deepcopy(normalized_state),
                "authority_state_mutated": False,
            }
        return {
            "outcome": "reject",
            "error": "operation-id-conflict",
            "state": copy.deepcopy(normalized_state),
            "authority_state_mutated": False,
        }

    if normalized_operation["attempt_id"] in normalized_state["seen_attempt_ids"]:
        return {
            "outcome": "reject",
            "error": "attempt-replay",
            "state": copy.deepcopy(normalized_state),
            "authority_state_mutated": False,
        }
    if normalized_operation["profile_id"] in normalized_state["revoked_profile_ids"]:
        return {
            "outcome": "reject",
            "error": "profile-revoked",
            "state": copy.deepcopy(normalized_state),
            "authority_state_mutated": False,
        }
    if (
        normalized_operation["expected_state_version"]
        != normalized_state["state_version"]
    ):
        return {
            "outcome": "reject",
            "error": "stale-state-version",
            "state": copy.deepcopy(normalized_state),
            "authority_state_mutated": False,
        }

    fault_point = normalized_operation["fault_point"]
    if fault_point in {"before-commit", "after-prepare"}:
        return {
            "outcome": "interrupted-before-commit",
            "error": fault_point,
            "state": copy.deepcopy(normalized_state),
            "authority_state_mutated": False,
        }

    committed = copy.deepcopy(normalized_state)
    committed["state_version"] += 1
    committed["seen_attempt_ids"].append(normalized_operation["attempt_id"])
    committed["receipts"].append(
        {
            "receipt_id": normalized_operation["proposed_receipt_id"],
            "operation_id": normalized_operation["operation_id"],
            "attempt_id": normalized_operation["attempt_id"],
            "profile_id": normalized_operation["profile_id"],
            "disposition": "accepted",
            "committed_state_version": committed["state_version"],
        }
    )
    committed = validate_atomic_state(committed)
    return {
        "outcome": (
            "committed-no-ack"
            if fault_point == "after-commit-before-ack"
            else "accepted"
        ),
        "error": None,
        "state": committed,
        "authority_state_mutated": False,
    }


def validate_atomic_fixture_case(
    *,
    state: Mapping[str, Any],
    operation: Mapping[str, Any],
    expected: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one shared synthetic case against the producer-side projection."""

    expected = _require_exact_keys("atomic expected result", expected, _EXPECTED_KEYS)
    if expected["outcome"] not in {
        "accepted",
        "already-committed",
        "committed-no-ack",
        "interrupted-before-commit",
        "reject",
    }:
        raise ContractError("unsupported expected outcome")
    if expected["error"] is not None and not isinstance(expected["error"], str):
        raise ContractError("expected error must be text or null")

    try:
        result = project_atomic_consume_and_record(state=state, operation=operation)
    except ContractError as exc:
        result = {
            "outcome": "reject",
            "error": str(exc),
            "state": copy.deepcopy(dict(state)),
            "authority_state_mutated": False,
        }

    actual_state = result["state"]
    actual = {
        "outcome": result["outcome"],
        "error": result["error"],
        "state_version": actual_state["state_version"],
        "seen_attempt_ids": actual_state["seen_attempt_ids"],
        "receipt_count": len(actual_state["receipts"]),
        "state_sha256": hashlib.sha256(
            canonical_json_bytes(actual_state)
        ).hexdigest(),
    }
    if actual != dict(expected):
        raise ContractError(
            f"atomic fixture outcome mismatch: expected={dict(expected)!r} actual={actual!r}"
        )
    if result["authority_state_mutated"] is not False:
        raise ContractError("producer-side projection must not mutate authority state")
    return actual
