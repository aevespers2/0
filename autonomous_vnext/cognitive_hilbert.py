from __future__ import annotations

from dataclasses import dataclass
from math import prod

from autonomous_vnext.itensor_adapter import ITensorUnavailableError, itensor_available


@dataclass(frozen=True)
class HilbertSpaceSpec:
    name: str
    dimension: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("subsystem name is required")
        if self.dimension < 2:
            raise ValueError("subsystem dimension must be at least 2")


@dataclass(frozen=True)
class CognitiveTensorBackbone:
    subsystems: tuple[HilbertSpaceSpec, ...]

    @property
    def rank(self) -> int:
        return len(self.subsystems)

    @property
    def total_dimension(self) -> int:
        return prod(space.dimension for space in self.subsystems)

    @property
    def labels(self) -> tuple[str, ...]:
        return tuple(space.name for space in self.subsystems)


def build_cognitive_backbone(specs: list[tuple[str, int]]) -> CognitiveTensorBackbone:
    if not specs:
        raise ValueError("at least one subsystem is required")
    return CognitiveTensorBackbone(tuple(HilbertSpaceSpec(name, dimension) for name, dimension in specs))


def require_itensor_backbone(backbone: CognitiveTensorBackbone) -> CognitiveTensorBackbone:
    if not itensor_available():
        raise ITensorUnavailableError("ITensor is required for tensor-backed cognitive execution")
    return backbone
