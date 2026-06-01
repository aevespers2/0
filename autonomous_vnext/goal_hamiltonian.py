from __future__ import annotations

from dataclasses import dataclass

from autonomous_vnext.cognitive_state import CognitiveState


@dataclass(frozen=True)
class GoalHamiltonian:
    subsystem: str
    energies: tuple[float, ...]

    def expected_energy(self, state: CognitiveState) -> float:
        target = state.subsystem(self.subsystem)
        if len(self.energies) != target.dimension:
            raise ValueError("energies must match subsystem dimension")
        return sum((amplitude * amplitude) * energy for amplitude, energy in zip(target.amplitudes, self.energies, strict=True))

    def ground_index(self) -> int:
        return min(range(len(self.energies)), key=lambda index: (self.energies[index], index))
