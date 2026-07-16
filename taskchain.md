# Task Chain

## Product directive

- **Next objective:** Establish a reproducible health baseline for Autonomous vNext, then verify one end-to-end local mission that is policy-gated, reversible, and fully evidenced.
- **User outcome:** An operator can submit an explicit mission contract and receive a bounded plan, policy decision, execution result, audit record, and rollback path without hidden authority or silent remote action.
- **MVP scope:** existing mission/action schemas; deny-by-default policy; low-risk plan selection; local executor checks; append-only audit/evidence; deterministic cognitive runtime; federation proposal validation; one read-only or local-check mission from intake through report.
- **Priority:** Repository health and the core autonomous-builder contract remain ahead of new scientific domain engines or portfolio roadmaps.
- **Success criteria:** clean setup is documented; the complete suite and smoke paths pass at one immutable commit; policy denial and stop conditions are tested; federation rejects stale or invalid proposals; evidence includes commands, versions, hashes, and rollback instructions.
- **Non-goals:** credential discovery, silent pushes or deployment, destructive operations, unrestricted networking, production scientific claims, or implementation of the ClimateSheafFM/composable-discovery proposals before the core baseline is accepted.
- **Release rationale:** The first release should prove trustworthy bounded execution rather than maximize feature breadth. A verified control loop is the reusable foundation for every later domain-specific agent.

## MVP Roadmap

| Priority | Task | Depends on | Status |
|---|---|---|---|
| P0 | Repository health baseline for the implemented Autonomous vNext surface | — | READY |
| P1 | Verify one end-to-end bounded mission and evidence bundle | P0 | PROPOSED |
| P2 | Establish architecture/package/contract compatibility and ADR baseline | P1 | PROPOSED |
| P3 | Harden configuration, secrets, command/path policy, federation, and rollback | P2 | PROPOSED |
| P4 | Package and document the verified Phase-0 runtime | P3 | PROPOSED |
| P5 | Evaluate domain-specific roadmaps as separate product proposals | P4 | BLOCKED |

## Portfolio proposal rule

Open pull requests proposing ClimateSheafFM or a broader composable scientific-discovery stack remain preserved as research proposals. They do not become active implementation priorities until P0-P4 produce a verified platform baseline and the Architect documents the new repository or package boundary.

## Builder Rules

Builders execute only the highest-priority unblocked task. Each task must name files, tests, constraints, stop conditions, evidence, and rollback guidance. Scope must not be widened to absorb a roadmap proposal or unrelated test failure.

## Builder Log

Record commits, exact commands/results, workflow links, artifact hashes, policy decisions, stop conditions, residual risks, and follow-up work.