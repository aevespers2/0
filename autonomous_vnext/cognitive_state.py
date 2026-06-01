from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from autonomous_vnext.cognitive_hilbert import CognitiveTensorBackbone


@dataclass(frozen=True)
class SubsystemState:
    name: str
    amplitudes: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("subsystem state name is required")
        if not self.amplitudes:
            raise ValueError("at least one amplitude is required")

    @property
    def dimension(self) -> int:
        return len(self.amplitudes)

    @property
    def norm(self) -> float:
        return sqrt(sum(value * value for value in self.amplitudes))

    def normalized(self) -> SubsystemState:
        norm = self.norm
        if norm == 0:
            raise ValueError("zero-norm state cannot be normalized")
        return SubsystemState(self.name, tuple(value / norm for value in self.amplitudes))


@dataclass(frozen=True)
class CognitiveState:
    backbone: CognitiveTensorBackbone
    subsystems: tuple[SubsystemState, ...]

    def __post_init__(self) -> None:
        expected = {space.name: space.dimension for space in self.backbone.subsystems}
        observed = {state.name: state.dimension for state in self.subsystems}
        if expected != observed:
            raise ValueError(f"state dimensions do not match backbone: expected={expected} observed={observed}")

    @property
    def labels(self) -> tuple[str, ...]:
        return tuple(state.name for state in self.subsystems)

    def subsystem(self, name: str) -> SubsystemState:
        for state in self.subsystems:
            if state.name == name:
                return state
        raise KeyError(name)

    def replace(self, state: SubsystemState) -> CognitiveState:
        updated = tuple(state if item.name == state.name else item for item in self.subsystems)
        return CognitiveState(self.backbone, updated)

    def normalized(self) -> CognitiveState:
        return CognitiveState(self.backbone, tuple(state.normalized() for state in self.subsystems))


def basis_state(backbone: CognitiveTensorBackbone, active_indices: dict[str, int] | None = None) -> CognitiveState:
    active_indices = active_indices or {}
    states: list[SubsystemState] = []
    for space in backbone.subsystems:
        active = active_indices.get(space.name, 0)
        if active < 0 or active >= space.dimension:
            raise ValueError(f"active index out of range for {space.name}")
        amplitudes = tuple(1.0 if index == active else 0.0 for index in range(space.dimension))
        states.append(SubsystemState(space.name, amplitudes))
    return CognitiveState(backbone, tuple(states))
