from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


def canonical_json(value: Mapping[str, Any]) -> bytes:
    """Return deterministic UTF-8 JSON suitable for hashing or signing."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest_payload(payload: bytes) -> str:
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


@dataclass(frozen=True)
class VTXEnvelope:
    envelope_id: str
    issued_at: str
    expires_at: str
    nonce: str
    issuer: str
    repository: Mapping[str, Any]
    operation: str
    target: Mapping[str, Any]
    payload_digest: str
    policy_id: str
    claims: Mapping[str, Any] = field(default_factory=dict)
    signature: Mapping[str, Any] | None = None
    version: str = "vtx.envelope.v1"

    def to_dict(self, *, include_signature: bool = True) -> dict[str, Any]:
        data = asdict(self)
        if not include_signature:
            data.pop("signature", None)
        elif data.get("signature") is None:
            data.pop("signature", None)
        return data

    def signing_bytes(self) -> bytes:
        return canonical_json(self.to_dict(include_signature=False))

    @staticmethod
    def parse_time(value: str) -> datetime:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("VTX timestamps must include a timezone")
        return parsed.astimezone(timezone.utc)
