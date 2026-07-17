# Task Chain

## Product directive

- **Next objective:** Establish a reproducible health baseline for Autonomous vNext, then verify one end-to-end local mission that is policy-gated, reversible, and fully evidenced.
- **User outcome:** An operator can submit an explicit mission contract and receive a bounded plan, policy decision, execution result, audit record, and rollback path without hidden authority or silent remote action.
- **MVP scope:** existing mission/action schemas; deny-by-default policy; low-risk plan selection; local executor checks; append-only audit/evidence; deterministic cognitive runtime; federation proposal validation; one read-only or local-check mission from intake through report.
- **Priority:** Repository health and the core autonomous-builder contract remain ahead of new scientific domain engines, portfolio roadmaps, cross-repository publication infrastructure, or owner-wide governance automation.
- **Success criteria:** clean setup is documented; the complete suite and smoke paths pass at one immutable commit; policy denial and stop conditions are tested; federation rejects stale or invalid proposals; evidence includes commands, versions, hashes, and rollback instructions.
- **Non-goals:** credential discovery, silent pushes or deployment, destructive operations, unrestricted networking, production scientific claims, implementation of the ClimateSheafFM/composable-discovery proposals, private publication authority, or activation of a portfolio-wide scanner and issue writer before the core baseline and separate governance boundary are accepted.
- **Release rationale:** The first release should prove trustworthy bounded execution rather than maximize feature breadth. A verified control loop is the reusable foundation for every later domain-specific agent, cross-repository adapter, or governance service.

## MVP Roadmap

| Priority | Task | Depends on | Status |
|---|---|---|---|
| P0 | Repository health baseline for the implemented Autonomous vNext surface | — | IN PROGRESS |
| P1 | Verify one end-to-end bounded mission and evidence bundle | P0 | PROPOSED |
| P2 | Establish architecture/package/contract compatibility and ADR baseline | P1 | PROPOSED |
| P3 | Harden configuration, secrets, command/path policy, federation, and rollback | P2 | PROPOSED |
| P4 | Package and document the verified Phase-0 runtime | P3 | PROPOSED |
| P5 | Evaluate domain-specific roadmaps, remote publication adapters, and portfolio governance as separate product proposals | P4 and separate approval | BLOCKED |

## P0 health-baseline candidate — PR #7

**Status:** `REVIEW — CONTENT CORRECTED, EXACT-HEAD EVIDENCE AND FINAL THREAD DISPOSITION REQUIRED`

PR #7 remains the single bounded Phase 1 inventory path. Its current submitted head is `991216f8c9f72a3bcb23b745f148697659217322`, and the PR body now identifies that same head. Autonomous vNext CI run `29565948627` passed only on superseded head `37f19f8c9560f2194bbdbf599e644d122324b994`; no workflow run or commit status is attached to the current head, and GitHub reports the PR non-mergeable.

The candidate now records Python/pip, both Node/TypeScript/npm packages and Node `>=20`, and the executable `.githooks/pre-push` Bash gate with its `scripts/setup_federation_git_hooks.py` activation path. It also keeps Phase 1 item 1 pending, preserves every material review-thread blocker in the release gate, requires Bash hook/setup coverage in the accepted health artifact, and expands rollback to every candidate-touched file. These are documentation-only corrections and do not modify runtime, workflow, package, schema, credential, network, or deployment behavior.

One review thread remains unresolved: the original Node/TypeScript inventory thread, intentionally retained until exact-head evidence exists. The rollback-scope thread is resolved, and the current branch content includes every candidate-touched documentation file in rollback scope.

**Directive:** obtain a successful workflow run attached to the final submitted head, resolve the remaining material thread against that immutable content, and only then mark Phase 1 item 1 complete and continue to the top-level directory and responsibility inventory. Do not start P1 or treat any earlier workflow as release readiness. The product objective and portfolio priority are unchanged.

## Cross-repository scope gate — draft PR #6

**Status:** `REVIEW — NOT PART OF THE ACTIVE MVP`

Draft PR #6 introduces a proposed Repository `0` myelination/proposal boundary, VTX envelope and serialization primitives, private-authority publication design, and a Muse credential-gateway policy. Its current head is `09038ac55c7945b2abb013d59cf9a1b270a9e717`. Autonomous vNext CI run `29546692277` failed during the test step, so the cognitive-runtime smoke and all federation validation steps were skipped.

A contract mismatch remains: PR #6 documents `0:working -> 0:proposal -> 1:quarantine`, while Repository `1` draft PR #1 models a direct `0:working -> 1:quarantine` transition and has no `proposal` partition edge.

