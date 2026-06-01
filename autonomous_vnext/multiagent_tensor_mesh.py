from __future__ import annotations

from dataclasses import dataclass

from autonomous_vnext.cognitive_state import CognitiveState
from autonomous_vnext.sheaf_consistency import LocalBeliefPatch, SheafConsistencyReport, check_sheaf_consistency


@dataclass(frozen=True)
class CognitiveAgentNode:
    node_id: str
    role: str
    state: CognitiveState
    belief_patch: LocalBeliefPatch


@dataclass(frozen=True)
class MultiAgentTensorMesh:
    nodes: tuple[CognitiveAgentNode, ...]

    @property
    def rank(self) -> int:
        return sum(node.state.backbone.rank for node in self.nodes)

    def consistency(self) -> SheafConsistencyReport:
        return check_sheaf_consistency(tuple(node.belief_patch for node in self.nodes))


def build_mesh(nodes: list[CognitiveAgentNode]) -> MultiAgentTensorMesh:
    node_ids = [node.node_id for node in nodes]
    if len(set(node_ids)) != len(node_ids):
        raise ValueError("node ids must be unique")
    return MultiAgentTensorMesh(tuple(nodes))
