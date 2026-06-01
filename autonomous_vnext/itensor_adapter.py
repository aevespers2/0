from __future__ import annotations

from dataclasses import dataclass
from importlib.util import find_spec
from typing import Any


class ITensorUnavailableError(RuntimeError):
    """Raised when ITensor bindings are not available in the runtime."""


@dataclass(frozen=True)
class ITensorPlanScore:
    plan_id: str
    score: float


def itensor_available() -> bool:
    """Return True when an ITensor Python module is importable."""
    return find_spec("itensor") is not None


def require_itensor() -> None:
    if not itensor_available():
        raise ITensorUnavailableError(
            "ITensor Python bindings are not installed. "
            "Install an ITensor package to enable tensor-network scoring."
        )


def score_plans_with_itensor(plan_vectors: dict[str, list[float]], weights: list[float]) -> list[ITensorPlanScore]:
    """
    Score plan vectors with a weighted contraction.

    This function currently uses a deterministic dot-product fallback while enforcing
    ITensor availability as a runtime dependency gate. It provides a stable surface
    for replacing the fallback with native ITensor tensor contractions.
    """
    require_itensor()

    if not weights:
        raise ValueError("weights must not be empty")

    scored: list[ITensorPlanScore] = []
    for plan_id, vector in plan_vectors.items():
        if len(vector) != len(weights):
            raise ValueError(f"vector length mismatch for plan '{plan_id}'")
        score = float(sum(v * w for v, w in zip(vector, weights)))
        scored.append(ITensorPlanScore(plan_id=plan_id, score=score))

    return sorted(scored, key=lambda item: item.score)


def best_plan_with_itensor(plan_vectors: dict[str, list[float]], weights: list[float]) -> ITensorPlanScore:
    scores = score_plans_with_itensor(plan_vectors=plan_vectors, weights=weights)
    return scores[0]
