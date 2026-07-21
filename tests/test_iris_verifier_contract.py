from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from iris_verifier_contract import (
    ContractError,
    assert_privacy_safe_record,
    canonical_json_bytes,
    derive_protected_identifier,
    strict_json_loads,
    validate_profile,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "iris-verifier" / "golden-vectors.json"
SCHEMA = ROOT / "contracts" / "iris-derived-verifier-v0.schema.json"


def _synthetic_bytes(domain: bytes, fixture_id: str) -> bytes:
    return hashlib.sha256(domain + b"\0" + fixture_id.encode("ascii")).digest()


def _manifest() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_golden_vector_is_reproducible() -> None:
    manifest = _manifest()
    vector = manifest["vectors"][0]
    fixture_id = vector["fixture_id"]
    actual = derive_protected_identifier(
        profile=vector["profile"],
        reconstructed_secret=_synthetic_bytes(
            b"QSO_IRIS_SYNTHETIC_RECONSTRUCTED_SECRET", fixture_id
        ),
        key=_synthetic_bytes(b"QSO_IRIS_SYNTHETIC_TEST_KEY", fixture_id),
    )
    assert actual == vector["expected_protected_identifier"]
    assert manifest["synthetic_only"] is True
    assert manifest["production_key_material_present"] is False
    assert manifest["raw_biometric_material_present"] is False


def test_profile_or_key_rotation_is_unlinkable() -> None:
    vector = _manifest()["vectors"][0]
    profile = vector["profile"]
    fixture_id = vector["fixture_id"]
    secret = _synthetic_bytes(
        b"QSO_IRIS_SYNTHETIC_RECONSTRUCTED_SECRET", fixture_id
    )
    key = _synthetic_bytes(b"QSO_IRIS_SYNTHETIC_TEST_KEY", fixture_id)
    original = derive_protected_identifier(
        profile=profile, reconstructed_secret=secret, key=key
    )

    rotated_profile = dict(profile, transform_id="synthetic-transform-1")
    profile_rotated = derive_protected_identifier(
        profile=rotated_profile, reconstructed_secret=secret, key=key
    )
    key_rotated = derive_protected_identifier(
        profile=profile,
        reconstructed_secret=secret,
        key=_synthetic_bytes(b"QSO_IRIS_SYNTHETIC_TEST_KEY_ROTATED", fixture_id),
    )
    assert len({original, profile_rotated, key_rotated}) == 3


def test_strict_json_rejects_duplicate_keys_and_non_finite_numbers() -> None:
    with pytest.raises(ContractError, match="duplicate JSON key"):
        strict_json_loads('{"schema":"a","schema":"b"}')
    with pytest.raises(ContractError, match="non-finite JSON number"):
        strict_json_loads('{"score":NaN}')


def test_profile_validation_fails_closed() -> None:
    profile = _manifest()["vectors"][0]["profile"]
    assert validate_profile(profile) == profile

    with pytest.raises(ContractError, match="single-eye"):
        validate_profile(dict(profile, subject_scope="both-eyes"))
    with pytest.raises(ContractError, match="memory-only"):
        validate_profile(dict(profile, raw_capture_retention="persistent"))
    with pytest.raises(ContractError, match="unknown profile fields"):
        validate_profile(dict(profile, network_endpoint="https://example.invalid"))
    with pytest.raises(ContractError, match="max_helper_data_bytes"):
        validate_profile(dict(profile, max_helper_data_bytes=True))


def test_privacy_guard_rejects_prohibited_material_at_any_depth() -> None:
    safe = {
        "schema": "qso.iris-match-proposal.v0",
        "protected_identifier_digest": "0" * 64,
        "evidence": [{"helper_data_digest": "1" * 64}],
    }
    assert_privacy_safe_record(safe)

    for forbidden in (
        "raw_image",
        "iris_code",
        "feature-vector",
        "reconstructed_secret",
        "hmac_key",
    ):
        with pytest.raises(ContractError, match="prohibited material"):
            assert_privacy_safe_record({"nested": {forbidden: "not-allowed"}})


def test_schema_is_closed_and_separates_record_types() -> None:
    schema = strict_json_loads(SCHEMA.read_text(encoding="utf-8"))
    definitions = schema["$defs"]
    expected = {
        "derivationProfile",
        "verificationAttempt",
        "matchProposal",
        "revocationRecord",
        "recoveryReference",
    }
    assert expected <= definitions.keys()
    for name in expected:
        assert definitions[name]["additionalProperties"] is False


def test_fixture_contains_no_embedded_key_or_reconstructed_secret() -> None:
    manifest = _manifest()
    assert_privacy_safe_record(manifest)
    serialized = canonical_json_bytes(manifest)
    assert b"synthetic_key" not in serialized
    assert b"reconstructed_secret" not in serialized
    assert b"raw_image" not in serialized


def test_short_key_or_secret_is_rejected() -> None:
    profile = _manifest()["vectors"][0]["profile"]
    with pytest.raises(ContractError, match="at least 32 bytes"):
        derive_protected_identifier(
            profile=profile, reconstructed_secret=b"short", key=b"k" * 32
        )
    with pytest.raises(ContractError, match="at least 32 bytes"):
        derive_protected_identifier(
            profile=profile, reconstructed_secret=b"s" * 32, key=b"short"
        )
