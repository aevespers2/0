from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from autonomous_vnext.attention_operator import AttentionOperator
from autonomous_vnext.belief_evolution import BeliefEvolutionOperator, BeliefObservation
from autonomous_vnext.cognitive_hilbert import build_cognitive_backbone
from autonomous_vnext.cognitive_state import CognitiveState, basis_state
from autonomous_vnext.goal_hamiltonian import GoalHamiltonian
from autonomous_vnext.mission_projection import MissionProjection
from autonomous_vnext.multiagent_tensor_mesh import CognitiveAgentNode, build_mesh
from autonomous_vnext.sheaf_consistency import LocalBeliefPatch
from autonomous_vnext.tensor_memory import TensorMemory, TensorMemoryRecord
from autonomous_vnext.uncertainty_operator import subsystem_entropy


DEFAULT_BACKBONE = (
    ("identity", 2),
    ("goals", 4),
    ("memory", 4),
    ("beliefs", 4),
    ("risks", 3),
    ("environment", 3),
)


@dataclass(frozen=True)
class CognitiveRuntimeReport:
    objective: str
    backbone: dict[str, object]
    state: dict[str, tuple[float, ...]]
    uncertainty: dict[str, dict[str, float | str]]
    goal_energy: float
    retrieved_memory: tuple[dict[str, object], ...]
    mesh_consistent: bool
    mesh_conflicts: tuple[dict[str, str], ...]


def run_cognitive_cycle(objective: str, observations: dict[str, tuple[float, ...]] | None = None) -> CognitiveRuntimeReport:
    if not objective.strip():
        raise ValueError("objective is required")

    backbone = build_cognitive_backbone(list(DEFAULT_BACKBONE))
    state = basis_state(backbone)
    state = MissionProjection(tuple(objective.split())).project(state)

    observation_payload = observations or {
        "beliefs": (0.1, 0.7, 0.1, 0.1),
        "risks": (0.7, 0.2, 0.1),
        "environment": (0.2, 0.6, 0.2),
    }
    state = _evolve_state(state, observation_payload)

    memory = _default_memory()
    retrieved = tuple(
        {"record_id": record.record_id, "score": score, "payload": record.payload}
        for record, score in memory.search(_query_vector(objective), limit=3)
    )

    mesh = build_mesh(
        [
            CognitiveAgentNode(
                "planner",
                "planning",
                state,
                LocalBeliefPatch("planner", {"objective": objective, "status": "active"}),
            ),
            CognitiveAgentNode(
                "risk",
                "risk",
                state,
                LocalBeliefPatch("risk", {"objective": objective, "status": "active"}),
            ),
        ]
    )
    consistency = mesh.consistency()
    energy = GoalHamiltonian("goals", (1.0, 0.5, 0.75, 1.25)).expected_energy(state)
    uncertainty = {
        label: asdict(subsystem_entropy(state, label))
        for label in ("goals", "beliefs", "risks", "environment")
    }

    return CognitiveRuntimeReport(
        objective=objective,
        backbone={
            "rank": backbone.rank,
            "total_dimension": backbone.total_dimension,
            "labels": backbone.labels,
        },
        state={subsystem.name: subsystem.amplitudes for subsystem in state.subsystems},
        uncertainty=uncertainty,
        goal_energy=energy,
        retrieved_memory=retrieved,
        mesh_consistent=consistency.consistent,
        mesh_conflicts=consistency.conflicts,
    )


def report_to_dict(report: CognitiveRuntimeReport) -> dict[str, object]:
    return json.loads(json.dumps(asdict(report), sort_keys=True))


def write_report(report: CognitiveRuntimeReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report_to_dict(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _evolve_state(state: CognitiveState, observations: dict[str, tuple[float, ...]]) -> CognitiveState:
    operators = [
        BeliefObservation(subsystem, evidence, learning_rate=0.8)
        for subsystem, evidence in sorted(observations.items())
    ]
    attention = (
        AttentionOperator("beliefs", (1.0, 1.2, 1.0, 0.8)),
        AttentionOperator("risks", (1.2, 0.9, 0.7)),
    )
    return BeliefEvolutionOperator(tuple(operators), attention=attention).evolve(state)


def _default_memory() -> TensorMemory:
    return (
        TensorMemory()
        .add(TensorMemoryRecord("mission_projection", (1.0, 0.2, 0.0, 0.0), {"module": "mission_projection"}))
        .add(TensorMemoryRecord("risk_governance", (0.2, 1.0, 0.2, 0.0), {"module": "policy"}))
        .add(TensorMemoryRecord("evidence_reporting", (0.1, 0.3, 1.0, 0.2), {"module": "executor"}))
        .add(TensorMemoryRecord("tensor_backbone", (0.4, 0.0, 0.2, 1.0), {"module": "cognitive_hilbert"}))
    )


def _query_vector(objective: str) -> tuple[float, ...]:
    lowered = objective.lower()
    return (
        1.0 if any(word in lowered for word in ("goal", "mission", "objective")) else 0.2,
        1.0 if any(word in lowered for word in ("risk", "policy", "safe")) else 0.2,
        1.0 if any(word in lowered for word in ("evidence", "test", "report")) else 0.2,
        1.0 if any(word in lowered for word in ("tensor", "hilbert", "cognitive")) else 0.2,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a deterministic Autonomous vNext cognitive cycle.")
    parser.add_argument("objective", help="Mission objective to project into the cognitive state.")
    parser.add_argument("--output", type=Path, default=Path("reports/cognitive_runtime_report.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run_cognitive_cycle(args.objective)
    write_report(report, args.output)
    print(args.output)


if __name__ == "__main__":
    main()
