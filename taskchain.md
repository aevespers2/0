# Task Chain

## Product directive

- **Next objective:** Establish a reproducible health baseline for Autonomous vNext, then verify one end-to-end local mission that is policy-gated, reversible, and fully evidenced.
- **User outcome:** An operator can submit an explicit mission contract and receive a bounded plan, policy decision, execution result, audit record, and rollback path without hidden authority or silent remote action.
- **MVP scope:** existing mission/action schemas; deny-by-default policy; low-risk plan selection; local executor checks; append-only audit/evidence; deterministic cognitive runtime; federation proposal validation; one read-only or local-check mission from intake through report.
- **Priority:** Repository health and the core autonomous-builder contract remain ahead of new scientific domain engines, portfolio roadmaps, or cross-repository publication infrastructure.
- **Success criteria:** clean setup is documented; the complete suite and smoke paths pass at one immutable commit; policy denial and stop conditions are tested; federation rejects stale or invalid proposals; evidence includes commands, versions, hashes, and rollback instructions.
- **Non-goals:** credential discovery, silent pushes or deployment, destructive operations, unrestricted networking, production scientific claims, or implementation of the ClimateSheafFM/composable-discovery proposals or a private publication authority before the core baseline is accepted.
- **Release rationale:** The first release should prove trustworthy bounded execution rather than maximize feature breadth. A verified control loop is the reusable foundation for every later domain-specific agent or cross-repository adapter.

## MVP Roadmap

| Priority | Task | Depends on | Status |
|---|---|---|---|
| P0 | Repository health baseline for the implemented Autonomous vNext surface | — | IN PROGRESS |
| P1 | Verify one end-to-end bounded mission and evidence bundle | P0 | PROPOSED |
| P2 | Establish architecture/package/contract compatibility and ADR baseline | P1 | PROPOSED |
| P3 | Harden configuration, secrets, command/path policy, federation, and rollback | P2 | PROPOSED |
| P4 | Package and document the verified Phase-0 runtime | P3 | PROPOSED |
| P5 | Evaluate domain-specific roadmaps and remote publication adapters as separate product proposals | P4 | BLOCKED |

## P0 health-baseline candidate — PR #7

**Status:** `REVIEW — CONTENT CORRECTED, EXACT-HEAD EVIDENCE AND THREAD DISPOSITION REQUIRED`

PR #7 remains the single bounded Phase 1 inventory path. Autonomous vNext CI run `29565948627` passed only on superseded head `37f19f8c9560f2194bbdbf599e644d122324b994`; it does not verify the current correction lineage.

The inventory now records the Python/pip surface, both Node/TypeScript/npm packages and Node `>=20`, and the executable `.githooks/pre-push` Bash gate with its `scripts/setup_federation_git_hooks.py` activation path. The hook is documented as operator-activated local configuration rather than automatically active for every clone. The punch-list item has been restored to pending, so the next directory-inventory task remains blocked until exact-head verification and review closure.

The remaining correction began at `e4cef7e6c0c286b1259b1469c58205a60de60fe8`; `punchlist.md` was corrected at `b86b7e9f01dac2d25ffcd810d5ce0e139b46e7a9`. These are documentation-only changes and do not modify runtime, workflow, package, schema, credential, network, or deployment behavior.

**Directive:** obtain a successful workflow run attached to the final submitted head, resolve the original Node/TypeScript thread after exact-head evidence is present, resolve the premature-completion and missing-Bash threads against the corrected content, and only then mark Phase 1 item 1 complete and continue to the top-level directory and responsibility inventory. Do not start P1 or treat any earlier workflow as release readiness. The product objective and portfolio priority are unchanged.

## Cross-repository scope gate — draft PR #6

**Status:** `REVIEW — NOT PART OF THE ACTIVE MVP`

Draft PR #6 introduces a proposed Repository `0` myelination/proposal boundary, VTX envelope and serialization primitives, private-authority publication design, and a Muse credential-gateway policy. Its current head is `09038ac55c7945b2abb013d59cf9a1b270a9e717`. Autonomous vNext CI run `29546692277` failed during the test step, so the cognitive-runtime smoke and all federation validation steps were skipped. A successful run on an earlier head does not verify the current submitted state.

Even a passing branch workflow would verify only the configured tests and smoke steps. It would not establish cryptographic signatures, replay protection, receipt chaining, durable canonical storage, key custody, Repository `1` compatibility, secure transport, revocation, or deployable GitHub integration.

A contract mismatch must be resolved before merge: PR #6 documents the expected route as `0:working -> 0:proposal -> 1:quarantine`, while Repository `1` draft PR #1 currently models a direct `0:working -> 1:quarantine` transition and does not define a `proposal` partition edge. The Architect must select one canonical state machine or explicitly distinguish Repository `0`'s local staging state from the cross-repository transition contract.

**Directive:** preserve PR #6 as a draft proposal without changing P0-P4 priority. Do not merge runtime/schema changes until the current head passes exact-head CI, Repository `1`'s product authority is approved, package and schema ownership are assigned, route semantics are reconciled, negative compatibility fixtures exist, and the proposal is decomposed under the appropriate later architecture/security task. Documentation may be split into an ADR-only change if it clearly remains proposed and makes no security or implementation claim.

## Portfolio proposal rule

Open pull requests proposing ClimateSheafFM, a broader composable scientific-discovery stack, or remote/private publication infrastructure remain preserved as research or architecture proposals. They do not become active implementation priorities until P0-P4 produce a verified platform baseline and the Architect documents the repository, package, authority, and rollback boundary.

## Builder Rules

Builders execute only the highest-priority unblocked task. Each task must name files, tests, constraints, stop conditions, evidence, and rollback guidance. Scope must not be widened to absorb a roadmap proposal, cross-repository authority design, or unrelated test failure.

## Builder Log

Record commits, exact commands/results, workflow links, artifact hashes, policy decisions, stop conditions, residual risks, and follow-up work.

- 2026-07-16 — Synchronized draft PR #6 evidence to current head `09038ac55c7945b2abb013d59cf9a1b270a9e717`; CI run `29546692277` failed during tests and skipped all later smoke/federation checks. The draft remains outside the active MVP and portfolio priority is unchanged.
- 2026-07-17 — Reviewed PR #7 at submitted head `37f19f8c9560f2194bbdbf599e644d122324b994`. Exact-head CI run `29565948627` passed, but the Phase 1 language/package/runtime inventory omitted the repository's Node/TypeScript/npm packages and Node `>=20` declaration. P0 advanced to `IN PROGRESS`; the same PR was required to be corrected and reverified.
- 2026-07-17 — Re-reviewed PR #7 at head `71ba0563bbbedfa1554c3f0edce70962fc199dc8`. The Node/TypeScript correction was present, but the active Bash pre-push hook remained omitted and the punch list prematurely marked the inventory item complete. No successful exact-head status was attached and three review threads remained unresolved.
- 2026-07-17 — Implemented the bounded remaining inventory correction on the same PR. `docs/repository-health-baseline.md` now records `.githooks/pre-push`, `/usr/bin/env bash`, strict shell behavior, the two delegated Python checks, `scripts/setup_federation_git_hooks.py`, local `core.hooksPath` activation, exact source blobs, and untested portability limitations. `punchlist.md` is pending again. Exact-head workflow evidence and thread disposition remain required before the directory inventory begins.