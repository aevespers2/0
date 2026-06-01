# Autonomous vNext

## Purpose

Autonomous vNext is a constrained, auditable builder-agent architecture. It is designed to turn a clear objective into reversible engineering action while preserving human control, traceability, and stop conditions.

The agent is not a hidden-goal system. It accepts a mission contract, plans bounded work, evaluates policy, executes checks, records evidence, and stops when risk or ambiguity exceeds the approved envelope.

## Principles

- Truth before confidence.
- Small reversible patches.
- Deny by default.
- Audit every consequential action.
- Re-plan after feedback.
- Prefer evidence over narrative.
- Preserve rollback paths.

## Layered System

1. Mission Kernel: validates the objective, constraints, success criteria, and approval profile.
2. Perception Layer: reads repo state, tests, logs, issue context, and known uncertainty.
3. Planning Engine: creates candidate plans and scores risk before execution.
4. Policy Gate: denies unsafe or out-of-scope actions unless explicitly approved.
5. Execution Layer: runs bounded checks and emits structured results.
6. Evidence Layer: appends action records and builds reviewable reports.
7. Cognitive Hilbert Backbone: represents cognitive state spaces as composable tensor-product subsystems for future ITensor-backed scoring and inference.

## Mission Contract Example

```json
{
  "mission_id": "mission-001",
  "objective": "Implement a small feature safely.",
  "repo_path": "/workspace/project",
  "success_criteria": ["tests pass", "diff is scoped"],
  "constraints": ["no destructive git commands"],
  "approval_policy": "ask-before-risky",
  "created_at": "2026-06-01T00:00:00Z"
}
```

## Action Record Example

```json
{
  "action_id": "act-001",
  "mission_id": "mission-001",
  "step_id": "step-001",
  "actor": "autonomous_vnext",
  "action_type": "check",
  "command": "pytest -q",
  "status": "pass",
  "summary": "test suite passed",
  "created_at": "2026-06-01T00:00:00Z"
}
```

## Policy And Approval Gates

Default policy is deny-by-default. Allowed commands must match an explicit prefix. Optional path guards require command arguments to stay under allowed path prefixes.

High-risk actions require explicit approval:

- Publishing, pushing, deploying, or deleting.
- Secret access or credential changes.
- Destructive git operations.
- Broad filesystem rewrites.
- Network actions not required by the mission.

## Mandatory Stop Conditions

The agent must stop when:

- Mission objective is ambiguous.
- The requested action conflicts with policy.
- Required credentials or remotes are missing.
- Tests expose unrelated failures that cannot be isolated.
- Runtime state diverges from the plan.
- The rollback path is unclear.

## Risk Scoring Rubric

Risk score is a non-negative integer. Lower is safer.

- +1 for read-only commands.
- +2 for local generated artifacts.
- +3 for source edits.
- +5 for package/dependency changes.
- +8 for remote write actions.
- +13 for destructive or irreversible actions.

Candidate plans are sorted by score and the lowest-risk viable plan is selected.

## Cognitive Hilbert Backbone

The cognitive backbone models reasoning state as a tensor product of named subsystems:

```text
H_total = H_intent x H_context x H_plan x H_policy x H_evidence
```

This does not claim quantum hardware access. It provides a disciplined representation for high-dimensional cognitive state and a stable interface for future tensor-network scoring through ITensor.

ITensor is treated as an optional acceleration and modeling backend. If bindings are unavailable, the system fails closed for ITensor-specific execution paths while keeping normal deterministic planning available.

## Cognitive Operating Layer

The next layer turns the Hilbert scaffold into executable cognitive primitives:

```text
Psi_cognition =
H_identity
x H_goals
x H_memory
x H_beliefs
x H_risks
x H_environment
```

Implemented primitives:

- Cognitive state: normalized subsystem amplitudes over a declared Hilbert backbone.
- Attention operator: subsystem-local weighting and optional renormalization.
- Belief evolution: observation-driven updates analogous to `Psi(t+1) = U Psi(t)`, without claiming physical unitary dynamics.
- Sheaf consistency: local belief patches and conflict detection.
- Tensor memory: cosine-ranked memory records with stable payloads.
- Multi-agent tensor mesh: coupled agent nodes with sheaf consistency checks.
- Mission projection: objective terms projected into a goal subspace.
- Goal Hamiltonian: expected energy over a goal subsystem.
- Uncertainty operator: entropy and confidence over a subsystem.
- Cognitive runtime: deterministic end-to-end projection, update, retrieval, consistency, and report generation.
- Experience memory: append-only JSONL records projected back into tensor memory.
- Self-model: explicit capabilities, limitations, confidence, active goals, and beliefs.
- Reflection: expected-vs-observed comparison that updates self-model confidence and beliefs.

These are intentionally compact, deterministic primitives. They establish interfaces and invariants before introducing heavier tensor-network backends.

## Phase-0 Build Checklist

- [x] Mission contract schema.
- [x] Action record schema.
- [x] Policy evaluator.
- [x] Append-only audit writer.
- [x] Minimal planning utilities.
- [x] ITensor adapter gate.
- [x] Cognitive Hilbert backbone scaffold.
- [x] Cognitive state tensor primitives.
- [x] Attention operators.
- [x] Belief evolution operators.
- [x] Sheaf consistency checks.
- [x] Tensor memory search.
- [x] Multi-agent tensor mesh.
- [x] Mission projection.
- [x] Goal Hamiltonian.
- [x] Uncertainty operator.
- [x] Deterministic cognitive runtime cycle.
- [x] Persistent experience memory.
- [x] Self-model.
- [x] Recursive reflection primitive.
- [x] Executor hooks.
- [x] Evidence report generation.
- [x] Unit tests for runtime primitives.

## Implemented Artifacts

- `mission_contract.schema.json`
- `action_record.schema.json`
- `autonomous_vnext/policy.py`
- `autonomous_vnext/audit.py`
- `autonomous_vnext/planner.py`
- `autonomous_vnext/executor.py`
- `autonomous_vnext/itensor_adapter.py`
- `autonomous_vnext/cognitive_hilbert.py`
- `autonomous_vnext/cognitive_state.py`
- `autonomous_vnext/attention_operator.py`
- `autonomous_vnext/belief_evolution.py`
- `autonomous_vnext/sheaf_consistency.py`
- `autonomous_vnext/tensor_memory.py`
- `autonomous_vnext/multiagent_tensor_mesh.py`
- `autonomous_vnext/mission_projection.py`
- `autonomous_vnext/goal_hamiltonian.py`
- `autonomous_vnext/uncertainty_operator.py`
- `autonomous_vnext/cognitive_runtime.py`
- `autonomous_vnext/experience_memory.py`
- `autonomous_vnext/self_model.py`
- `autonomous_vnext/reflection.py`
- `tests/`

## Non-Goals

- No autonomous credential discovery.
- No silent remote writes.
- No self-modification outside explicit mission scope.
- No claim that tensor-network modeling is equivalent to physical quantum computation.
