from __future__ import annotations

from dataclasses import dataclass
from math import prod

from autonomous_vnext.itensor_adapter import ITensorUnavailableError, require_itensor


@dataclass(frozen=True)
class HilbertSpaceSpec:
    name: str
    dimensions: tuple[int, ...]

    @property
    def rank(self) -> int:
        return len(self.dimensions)

    @property
    def total_dimension(self) -> int:
        return int(prod(self.dimensions))


@dataclass(frozen=True)
class CognitiveTensorBackbone:
    subsystems: tuple[HilbertSpaceSpec, ...]

    @property
    def rank(self) -> int:
        return sum(s.rank for s in self.subsystems)

    @property
    def total_dimension(self) -> int:
        return int(prod(s.total_dimension for s in self.subsystems))


def build_cognitive_backbone(subsystems: list[HilbertSpaceSpec]) -> CognitiveTensorBackbone:
    if not subsystems:
        raise ValueError("at least one subsystem is required")
    for sub in subsystems:
        if not sub.dimensions:
            raise ValueError(f"subsystem '{sub.name}' has empty dimensions")
        if any(d <= 0 for d in sub.dimensions):
            raise ValueError(f"subsystem '{sub.name}' has non-positive dimensions")
    return CognitiveTensorBackbone(subsystems=tuple(subsystems))


def require_itensor_backbone(backbone: CognitiveTensorBackbone) -> None:
    """
    Gate execution on ITensor availability for tensor-network based cognition.

    Note: this scaffolding models high-dimensional tensor spaces for planning and
    representation. It does not itself provide quantum hardware execution.
    """
    if backbone.total_dimension <= 0:
        raise ValueError("backbone has invalid dimension")
    try:
        require_itensor()
    except ITensorUnavailableError as exc:
        raise ITensorUnavailableError(
            "ITensor is required for cognitive backbone execution. "
            "Install ITensor bindings and configure tensor contractions for runtime use."
        ) from exc
