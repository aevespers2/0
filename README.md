# 0

Autonomous vNext Phase-0 scaffolding for a constrained, auditable builder-agent.

## What Is Here

- [AUTONOMOUS_VNEXT.md](AUTONOMOUS_VNEXT.md): architecture, guardrails, risk rubric, and build checklist.
- [mission_contract.schema.json](mission_contract.schema.json): mission intake contract.
- [action_record.schema.json](action_record.schema.json): append-only execution/audit event contract.
- [autonomous_vnext/policy.py](autonomous_vnext/policy.py): deny-by-default policy evaluator.
- [autonomous_vnext/audit.py](autonomous_vnext/audit.py): append-only JSONL audit writer.
- [autonomous_vnext/planner.py](autonomous_vnext/planner.py): minimal candidate planning and risk scoring.
- [autonomous_vnext/executor.py](autonomous_vnext/executor.py): policy-gated execution checks and evidence reports.
- [autonomous_vnext/itensor_adapter.py](autonomous_vnext/itensor_adapter.py): optional ITensor-backed plan scoring adapter.
- [autonomous_vnext/cognitive_hilbert.py](autonomous_vnext/cognitive_hilbert.py): tensor-product Hilbert backbone model.
- [autonomous_vnext/cognitive_state.py](autonomous_vnext/cognitive_state.py): subsystem state representation over the Hilbert backbone.
- [autonomous_vnext/attention_operator.py](autonomous_vnext/attention_operator.py): subsystem attention operators.
- [autonomous_vnext/belief_evolution.py](autonomous_vnext/belief_evolution.py): observation-driven cognitive update operators.
- [autonomous_vnext/sheaf_consistency.py](autonomous_vnext/sheaf_consistency.py): local belief patch consistency checks.
- [autonomous_vnext/tensor_memory.py](autonomous_vnext/tensor_memory.py): vector/tensor memory search primitives.
- [autonomous_vnext/multiagent_tensor_mesh.py](autonomous_vnext/multiagent_tensor_mesh.py): coupled multi-agent state mesh.
- [autonomous_vnext/mission_projection.py](autonomous_vnext/mission_projection.py): objective projection into goal subspace.
- [autonomous_vnext/goal_hamiltonian.py](autonomous_vnext/goal_hamiltonian.py): goal energy scoring.
- [autonomous_vnext/uncertainty_operator.py](autonomous_vnext/uncertainty_operator.py): entropy/confidence reporting.

## Test

```bash
pytest -q
```

The ITensor integration is dependency-gated. Tests mock availability, so the core suite does not require ITensor bindings to be installed.
