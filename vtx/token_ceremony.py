from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .gateway_policy import GatewayGrant, GatewayRequest, authorize


@dataclass(frozen=True)
class CeremonyCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class CeremonyReport:
    ready_for_live_drill: bool
    checks: tuple[CeremonyCheck, ...]


def dry_run(grant: GatewayGrant, requests: Iterable[tuple[str, GatewayRequest, bool]]) -> CeremonyReport:
    """Exercise gateway policy without creating or using a credential.

    Each request tuple contains a check name, a request, and the expected allowed
    result. This validates policy wiring only; it does not claim that GitHub-side
    branch protection, secret storage, or revocation controls are operational.
    """
    checks: list[CeremonyCheck] = []
    for name, request, expected_allowed in requests:
        decision = authorize(request, grant)
        passed = decision.allowed is expected_allowed
        checks.append(CeremonyCheck(
            name=name,
            passed=passed,
            detail=f"expected={expected_allowed}; actual={decision.allowed}; reason={decision.reason}",
        ))
    return CeremonyReport(
        ready_for_live_drill=bool(checks) and all(check.passed for check in checks),
        checks=tuple(checks),
    )
