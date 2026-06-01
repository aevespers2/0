from __future__ import annotations

from dataclasses import dataclass

from autonomous_vnext.attention_operator import AttentionOperator
from autonomous_vnext.cognitive_state import CognitiveState, SubsystemState


@dataclass(frozen=True)
class BeliefObservation:
    subsystem: str
    evidence: tuple[float, ...]
    learning_rate: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.learning_rate <= 1.0:
            raise ValueError("learning_rate must be between 0 and 1")


@dataclass(frozen=True)
class BeliefEvolutionOperator:
    observations: tuple[BeliefObservation, ...]
    attention: tuple[AttentionOperator, ...] = ()

    def evolve(self, state: CognitiveState) -> CognitiveState:
        evolved = state
        for observation in self.observations:
            target = evolved.subsystem(observation.subsystem)
            if len(observation.evidence) != target.dimension:
                raise ValueError("observation evidence must match subsystem dimension")
            rate = observation.learning_rate
            updated = SubsystemState(
                target.name,
                tuple(
                    ((1.0 - rate) * current) + (rate * evidence)
                    for current, evidence in zip(target.amplitudes, observation.evidence, strict=True)
                ),
            ).normalized()
            evolved = evolved.replace(updated)
        for operator in self.attention:
            evolved = operator.apply(evolved)
        return evolved
