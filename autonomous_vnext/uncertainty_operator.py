from __future__ import annotations

from dataclasses import dataclass
from math import log2

from autonomous_vnext.cognitive_state import CognitiveState


@dataclass(frozen=True)
class UncertaintyReport:
    subsystem: str
    entropy_bits: float
    confidence: float


def subsystem_entropy(state: CognitiveState, subsystem: str) -> UncertaintyReport:
    target = state.subsystem(subsystem)
    probabilities = [value * value for value in target.normalized().amplitudes]
    entropy = -sum(probability * log2(probability) for probability in probabilities if probability > 0)
    max_entropy = log2(target.dimension)
    confidence = 1.0 if max_entropy == 0 else 1.0 - (entropy / max_entropy)
    return UncertaintyReport(subsystem=target.name, entropy_bits=entropy, confidence=confidence)
