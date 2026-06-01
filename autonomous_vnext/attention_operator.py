from __future__ import annotations

from dataclasses import dataclass

from autonomous_vnext.cognitive_state import CognitiveState, SubsystemState


@dataclass(frozen=True)
class AttentionOperator:
    subsystem: str
    weights: tuple[float, ...]
    renormalize: bool = True

    def apply(self, state: CognitiveState) -> CognitiveState:
        target = state.subsystem(self.subsystem)
        if len(self.weights) != target.dimension:
            raise ValueError("attention weights must match subsystem dimension")
        updated = SubsystemState(
            target.name,
            tuple(value * weight for value, weight in zip(target.amplitudes, self.weights, strict=True)),
        )
        if self.renormalize:
            updated = updated.normalized()
        return state.replace(updated)


def uniform_attention(subsystem: str, dimension: int) -> AttentionOperator:
    if dimension < 1:
        raise ValueError("dimension must be positive")
    return AttentionOperator(subsystem, tuple(1.0 for _ in range(dimension)))
