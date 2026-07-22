from __future__ import annotations

import copy
import hashlib
import re
from collections.abc import Mapping, Sequence
from typing import Any

from .atomicity import validate_atomic_state
from .contract import ContractError, canonical_json_bytes

_ID = re.compile(r"^[a-z0-9][a-z0-9._:-]{2,127}$")
_RECORD_KEYS = {
    "schema", "journal_seq", "operation_id", "attempt_id", "profile_id",
    "receipt_id", "phase", "prior_state_sha256", "state_after", "record_sha256",
}
_ALLOWED_PHASES = ("prepared", "committed", "acknowledged")
_EXPECTED_KEYS = {
    "outcome", "error", "state_version", "seen_attempt_ids", "receipt_count", "state_sha256",
}


def _exact(name: str, value: Any, keys: set[str]) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{name} must be an object")
    if set(value) != keys:
        raise ContractError(f"{name} fields mismatch")
    return copy.deepcopy(dict(value))


def _identifier(name: str, value: Any) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise ContractError(f"{name} is invalid")
    return value


def _sha(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def journal_record_sha256(record: Mapping[str, Any]) -> str:
    body = dict(record)
    body.pop("record_sha256", None)
    return _sha(body)


def validate_journal_record(record: Mapping[str, Any]) -> dict[str, Any]:
    normalized = _exact("journal record", record, _RECORD_KEYS)
    if normalized["schema"] != "qso.iris-authority-journal-record.v0":
        raise ContractError("unsupported journal record schema")
    if type(normalized["journal_seq"]) is not int or normalized["journal_seq"] < 1:
        raise ContractError("journal sequence must be a positive integer")
    for field in ("operation_id", "attempt_id", "profile_id", "receipt_id"):
        _identifier(field, normalized[field])
    if normalized["phase"] not in _ALLOWED_PHASES:
        raise ContractError("unsupported journal phase")
    for field in ("prior_state_sha256", "record_sha256"):
        if not isinstance(normalized[field], str) or not re.fullmatch(r"[0-9a-f]{64}", normalized[field]):
            raise ContractError(f"{field} must be lowercase sha256")
    if normalized["state_after"] is not None:
        normalized["state_after"] = validate_atomic_state(normalized["state_after"])
    if normalized["phase"] == "prepared" and normalized["state_after"] is not None:
        raise ContractError("prepared record must not contain state_after")
    if normalized["phase"] in {"committed", "acknowledged"} and normalized["state_after"] is None:
        raise ContractError("committed journal phase requires state_after")
    if journal_record_sha256(normalized) != normalized["record_sha256"]:
        raise ContractError("journal-record-digest-mismatch")
    return normalized


def _validate_commit_transition(prior: dict[str, Any], committed: dict[str, Any], record: dict[str, Any]) -> None:
    if committed["state_version"] != prior["state_version"] + 1:
        raise ContractError("journal-commit-version-mismatch")
    if committed["revoked_profile_ids"] != prior["revoked_profile_ids"]:
        raise ContractError("journal-commit-revocation-drift")
    if committed["seen_attempt_ids"] != prior["seen_attempt_ids"] + [record["attempt_id"]]:
        raise ContractError("journal-commit-attempt-mismatch")
    if len(committed["receipts"]) != len(prior["receipts"]) + 1:
        raise ContractError("journal-commit-receipt-count-mismatch")
    expected_receipt = {
        "receipt_id": record["receipt_id"],
        "operation_id": record["operation_id"],
        "attempt_id": record["attempt_id"],
        "profile_id": record["profile_id"],
        "disposition": "accepted",
        "committed_state_version": committed["state_version"],
    }
    if committed["receipts"][:-1] != prior["receipts"] or committed["receipts"][-1] != expected_receipt:
        raise ContractError("journal-commit-receipt-mismatch")


def reconcile_journal(*, authority_state: Mapping[str, Any], records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Purely reconcile one bounded synthetic journal without durable writes."""
    current = validate_atomic_state(authority_state)
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes, bytearray)):
        raise ContractError("journal records must be a sequence")
    if len(records) > 16:
        raise ContractError("journal-record-limit-exceeded")
    if not records:
        return {"outcome": "clean", "error": None, "state": current, "authority_state_mutated": False}

    normalized = [validate_journal_record(record) for record in records]
    if [record["journal_seq"] for record in normalized] != list(range(1, len(normalized) + 1)):
        raise ContractError("journal-sequence-gap")
    identity = {
        (record["operation_id"], record["attempt_id"], record["profile_id"], record["receipt_id"])
        for record in normalized
    }
    if len(identity) != 1:
        raise ContractError("journal-identity-drift")
    phases = [record["phase"] for record in normalized]
    if phases not in (["prepared"], ["prepared", "committed"], ["prepared", "committed", "acknowledged"]):
        raise ContractError("journal-phase-order-invalid")
    prior_digest = normalized[0]["prior_state_sha256"]
    if any(record["prior_state_sha256"] != prior_digest for record in normalized):
        raise ContractError("journal-prior-digest-drift")
    current_digest = _sha(current)

    if normalized[0]["profile_id"] in current["revoked_profile_ids"]:
        return {
            "outcome": "reject",
            "error": "profile-revoked-before-recovery",
            "state": current,
            "authority_state_mutated": False,
        }
    if phases == ["prepared"]:
        if current_digest != prior_digest:
            raise ContractError("journal-prior-state-mismatch")
        return {"outcome": "rolled-back", "error": None, "state": current, "authority_state_mutated": False}

    committed_record = normalized[1]
    committed = committed_record["state_after"]
    assert committed is not None
    if normalized[-1]["state_after"] != committed:
        raise ContractError("journal-acknowledgement-state-mismatch")
    if current_digest == _sha(committed):
        return {
            "outcome": "clean" if phases[-1] == "acknowledged" else "already-recovered",
            "error": None,
            "state": current,
            "authority_state_mutated": False,
        }
    if current_digest != prior_digest:
        raise ContractError("journal-authority-state-diverged")
    _validate_commit_transition(current, committed, committed_record)
    return {
        "outcome": "recovered-committed",
        "error": None,
        "state": committed,
        "authority_state_mutated": False,
    }


def validate_journal_fixture_case(*, authority_state: Mapping[str, Any], records: Sequence[Mapping[str, Any]], expected: Mapping[str, Any]) -> dict[str, Any]:
    expected = _exact("journal expected result", expected, _EXPECTED_KEYS)
    try:
        result = reconcile_journal(authority_state=authority_state, records=records)
    except ContractError as exc:
        state = copy.deepcopy(dict(authority_state))
        result = {
            "outcome": "reject",
            "error": str(exc),
            "state": state,
            "authority_state_mutated": False,
        }
    state = result["state"]
    actual = {
        "outcome": result["outcome"],
        "error": result["error"],
        "state_version": state["state_version"],
        "seen_attempt_ids": state["seen_attempt_ids"],
        "receipt_count": len(state["receipts"]),
        "state_sha256": _sha(state),
    }
    if actual != dict(expected):
        raise ContractError(
            f"journal fixture outcome mismatch: expected={dict(expected)!r} actual={actual!r}"
        )
    if result["authority_state_mutated"] is not False:
        raise ContractError("journal projection must not mutate authority state")
    return actual
