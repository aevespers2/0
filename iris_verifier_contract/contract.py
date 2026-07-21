from __future__ import annotations

import hashlib
import hmac
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any


class ContractError(ValueError):
    """Raised when a contract or privacy invariant is violated."""


_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
_IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9._:-]{2,127}$")
_PROFILE_KEYS = {
    "schema",
    "profile_id",
    "extractor_version",
    "transform_id",
    "domain",
    "key_id",
    "subject_scope",
    "max_helper_data_bytes",
    "raw_capture_retention",
    "output_algorithm",
}
_FORBIDDEN_RECORD_KEYS = {
    "raw_image",
    "raw_eye_image",
    "iris_code",
    "unprotected_feature_vector",
    "feature_vector",
    "reconstructed_secret",
    "live_biometric_sample",
    "biometric_sample",
    "key_material",
    "hmac_key",
    "secret",
}


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_non_finite(value: str) -> None:
    raise ContractError(f"non-finite JSON number: {value}")


def strict_json_loads(text: str) -> Any:
    """Parse UTF-8 JSON while rejecting duplicate keys and non-finite numbers."""

    if not isinstance(text, str):
        raise ContractError("JSON input must be text")
    try:
        return json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_non_finite,
        )
    except ContractError:
        raise
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ContractError(f"invalid JSON: {exc}") from exc


def canonical_json_bytes(value: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes for contract hashing."""

    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractError(f"value is not canonical-JSON compatible: {exc}") from exc


def _require_identifier(name: str, value: Any) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise ContractError(f"{name} must be a normalized identifier")
    return value


def validate_profile(profile: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the proposed derivation profile without activating enrollment."""

    if not isinstance(profile, Mapping):
        raise ContractError("profile must be an object")
    keys = set(profile)
    missing = _PROFILE_KEYS - keys
    unknown = keys - _PROFILE_KEYS
    if missing:
        raise ContractError(f"missing profile fields: {sorted(missing)}")
    if unknown:
        raise ContractError(f"unknown profile fields: {sorted(unknown)}")

    normalized = dict(profile)
    if normalized["schema"] != "qso.iris-derivation-profile.v0":
        raise ContractError("unsupported profile schema")
    _require_identifier("profile_id", normalized["profile_id"])
    _require_identifier("extractor_version", normalized["extractor_version"])
    _require_identifier("transform_id", normalized["transform_id"])
    _require_identifier("key_id", normalized["key_id"])
    if normalized["domain"] != "qso.iris.local-verifier.v0":
        raise ContractError("unexpected derivation domain")
    if normalized["subject_scope"] != "single-eye":
        raise ContractError("subject scope must remain single-eye")
    if normalized["raw_capture_retention"] != "memory-only":
        raise ContractError("raw capture retention must remain memory-only")
    if normalized["output_algorithm"] != "HMAC-SHA-256":
        raise ContractError("unsupported output algorithm")
    maximum = normalized["max_helper_data_bytes"]
    if type(maximum) is not int or not 1 <= maximum <= 1_048_576:
        raise ContractError("max_helper_data_bytes must be an integer in [1, 1048576]")
    return normalized


def derive_protected_identifier(
    *,
    profile: Mapping[str, Any],
    reconstructed_secret: bytes,
    key: bytes,
) -> str:
    """Derive a protected identifier from already reconstructed in-memory bytes.

    This function does not process captures, perform liveness checks, store helper
    data, enroll a subject, or make an authentication or capability decision.
    """

    normalized = validate_profile(profile)
    if not isinstance(reconstructed_secret, bytes) or len(reconstructed_secret) < 32:
        raise ContractError("reconstructed_secret must contain at least 32 bytes")
    if not isinstance(key, bytes) or len(key) < 32:
        raise ContractError("key must contain at least 32 bytes")
    message = (
        b"qso.iris.local-verifier.v0\0"
        + canonical_json_bytes(normalized)
        + b"\0"
        + reconstructed_secret
    )
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def assert_privacy_safe_record(record: Any, *, path: str = "$") -> None:
    """Reject record structures that could carry prohibited biometric material."""

    if isinstance(record, Mapping):
        for key, value in record.items():
            if not isinstance(key, str):
                raise ContractError(f"non-string record key at {path}")
            normalized_key = key.strip().lower().replace("-", "_")
            if normalized_key in _FORBIDDEN_RECORD_KEYS:
                raise ContractError(f"prohibited material field at {path}.{key}")
            assert_privacy_safe_record(value, path=f"{path}.{key}")
        return
    if isinstance(record, Sequence) and not isinstance(record, (str, bytes, bytearray)):
        for index, value in enumerate(record):
            assert_privacy_safe_record(value, path=f"{path}[{index}]")
        return
    if isinstance(record, float) and (record != record or record in (float("inf"), float("-inf"))):
        raise ContractError(f"non-finite value at {path}")


def require_sha256(name: str, value: Any) -> str:
    """Validate a lowercase SHA-256 hex digest for record-level checks."""

    if not isinstance(value, str) or not _HEX_64.fullmatch(value):
        raise ContractError(f"{name} must be a lowercase SHA-256 digest")
    return value
