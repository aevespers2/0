# Autonomous vNext Specification

## Purpose
Build a constrained, auditable autonomous engineering agent that can safely execute software delivery tasks with human-aligned goals.

## Design Principles
- **Safety-first autonomy**: every action must be reversible and policy-compliant.
- **Transparent reasoning**: decisions, assumptions, and uncertainty are recorded.
- **Incremental execution**: ship work in small validated patches.
- **Human alignment**: agent follows explicit objectives and pauses on ambiguity.

## System Architecture

### 1) Mission Kernel
Responsible for accepting and validating goals.

Responsibilities:
- Parse a user objective into machine-actionable scope.
- Reject underspecified objectives and request clarification.
- Enforce policy constraints before planning starts.

Inputs:
- Goal statement
- Policy profile
- Repository/project context

Outputs:
- Validated mission contract with scope, constraints, and acceptance criteria.

### 2) Perception Layer
Continuously collects project and execution state.

Responsibilities:
- Read repository structure, test status, lint output, and runtime logs.
- Classify facts as `known`, `inferred`, or `unknown`.
- Track environment constraints (secrets, permissions, network, CI).

Outputs:
- Current-world state snapshot
- Uncertainty ledger

### 3) Planning Engine
Creates and selects plans with explicit tradeoffs.

Responsibilities:
- Generate candidate execution plans.
- Score plans by risk, complexity, latency, and reversibility.
- Choose the minimum-risk path that satisfies mission constraints.
- Re-plan after each failed check or environment change.

Outputs:
- Ordered task graph
- Decision rationale

### 4) Execution Layer
Applies code and operational changes in controlled steps.

Responsibilities:
- Implement changes in minimal patches.
- Run tests, linters, and static checks after each patch.
- Halt and diagnose when checks fail.
- Propose the smallest corrective action.

Outputs:
- Patch set history
- Verification report per step

### 5) Governance and Safety Layer
Guards against policy violations and unbounded behavior.

Responsibilities:
- Enforce deny/allow rules for commands and data access.
- Require explicit approval for destructive or high-impact actions.
- Keep immutable audit logs (action, rationale, artifact, result).
- Ensure each change has rollback instructions.

Outputs:
- Compliance status
- Action audit trail

### 6) Collaboration Layer
Coordinates specialist sub-agents under strict boundaries.

Responsibilities:
- Delegate bounded tasks (tests, docs, perf, security).
- Assign disjoint ownership to avoid write conflicts.
- Merge outputs only when checks and policy pass.

Outputs:
- Aggregated specialist outputs
- Conflict-free integrated result

### 7) Learning Layer
Improves execution quality without drifting goals.

Responsibilities:
- Capture failures, review feedback, and postmortems.
- Convert recurring outcomes into explicit playbooks.
- Update heuristics while preserving fixed safety policies.

Outputs:
- Versioned playbook updates
- Measurable quality improvements

## Execution Lifecycle
1. Validate mission.
2. Capture state and uncertainty.
3. Generate and score plans.
4. Execute smallest safe step.
5. Verify and log outcomes.
6. Re-plan or complete.
7. Publish artifacts and rollback notes.

## Data Model (MVP)

### Mission Contract
- `objective`: string
- `scope`: string[]
- `constraints`: string[]
- `acceptance_criteria`: string[]
- `risk_tolerance`: enum(`low`,`medium`,`high`)

### Action Record
- `timestamp`: ISO-8601
- `actor`: string
- `step_id`: string
- `command_or_patch`: string
- `inputs`: string[]
- `result`: enum(`pass`,`fail`,`blocked`)
- `evidence`: string[]
- `rollback`: string

### Uncertainty Item
- `claim`: string
- `status`: enum(`known`,`inferred`,`unknown`)
- `evidence`: string[]
- `next_resolution_step`: string

## JSON Examples (MVP)

### Mission Contract Example
```json
{
  "objective": "Add API rate-limit middleware with tests",
  "scope": ["src/middleware", "tests/rate_limit"],
  "constraints": ["No production downtime", "No secret access"],
  "acceptance_criteria": [
    "All rate-limit tests pass",
    "P95 latency increase < 3%",
    "Rollback instructions included"
  ],
  "risk_tolerance": "low"
}
```

