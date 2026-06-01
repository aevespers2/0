from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class PolicyViolationError(ValueError):
    """Raised when a command or path violates policy constraints."""


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


class PolicyEvaluator:
    """Deny-by-default command policy evaluator with optional path guardrails."""

    def __init__(self, allow_commands: set[str], allow_path_prefixes: tuple[str, ...] = ()) -> None:
        self.allow_commands = allow_commands
        self.allow_path_prefixes = allow_path_prefixes

    def evaluate(self, command: str, touched_paths: list[str] | None = None) -> PolicyDecision:
        command = command.strip()
        if not command:
            return PolicyDecision(False, "empty command")

        command_name = command.split()[0]
        if command_name not in self.allow_commands:
            return PolicyDecision(False, f"command '{command_name}' not allowlisted")

        if touched_paths and self.allow_path_prefixes:
            for path in touched_paths:
                if not path.startswith(self.allow_path_prefixes):
                    return PolicyDecision(False, f"path '{path}' outside allowed prefixes")

        return PolicyDecision(True, "allowed")

    def require_allowed(self, command: str, touched_paths: list[str] | None = None) -> None:
        decision = self.evaluate(command, touched_paths)
        if not decision.allowed:
            raise PolicyViolationError(decision.reason)


class AuditLogWriter:
    """Append-only JSONL writer for action records."""

    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: dict[str, Any]) -> None:
        line = json.dumps(record, sort_keys=True)
        with self.output_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")


def generate_candidate_plans(objective: str) -> list[dict[str, Any]]:
    """Return three simple plan variants with explicit tradeoffs."""
    return [
        {
            "id": "plan-1",
            "strategy": "smallest patch first",
            "objective": objective,
            "risk": {"blast_radius": 1, "recoverability": 1, "operational_impact": 1, "confidence": 2},
        },
        {
            "id": "plan-2",
            "strategy": "balanced implementation",
            "objective": objective,
            "risk": {"blast_radius": 2, "recoverability": 2, "operational_impact": 2, "confidence": 2},
        },
        {
            "id": "plan-3",
            "strategy": "faster larger batch",
            "objective": objective,
            "risk": {"blast_radius": 3, "recoverability": 3, "operational_impact": 3, "confidence": 3},
        },
    ]


def risk_score(plan: dict[str, Any]) -> int:
    return sum(int(v) for v in plan["risk"].values())


def pick_lowest_risk_plan(objective: str) -> dict[str, Any]:
    plans = generate_candidate_plans(objective)
    return min(plans, key=risk_score)
