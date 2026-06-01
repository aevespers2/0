from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CandidatePlan:
    plan_id: str
    steps: tuple[str, ...]
    risk_score: int


def score_risk(steps: tuple[str, ...]) -> int:
    score = 0
    for step in steps:
        lowered = step.lower()
        if any(word in lowered for word in ("push", "deploy", "publish")):
            score += 8
        elif any(word in lowered for word in ("delete", "reset --hard", "rm -rf")):
            score += 13
        elif any(word in lowered for word in ("edit", "write", "patch")):
            score += 3
        elif any(word in lowered for word in ("test", "lint", "inspect", "read")):
            score += 1
        else:
            score += 2
    return score


def generate_candidate_plans(objective: str) -> list[CandidatePlan]:
    objective = objective.strip() or "complete objective"
    candidates = [
        ("plan-read-first", ("inspect repository", f"plan changes for {objective}", "run focused tests")),
        ("plan-implement", ("inspect repository", f"patch implementation for {objective}", "run focused tests")),
        ("plan-ship", ("inspect repository", f"patch implementation for {objective}", "run full tests", "push changes")),
    ]
    return [
        CandidatePlan(plan_id=plan_id, steps=steps, risk_score=score_risk(steps))
        for plan_id, steps in candidates
    ]


def select_lowest_risk_plan(plans: list[CandidatePlan]) -> CandidatePlan:
    if not plans:
        raise ValueError("at least one plan is required")
    return sorted(plans, key=lambda plan: (plan.risk_score, plan.plan_id))[0]
