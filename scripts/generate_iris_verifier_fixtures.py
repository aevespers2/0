from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from iris_verifier_contract import (  # noqa: E402
    canonical_json_bytes,
    derive_protected_identifier,
    strict_json_loads,
)


_PROFILE = {
    "schema": "qso.iris-derivation-profile.v0",
    "profile_id": "iris-profile-synthetic-v0",
    "extractor_version": "synthetic-extractor-0",
    "transform_id": "synthetic-transform-0",
    "domain": "qso.iris.local-verifier.v0",
    "key_id": "synthetic-key-slot-0",
    "subject_scope": "single-eye",
    "max_helper_data_bytes": 4096,
    "raw_capture_retention": "memory-only",
    "output_algorithm": "HMAC-SHA-256",
}


def _synthetic_bytes(domain: bytes, fixture_id: str) -> bytes:
    """Produce deterministic, public, non-secret bytes for conformance only."""

    return hashlib.sha256(domain + b"\0" + fixture_id.encode("ascii")).digest()


def build_manifest() -> dict[str, Any]:
    fixture_id = "vector-001"
    synthetic_key = _synthetic_bytes(b"QSO_IRIS_SYNTHETIC_TEST_KEY", fixture_id)
    synthetic_secret = _synthetic_bytes(
        b"QSO_IRIS_SYNTHETIC_RECONSTRUCTED_SECRET", fixture_id
    )
    protected_identifier = derive_protected_identifier(
        profile=_PROFILE,
        reconstructed_secret=synthetic_secret,
        key=synthetic_key,
    )
    return {
        "schema": "qso.iris-synthetic-golden-vectors.v0",
        "synthetic_only": True,
        "production_key_material_present": False,
        "raw_biometric_material_present": False,
        "vectors": [
            {
                "fixture_id": fixture_id,
                "profile": _PROFILE,
                "synthetic_input_derivation": "domain-separated-sha256-labels",
                "expected_protected_identifier": protected_identifier,
            }
        ],
    }


def render_manifest() -> str:
    return json.dumps(build_manifest(), indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if bool(args.check) == bool(args.output):
        parser.error("provide exactly one of --check or --output")

    rendered = render_manifest()
    if args.check:
        current = strict_json_loads(args.check.read_text(encoding="utf-8"))
        if canonical_json_bytes(current) != canonical_json_bytes(build_manifest()):
            raise SystemExit(f"fixture drift: {args.check}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
