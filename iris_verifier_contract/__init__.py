"""Contract-only primitives for synthetic iris-verifier conformance tests."""

from .atomicity import (
    atomic_state_sha256,
    project_atomic_consume_and_record,
    validate_atomic_fixture_case,
    validate_atomic_operation,
    validate_atomic_state,
)
from .contract import (
    ContractError,
    assert_privacy_safe_record,
    canonical_json_bytes,
    derive_protected_identifier,
    screen_synthetic_attempt_context,
    strict_json_loads,
    validate_profile,
)
from .journal import (
    journal_record_sha256,
    reconcile_journal,
    validate_journal_fixture_case,
    validate_journal_record,
)

__all__ = [
    "ContractError",
    "assert_privacy_safe_record",
    "atomic_state_sha256",
    "canonical_json_bytes",
    "derive_protected_identifier",
    "journal_record_sha256",
    "project_atomic_consume_and_record",
    "reconcile_journal",
    "screen_synthetic_attempt_context",
    "strict_json_loads",
    "validate_atomic_fixture_case",
    "validate_atomic_operation",
    "validate_atomic_state",
    "validate_journal_fixture_case",
    "validate_journal_record",
    "validate_profile",
]
