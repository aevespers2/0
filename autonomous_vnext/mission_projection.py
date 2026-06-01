from __future__ import annotations

from dataclasses import dataclass

from autonomous_vnext.cognitive_state import CognitiveState, SubsystemState


@dataclass(frozen=True)
class MissionProjection:
    objective_terms: tuple[str, ...]
    subsystem: str = "goals"

    def project(self, state: CognitiveState) -> CognitiveState:
        target = state.subsystem(self.subsystem)
        active = min(len(self.objective_terms), target.dimension)
        if active == 0:
            raise ValueError("at least one objective term is required")
        amplitudes = tuple(1.0 if index < active else 0.0 for index in range(target.dimension))
        return state.replace(SubsystemState(target.name, amplitudes).normalized())
