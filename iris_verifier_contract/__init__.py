"""Contract-only primitives for synthetic iris-verifier conformance tests."""

from .contract import (
    ContractError,
    assert_privacy_safe_record,
    canonical_json_bytes,
    derive_protected_identifier,
    strict_json_loads,
    validate_profile,
)

__all__ = [
    "ContractError",
    "assert_privacy_safe_record",
    "canonical_json_bytes",
    "derive_protected_identifier",
    "strict_json_loads",
    "validate_profile",
]
