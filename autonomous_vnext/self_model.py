from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SelfModel:
    capabilities: tuple[str, ...]
    limitations: tuple[str, ...]
    confidence: float
    current_goals: tuple[str, ...] = ()
    current_beliefs: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def with_reflection(self, confidence_delta: float, belief_updates: dict[str, str]) -> SelfModel:
        confidence = min(1.0, max(0.0, self.confidence + confidence_delta))
        beliefs = dict(self.current_beliefs)
        beliefs.update(belief_updates)
        return SelfModel(
            capabilities=self.capabilities,
            limitations=self.limitations,
            confidence=confidence,
            current_goals=self.current_goals,
            current_beliefs=beliefs,
        )


def default_self_model(objective: str) -> SelfModel:
    return SelfModel(
        capabilities=(
            "mission_projection",
            "belief_evolution",
            "tensor_memory_retrieval",
            "sheaf_consistency_checking",
            "uncertainty_reporting",
        ),
        limitations=(
            "deterministic_runtime",
            "no_physical_quantum_execution",
            "no_unapproved_remote_writes",
        ),
        confidence=0.72,
        current_goals=(objective,),
        current_beliefs={"runtime": "deterministic", "memory": "append_only"},
    )
