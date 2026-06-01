from __future__ import annotations

import pytest

from autonomous_vnext.attention_operator import AttentionOperator
from autonomous_vnext.belief_evolution import BeliefEvolutionOperator, BeliefObservation
from autonomous_vnext.cognitive_hilbert import build_cognitive_backbone
from autonomous_vnext.cognitive_state import basis_state
from autonomous_vnext.goal_hamiltonian import GoalHamiltonian
from autonomous_vnext.mission_projection import MissionProjection
from autonomous_vnext.multiagent_tensor_mesh import CognitiveAgentNode, build_mesh
from autonomous_vnext.sheaf_consistency import LocalBeliefPatch, check_sheaf_consistency
from autonomous_vnext.tensor_memory import TensorMemory, TensorMemoryRecord
from autonomous_vnext.uncertainty_operator import subsystem_entropy


def test_attention_operator_updates_subsystem() -> None:
    backbone = build_cognitive_backbone([("goals", 2), ("memory", 2)])
    state = basis_state(backbone, {"goals": 0, "memory": 1})

    updated = AttentionOperator("goals", (0.0, 1.0), renormalize=False).apply(state)

    assert updated.subsystem("goals").amplitudes == (0.0, 0.0)
    assert updated.subsystem("memory").amplitudes == (0.0, 1.0)


def test_belief_evolution_mixes_observation() -> None:
    backbone = build_cognitive_backbone([("beliefs", 2)])
    state = basis_state(backbone, {"beliefs": 0})
    operator = BeliefEvolutionOperator((BeliefObservation("beliefs", (0.0, 1.0), learning_rate=0.5),))

    evolved = operator.evolve(state)

    assert evolved.subsystem("beliefs").amplitudes == pytest.approx((0.70710678, 0.70710678))


def test_sheaf_consistency_detects_conflict() -> None:
    report = check_sheaf_consistency(
        (
            LocalBeliefPatch("planner", {"case": "open"}),
            LocalBeliefPatch("legal", {"case": "closed"}),
        )
    )

    assert not report.consistent
    assert report.conflicts[0]["variable"] == "case"


def test_tensor_memory_search_orders_by_similarity() -> None:
    memory = TensorMemory().add(TensorMemoryRecord("a", (1.0, 0.0), {"text": "alpha"})).add(
        TensorMemoryRecord("b", (0.0, 1.0), {"text": "beta"})
    )

    result = memory.search((0.9, 0.1), limit=1)

    assert result[0][0].record_id == "a"


def test_multiagent_mesh_reports_rank_and_consistency() -> None:
    backbone = build_cognitive_backbone([("goals", 2)])
    state = basis_state(backbone)
    mesh = build_mesh(
        [
            CognitiveAgentNode("planner", "planning", state, LocalBeliefPatch("planner", {"x": "1"})),
            CognitiveAgentNode("risk", "risk", state, LocalBeliefPatch("risk", {"x": "1"})),
        ]
    )

    assert mesh.rank == 2
    assert mesh.consistency().consistent


def test_mission_projection_sets_goal_subspace() -> None:
    backbone = build_cognitive_backbone([("goals", 4)])
    state = basis_state(backbone, {"goals": 3})

    projected = MissionProjection(("ship", "verify")).project(state)

    assert projected.subsystem("goals").amplitudes == pytest.approx((0.70710678, 0.70710678, 0.0, 0.0))


def test_goal_hamiltonian_expected_energy() -> None:
    backbone = build_cognitive_backbone([("goals", 2)])
    state = basis_state(backbone, {"goals": 1})
    hamiltonian = GoalHamiltonian("goals", (10.0, 2.0))

    assert hamiltonian.ground_index() == 1
    assert hamiltonian.expected_energy(state) == 2.0


def test_uncertainty_entropy_confidence() -> None:
    backbone = build_cognitive_backbone([("beliefs", 2)])
    state = basis_state(backbone, {"beliefs": 0})

    report = subsystem_entropy(state, "beliefs")

    assert report.entropy_bits == 0.0
    assert report.confidence == 1.0
