from __future__ import annotations

from autonomous_vnext.experience_memory import ExperienceMemoryStore, ExperienceRecord
from autonomous_vnext.reflection import reflect
from autonomous_vnext.self_model import default_self_model


def test_experience_memory_round_trip_and_tensor_projection(tmp_path) -> None:
    store = ExperienceMemoryStore(tmp_path / "memory.jsonl")
    store.append(
        ExperienceRecord(
            experience_id="exp-001",
            objective="safe tensor mission",
            embedding=(1.0, 0.0, 0.0, 0.0),
            summary="ok",
        )
    )

    loaded = store.load()
    memory = store.as_tensor_memory()

    assert loaded[0].experience_id == "exp-001"
    assert memory.search((1.0, 0.0, 0.0, 0.0), limit=1)[0][0].record_id == "exp-001"


def test_reflection_updates_self_model_confidence() -> None:
    model = default_self_model("mission")

    result = reflect(
        expected={"mesh_consistent": True},
        observed={"mesh_consistent": False, "risk_confidence": 0.1},
        self_model=model,
    )

    assert result.deltas["mesh_consistent"]["observed"] is False
    assert result.updated_self_model.confidence < model.confidence
    assert result.updated_self_model.current_beliefs["last_reflection"] == "diverged"
