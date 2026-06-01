from __future__ import annotations

from dataclasses import dataclass

from autonomous_vnext.self_model import SelfModel


@dataclass(frozen=True)
class ReflectionResult:
    expected: dict[str, object]
    observed: dict[str, object]
    deltas: dict[str, object]
    confidence_delta: float
    updated_self_model: SelfModel


def reflect(expected: dict[str, object], observed: dict[str, object], self_model: SelfModel) -> ReflectionResult:
    deltas: dict[str, object] = {}
    confidence_delta = 0.0

    for key, expected_value in expected.items():
        observed_value = observed.get(key)
        if observed_value != expected_value:
            deltas[key] = {"expected": expected_value, "observed": observed_value}
            confidence_delta -= 0.05
        else:
            confidence_delta += 0.02

    if observed.get("mesh_consistent") is False:
        confidence_delta -= 0.1
    if float(observed.get("risk_confidence", 0.0)) > 0.8:
        confidence_delta += 0.03

    updated = self_model.with_reflection(
        confidence_delta=confidence_delta,
        belief_updates={
            "last_reflection": "matched" if not deltas else "diverged",
            "mesh_consistent": str(observed.get("mesh_consistent")),
        },
    )
    return ReflectionResult(
        expected=expected,
        observed=observed,
        deltas=deltas,
        confidence_delta=confidence_delta,
        updated_self_model=updated,
    )
