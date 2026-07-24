from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


TRUST_CORE_REPOSITORY = "aevespers2/1"
ALLOWED_OPERATIONS = frozenset({
    "repository.read",
    "contents.read",
    "contents.write",
    "branch.create",
    "pull_request.create",
    "pull_request.update",
    "pull_request.read",
    "checks.read",
})


@dataclass(frozen=True)
class GatewayRequest:
    actor: str
    repository: str
    operation: str
    branch: str | None
    payload_digest: str
    vtx_envelope_id: str
    nonce: str


@dataclass(frozen=True)
class GatewayGrant:
    actor: str
    repositories: FrozenSet[str]
    operations: FrozenSet[str]
    branch_prefix: str
    active: bool = True


@dataclass(frozen=True)
class GatewayDecision:
    allowed: bool
    reason: str


def authorize(request: GatewayRequest, grant: GatewayGrant) -> GatewayDecision:
    """Authorize a structured GitHub request without exposing a token."""
    if not grant.active:
        return GatewayDecision(False, "grant_inactive")
    if request.actor != grant.actor:
        return GatewayDecision(False, "actor_mismatch")
    if request.repository == TRUST_CORE_REPOSITORY:
        return GatewayDecision(False, "trust_core_denied")
    if request.repository not in grant.repositories:
        return GatewayDecision(False, "repository_denied")
    if request.operation not in ALLOWED_OPERATIONS or request.operation not in grant.operations:
        return GatewayDecision(False, "operation_denied")
    if not request.vtx_envelope_id or not request.nonce:
        return GatewayDecision(False, "missing_vtx_binding")
    if not request.payload_digest.startswith(("sha256:", "blake3:")):
        return GatewayDecision(False, "invalid_payload_digest")
    if request.operation in {"contents.write", "branch.create", "pull_request.create", "pull_request.update"}:
        if not request.branch or not request.branch.startswith(grant.branch_prefix):
            return GatewayDecision(False, "branch_denied")
    return GatewayDecision(True, "allowed")
