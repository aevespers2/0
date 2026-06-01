from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class TensorMemoryRecord:
    record_id: str
    embedding: tuple[float, ...]
    payload: dict[str, str]

    def __post_init__(self) -> None:
        if not self.record_id:
            raise ValueError("record_id is required")
        if not self.embedding:
            raise ValueError("embedding is required")


class TensorMemory:
    def __init__(self, records: tuple[TensorMemoryRecord, ...] = ()) -> None:
        self._records = records

    @property
    def records(self) -> tuple[TensorMemoryRecord, ...]:
        return self._records

    def add(self, record: TensorMemoryRecord) -> TensorMemory:
        if any(item.record_id == record.record_id for item in self._records):
            raise ValueError(f"duplicate memory record: {record.record_id}")
        return TensorMemory(self._records + (record,))

    def search(self, query: tuple[float, ...], limit: int = 5) -> tuple[tuple[TensorMemoryRecord, float], ...]:
        if limit < 1:
            raise ValueError("limit must be positive")
        scored = [(record, cosine_similarity(query, record.embedding)) for record in self._records]
        return tuple(sorted(scored, key=lambda item: (-item[1], item[0].record_id))[:limit])


def cosine_similarity(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have equal dimensions")
    left_norm = sqrt(sum(value * value for value in left))
    right_norm = sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    return dot / (left_norm * right_norm)
