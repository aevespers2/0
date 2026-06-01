from __future__ import annotations

from autonomous_vnext.planner import CandidatePlan


class ITensorUnavailableError(RuntimeError):
    pass


def itensor_available() -> bool:
    try:
        import itensor  # type: ignore  # noqa: F401
    except Exception:
        return False
    return True


def score_plans_with_itensor(plans: list[CandidatePlan]) -> list[tuple[CandidatePlan, float]]:
    if not itensor_available():
        raise ITensorUnavailableError("Python ITensor bindings are unavailable")
    return [(plan, 1.0 / (1.0 + plan.risk_score)) for plan in plans]


def best_plan_with_itensor(plans: list[CandidatePlan]) -> CandidatePlan:
    scored = score_plans_with_itensor(plans)
    if not scored:
        raise ValueError("at least one plan is required")
    return sorted(scored, key=lambda item: (-item[1], item[0].plan_id))[0][0]