**Directive:** preserve PR #6 as a draft proposal without changing P0-P4 priority. Do not merge runtime/schema changes until the current head passes exact-head CI, Repository `1` authority is approved, package and schema ownership are assigned, route semantics are reconciled, negative compatibility fixtures exist, and the proposal is decomposed under a later architecture/security task.

## Portfolio health control-plane scope gate — draft PR #8

**Status:** `REVIEW — DRAFT GOVERNANCE PROPOSAL; NOT PART OF THE ACTIVE MVP`

Draft PR #8 proposes a six-hour owner-wide repository scanner, seven governance-agent roles, deterministic report artifacts, and automatic synchronization of a central health issue. Current head `f291db0446d84005a3764795ca880cafeec1ad4c` passed Portfolio Health Candidate CI run `29583289679` and Autonomous vNext CI run `29583289637`, but neither run retained artifacts. The checks establish compilation and registry structure only; the PR is draft and non-mergeable and does not establish complete repository enumeration, finding accuracy, safe issue lifecycle, private/organization coverage, disabled-Issues behavior, partial-failure recovery, least-privilege credentials, revocation, behavioral fixtures, or rollback.

The candidate overlaps the closed QSO-FABRIC bootstrap proposal and QSO-GENOMES draft PR #3 governance control plane. One canonical owner and authority boundary must be selected before any scheduled portfolio automation is adopted.

**Directive:** keep PR #8 draft and inert without changing P0-P4 priority. Do not merge the scheduled workflow, configure a portfolio token, or activate issue-writing automation until the Architect approves the owning repository, explicit opt-in scope, least-privilege credential/revocation model, enumeration and pagination rules, exact-head and superseded-evidence semantics, failure/retry/checkpoint behavior, issue lifecycle, deterministic behavioral fixtures, retained provenance artifacts, and tested disable/revoke/revert rollback. Reconcile or retire the overlapping QSO-FABRIC and QSO-GENOMES proposals as part of that decision.

## Portfolio proposal rule

Scientific-discovery, private publication, and portfolio-governance pull requests remain preserved as research or architecture proposals. They do not become active implementation priorities until P0-P4 produce a verified platform baseline and the Architect documents repository ownership, authority, contracts, evidence, migration, and rollback.

## Builder Rules

Builders execute only the highest-priority unblocked task. Each task must name files, tests, constraints, stop conditions, evidence, and rollback guidance. Scope must not be widened to absorb a roadmap proposal, cross-repository authority design, governance service, or unrelated test failure.

## Builder Log

Record commits, exact commands/results, workflow links, artifact hashes, policy decisions, stop conditions, residual risks, and follow-up work.

- 2026-07-16 — Synchronized draft PR #6 evidence to current head `09038ac55c7945b2abb013d59cf9a1b270a9e717`; CI run `29546692277` failed during tests and skipped all later smoke/federation checks. The draft remains outside the active MVP and portfolio priority is unchanged.
- 2026-07-17 — Reviewed PR #7 at submitted head `37f19f8c9560f2194bbdbf599e644d122324b994`. Exact-head CI run `29565948627` passed, but the Phase 1 language/package/runtime inventory omitted Node/TypeScript/npm and Node `>=20`. P0 advanced to `IN PROGRESS`; the same PR was required to be corrected and reverified.
- 2026-07-17 — Re-reviewed PR #7 at head `71ba0563bbbedfa1554c3f0edce70962fc199dc8`. The Node correction was present, but the active Bash pre-push hook remained omitted and the punch list prematurely marked the item complete. No successful exact-head status was attached.
- 2026-07-17 — PR #7 corrected the Bash hook/activation inventory, restored the punch-list item to pending, preserved every material release-thread blocker, added Bash to artifact requirements, and expanded rollback scope. Current head `991216f8c9f72a3bcb23b745f148697659217322` has no workflow or commit status, is non-mergeable, and retains one unresolved exact-head thread; the PR body and rollback disposition are now reconciled.
- 2026-07-17 — Classified draft PR #8 as a deferred governance/control-plane proposal outside the active MVP. Its current structural CI passed without retained artifacts, while ownership, scope, credentials, issue lifecycle, failure handling, behavioral evidence, and rollback require a separate Architect decision.
- 2026-07-17 — Reconciled live GitHub state: PR #7 has one unresolved review thread rather than two, and draft PR #8 is non-mergeable. No product priority or scope boundary changed.