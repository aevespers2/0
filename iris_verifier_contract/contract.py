from __future__ import annotations

import hashlib
import hmac
import json
import re
from datetime import datetime, timezone
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
_ATTEMPT_KEYS = {
    "schema",
    "attempt_id",
    "profile_id",
    "generation",
    "subject_ref",
    "eye_side",
    "device_ref",
    "capture_digest",
    "helper_data_digest",
    "created_at",
    "status",
}
_CONTEXT_KEYS = {
    "expected_profile_id",
    "current_generation",
    "expected_subject_ref",
    "expected_eye_side",
    "expected_device_ref",
    "expected_helper_data_digest",
    "now",
    "max_age_seconds",
    "seen_attempt_ids",
    "revoked_profile_ids",
    "replacement_profile_id",
    "recovery_state",
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
    if isinstance(record, float) and (
        record != record or record in (float("inf"), float("-inf"))
    ):
        raise ContractError(f"non-finite value at {path}")


def require_sha256(name: str, value: Any) -> str:
    """Validate a lowercase SHA-256 hex digest for record-level checks."""

    if not isinstance(value, str) or not _HEX_64.fullmatch(value):
        raise ContractError(f"{name} must be a lowercase SHA-256 digest")
    return value


def _require_exact_keys(
    name: str, value: Mapping[str, Any], expected: set[str]
) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{name} must be an object")
    keys = set(value)
    missing = expected - keys
    unknown = keys - expected
    if missing:
        raise ContractError(f"missing {name} fields: {sorted(missing)}")
    if unknown:
        raise ContractError(f"unknown {name} fields: {sorted(unknown)}")
    return dict(value)


def _parse_utc_timestamp(name: str, value: Any) -> datetime:
    if not isinstance(value, str):
        raise ContractError(f"{name} must be an RFC 3339 timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ContractError(f"{name} must be an RFC 3339 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ContractError(f"{name} must include a UTC offset")
    return parsed.astimezone(timezone.utc)


def screen_synthetic_attempt_context(
    *,
    attempt: Mapping[str, Any],
    context: Mapping[str, Any],
) -> dict[str, Any]:
    """Fail closed on synthetic attempt/context mismatches before proposal use.

    This is a deterministic contract screen for synthetic fixtures. It does not
    perform biometric comparison, enrollment, authentication, capability
    issuance, device control, or canonical identity disposition.
    """

    normalized_attempt = _require_exact_keys("attempt", attempt, _ATTEMPT_KEYS)
    normalized_context = _require_exact_keys("context", context, _CONTEXT_KEYS)

    if normalized_attempt["schema"] != "qso.iris-verification-attempt.v0":
        raise ContractError("unsupported attempt schema")
    for field in ("attempt_id", "profile_id", "subject_ref", "device_ref"):
        _require_identifier(field, normalized_attempt[field])
    generation = normalized_attempt["generation"]
    if type(generation) is not int or generation < 1:
        raise ContractError("generation must be a positive integer")
    if normalized_attempt["eye_side"] not in {"left", "right"}:
        raise ContractError("eye_side must be left or right")
    require_sha256("capture_digest", normalized_attempt["capture_digest"])
    require_sha256("helper_data_digest", normalized_attempt["helper_data_digest"])
    created_at = _parse_utc_timestamp("created_at", normalized_attempt["created_at"])
    if normalized_attempt["status"] != "proposal-created":
        raise ContractError("attempt status is not proposal-created")

    for field in (
        "expected_profile_id",
        "expected_subject_ref",
        "expected_device_ref",
    ):
        _require_identifier(field, normalized_context[field])
    if normalized_context["expected_eye_side"] not in {"left", "right"}:
        raise ContractError("expected_eye_side must be left or right")
    require_sha256(
        "expected_helper_data_digest",
        normalized_context["expected_helper_data_digest"],
    )
    current_generation = normalized_context["current_generation"]
    if type(current_generation) is not int or current_generation < 1:
        raise ContractError("current_generation must be a positive integer")
    max_age_seconds = normalized_context["max_age_seconds"]
    if type(max_age_seconds) is not int or not 1 <= max_age_seconds <= 86_400:
        raise ContractError("max_age_seconds must be an integer in [1, 86400]")
    now = _parse_utc_timestamp("now", normalized_context["now"])

    seen_attempt_ids = normalized_context["seen_attempt_ids"]
    revoked_profile_ids = normalized_context["revoked_profile_ids"]
    if not isinstance(seen_attempt_ids, list) or not all(
        isinstance(value, str) and _IDENTIFIER.fullmatch(value)
        for value in seen_attempt_ids
    ):
        raise ContractError("seen_attempt_ids must be normalized identifiers")
    if len(seen_attempt_ids) != len(set(seen_attempt_ids)):
        raise ContractError("seen_attempt_ids must not contain duplicates")
    if not isinstance(revoked_profile_ids, list) or not all(
        isinstance(value, str) and _IDENTIFIER.fullmatch(value)
        for value in revoked_profile_ids
    ):
        raise ContractError("revoked_profile_ids must be normalized identifiers")
    if len(revoked_profile_ids) != len(set(revoked_profile_ids)):
        raise ContractError("revoked_profile_ids must not contain duplicates")

    replacement_profile_id = normalized_context["replacement_profile_id"]
    if replacement_profile_id is not None:
        _require_identifier("replacement_profile_id", replacement_profile_id)
    recovery_state = normalized_context["recovery_state"]
    if recovery_state not in {"normal", "recovery-required", "recovery-completed"}:
        raise ContractError("unsupported recovery_state")
    if recovery_state == "recovery-completed" and replacement_profile_id is None:
        raise ContractError("recovery-completed requires a replacement profile")

    profile_id = normalized_attempt["profile_id"]
    if profile_id in revoked_profile_ids:
        raise ContractError("profile-revoked")
    if replacement_profile_id is not None and profile_id != replacement_profile_id:
        raise ContractError("profile-replaced")
    if recovery_state == "recovery-required":
        raise ContractError("recovery-not-complete")
    if profile_id != normalized_context["expected_profile_id"]:
        raise ContractError("profile-mismatch")
    if generation < current_generation:
        raise ContractError("stale-generation")
    if generation > current_generation:
        raise ContractError("future-generation")
    if normalized_attempt["subject_ref"] != normalized_context["expected_subject_ref"]:
        raise ContractError("subject-mismatch")
    if normalized_attempt["eye_side"] != normalized_context["expected_eye_side"]:
        raise ContractError("eye-side-mismatch")
    if normalized_attempt["device_ref"] != normalized_context["expected_device_ref"]:
        raise ContractError("device-mismatch")
    if (
        normalized_attempt["helper_data_digest"]
        != normalized_context["expected_helper_data_digest"]
    ):
        raise ContractError("helper-data-digest-mismatch")
    if normalized_attempt["attempt_id"] in seen_attempt_ids:
        raise ContractError("attempt-replay")

    age_seconds = (now - created_at).total_seconds()
    if age_seconds < 0:
        raise ContractError("future-attempt")
    if age_seconds > max_age_seconds:
        raise ContractError("stale-attempt")

    assert_privacy_safe_record(normalized_attempt)
    assert_privacy_safe_record(normalized_context)
    return normalized_attempt
