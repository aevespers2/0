from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from autonomous_vnext.tensor_memory import TensorMemory, TensorMemoryRecord


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class ExperienceRecord:
    experience_id: str
    objective: str
    embedding: tuple[float, ...]
    summary: str
    created_at: str = field(default_factory=utc_now)
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return json.loads(json.dumps(asdict(self), sort_keys=True))

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ExperienceRecord:
        return cls(
            experience_id=str(payload["experience_id"]),
            objective=str(payload["objective"]),
            embedding=tuple(float(value) for value in payload["embedding"]),
            summary=str(payload["summary"]),
            created_at=str(payload["created_at"]),
            metrics=dict(payload.get("metrics", {})),
        )


class ExperienceMemoryStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def append(self, record: ExperienceRecord) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")

    def load(self) -> tuple[ExperienceRecord, ...]:
        if not self.path.exists():
            return ()
        records = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(ExperienceRecord.from_dict(json.loads(line)))
        return tuple(records)

    def as_tensor_memory(self) -> TensorMemory:
        memory = TensorMemory()
        for record in self.load():
            memory = memory.add(
                TensorMemoryRecord(
                    record_id=record.experience_id,
                    embedding=record.embedding,
                    payload={"objective": record.objective, "summary": record.summary, "source": "experience"},
                )
            )
        return memory