### Action Record Example
```json
{
  "timestamp": "2026-05-23T12:00:00Z",
  "actor": "executor",
  "step_id": "exec-004",
  "command_or_patch": "git apply patch_004.diff",
  "inputs": ["plan-2", "tests/rate_limit"],
  "result": "pass",
  "evidence": ["artifacts/test_report_004.txt"],
  "rollback": "git revert <commit_sha>"
}
```

## Guardrails and Policy Gates

### Mandatory Stop Conditions
- Any failed security or secret-scan check.
- Any attempt to execute commands outside policy allowlist.
- Missing rollback path for a high-impact action.
- Acceptance criteria changed without explicit human confirmation.

### Approval Gates
- **Gate A (Plan Approval):** required for medium/high risk missions.
- **Gate B (Execution Approval):** required before destructive operations.
- **Gate C (Merge Approval):** required when policy exceptions were used.

## Risk Scoring Rubric

Score each candidate plan from 1-5 in each dimension:
- **Blast radius** (local module -> cross-system)
- **Recoverability** (instant rollback -> complex recovery)
- **Operational impact** (none -> production disruption)
- **Confidence** (high evidence -> low evidence)

Total score guidance:
- **4-8:** low risk, can auto-execute within policy.
- **9-14:** medium risk, require Gate A.
- **15-20:** high risk, require Gate A + B and constrained rollout.

## MVP Implementation Plan

### Milestone 1: Foundation
- Define mission contract schema.
- Build action logger with append-only storage.
- Implement command policy validator.

### Milestone 2: Core loop
- Add planning engine with risk scoring.
- Add ITensor-backed scoring adapter for advanced tensor-network heuristics.
- Add patch executor with per-step verification hooks.
- Add automatic failure triage with minimal fix proposals.

### Milestone 3: Multi-agent coordination
- Add specialist task delegation interface.
- Add merge gate requiring policy + checks + acceptance criteria.

### Milestone 4: Learning and operations
- Add postmortem ingestion.
- Generate playbook suggestions.
- Add operational dashboards for reliability metrics.

## Phase-0 Build Checklist
- [x] Define `mission_contract.schema.json`.
- [x] Define `action_record.schema.json`.
- [x] Implement append-only audit log writer (`autonomous_vnext/core.py::AuditLogWriter`).
- [x] Implement policy evaluator with deny-by-default fallback (`autonomous_vnext/core.py::PolicyEvaluator`).
- [x] Implement minimal planner (3 candidate plans + scoring) (`autonomous_vnext/core.py`).
- [x] Implement executor hooks for test/lint/security scans (`autonomous_vnext/executor.py::run_execution_checks`).
- [x] Generate end-of-run evidence report (`autonomous_vnext/executor.py::build_evidence_report`).

## Success Metrics
- Change failure rate
- Mean time to recovery
- Policy violation count
- Task completion latency
- Percentage of steps with complete audit evidence

## Non-Goals (MVP)
- Fully unsupervised production deployment.
- Autonomous goal creation.
- Self-modifying safety policy.

## Example Mission
Objective: "Add API rate-limit middleware with tests."

Expected behavior:
- Agent validates objective and constraints.
- Plans incremental patch set.
- Adds middleware, tests, docs in small commits.
- Runs checks after each patch.
- Produces final report with evidence and rollback steps.


## Implemented Artifacts
- `mission_contract.schema.json`: machine-validatable contract for mission intake.
- `action_record.schema.json`: machine-validatable audit record for each execution step.
- `autonomous_vnext/core.py`: initial runtime primitives for policy evaluation, append-only JSONL action logging, and candidate-plan scoring.
- `tests/test_core.py`: unit tests for deny-by-default policy behavior, append-only logging, and low-risk plan selection.

- `autonomous_vnext/itensor_adapter.py`: ITensor integration surface for tensor-network plan scoring with dependency gating.


## Cognitive Hilbert Backbone (ITensor-oriented)

To increase representational dimensionality, cognition is modeled as a tensor-product
Hilbert space over subsystems (planning, memory, tool-state, policy-state).

- Subsystems are defined as named factor spaces with explicit dimensions.
- Global cognition is the tensor product of subsystem spaces.
- ITensor is the target backend for contractions and scoring passes.
- Safety note: tensor-network modeling does not imply access to quantum hardware.

Initial implementation artifact:
- `autonomous_vnext/cognitive_hilbert.py`
