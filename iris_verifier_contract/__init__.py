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

__all__ = [
    "ContractError",
    "assert_privacy_safe_record",
    "atomic_state_sha256",
    "canonical_json_bytes",
    "derive_protected_identifier",
    "project_atomic_consume_and_record",
    "screen_synthetic_attempt_context",
    "strict_json_loads",
    "validate_atomic_fixture_case",
    "validate_atomic_operation",
    "validate_atomic_state",
    "validate_profile",
]
