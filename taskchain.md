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

**Status:** `REVIEW — FINAL INVENTORY CORRECTIONS AND EXACT-HEAD EVIDENCE REQUIRED`

PR #7 remains the single bounded Phase 1 inventory path. Its current submitted head is `71ba0563bbbedfa1554c3f0edce70962fc199dc8`. Autonomous vNext CI run `29565948627` passed only on superseded head `37f19f8c9560f2194bbdbf599e644d122324b994`; no successful workflow run or commit status is attached to the current head, and GitHub reports the PR non-mergeable.

The Node/TypeScript/npm omission was corrected on the same PR, but review identified two additional acceptance defects. First, the source-level language/runtime inventory omits the active executable `.githooks/pre-push` Bash hook and the documented `scripts/setup_federation_git_hooks.py` activation path. Second, the PR marks the first Phase 1 punch-list item complete before exact-head verification and review closure, contradicting the release and task-chain gates. Three review threads remain unresolved: the retained Node/TypeScript thread pending exact-head CI, the premature punch-list-completion finding, and the missing Bash-runtime finding.

**Directive:** revise the same PR rather than opening a competing baseline path; add the Bash hook and activation/configuration path to the inventory; keep the first Phase 1 punch-list item pending until acceptance; rerun verification at the final submitted head; resolve every material review thread; and only then continue to the top-level directory and responsibility inventory. Do not start P1 or treat any earlier workflow as release readiness. The product objective and portfolio priority are unchanged.

## Cross-repository scope gate — draft PR #6

**Status:** `REVIEW — NOT PART OF THE ACTIVE MVP`

Draft PR #6 introduces a proposed Repository `0` myelination/proposal boundary, VTX envelope and serialization primitives, private-authority publication design, and a Muse credential-gateway policy. Its current head is `09038ac55c7945b2abb013d59cf9a1b270a9e717`. Autonomous vNext CI run `29546692277` failed during the test step, so the cognitive-runtime smoke and all federation validation steps were skipped. A successful run on an earlier head does not verify the current submitted state.

Even a passing branch workflow would verify only the configured tests and smoke steps. It would not establish cryptographic signatures, replay protection, receipt chaining, durable canonical storage, key custody, Repository `1` compatibility, secure transport, revocation, or deployable GitHub integration.

A contract mismatch must be resolved before merge: PR #6 documents the expected route as `0:working -> 0:proposal -> 1:quarantine`, while Repository `1` draft PR #1 currently models a direct `0:working -> 1:quarantine` transition and does not define a `proposal` partition edge. The Architect must select one canonical state machine or explicitly distinguish Repository `0`'s local staging state from the cross-repository transition contract.

**Directive:** preserve PR #6 as a draft proposal without changing P0-P4 priority. Do not merge runtime/schema changes until the current head passes exact-head CI, Repository `1`'s product authority is approved, package and schema ownership are assigned, route semantics are reconciled, negative compatibility fixtures exist, and the proposal is decomposed under the appropriate later architecture/security task. Documentation may be split into an ADR-only change if it clearly remains proposed and makes no security or implementation claim.

## Portfolio health control-plane scope gate — draft PR #8

**Status:** `REVIEW — DRAFT GOVERNANCE PROPOSAL; NOT PART OF THE ACTIVE MVP`

At review start, draft PR #8 proposed a six-hour owner-wide repository scanner, seven governance-agent roles, deterministic report artifacts, and automatic synchronization of a central health issue. The candidate head `7eba0a44256c10df1e63c069d145ef92dfd60280` completed Portfolio Health Candidate CI run `29579875273` and Autonomous vNext CI run `29579875248` successfully. Those runs establish only that the submitted scanner compiles and its role registry satisfies the configured structural checks; they do not establish reliable portfolio enumeration, finding accuracy, safe issue lifecycle behavior, or production authorization.

The candidate overlaps the owner-wide bootstrap/control-plane proposal rejected and closed in QSO-FABRIC PR #1 and the separate governance-control-plane proposal in QSO-GENOMES draft PR #3. One canonical owner and authority boundary must be selected before any scheduled portfolio automation is adopted. The current implementation also requires review for repository and API pagination, private/organization repository coverage, disabled-Issues behavior, transient and partial failures, exact-head **success** rather than mere check-run presence, superseded workflow failures, pull-request mergeability semantics, least-privilege credentials, token fallback behavior, deduplicated issue update/closure, artifact retention, and deterministic zero/one/multiple-finding fixtures.

**Directive:** keep PR #8 draft and preserve its evidence without changing P0-P4 priority. Do not merge the scheduled workflow, configure a portfolio-wide token, or activate issue-writing automation until the Architect approves: (1) the owning repository, preferably a dedicated governance/control repository unless Repository `0` ownership is justified; (2) explicit opt-in repository scope; (3) least-privilege credential and revocation design; (4) complete enumeration and pagination rules; (5) exact-head and superseded-evidence semantics; (6) failure, retry, checkpoint, and rollback behavior; (7) issue lifecycle and disabled-feature handling; (8) behavioral fixtures and retained evidence; and (9) reconciliation with QSO-FABRIC and QSO-GENOMES governance proposals. Because this directive changes the submitted head, the earlier successful runs become superseded and final exact-head CI is required before further review.

## Portfolio proposal rule

Open pull requests proposing ClimateSheafFM, a broader composable scientific-discovery stack, or remote/private publication infrastructure remain preserved as research or architecture proposals. They do not become active implementation priorities until P0-P4 produce a verified platform baseline and the Architect documents the repository, package, authority, and rollback boundary.

## Builder Rules

Builders execute only the highest-priority unblocked task. Each task must name files, tests, constraints, stop conditions, evidence, and rollback guidance. Scope must not be widened to absorb a roadmap proposal, cross-repository authority design, or unrelated test failure.

## Builder Log

Record commits, exact commands/results, workflow links, artifact hashes, policy decisions, stop conditions, residual risks, and follow-up work.

- 2026-07-16 — Synchronized draft PR #6 evidence to current head `09038ac55c7945b2abb013d59cf9a1b270a9e717`; CI run `29546692277` failed during tests and skipped all later smoke/federation checks. The draft remains outside the active MVP and portfolio priority is unchanged.
- 2026-07-17 — Reviewed PR #7 at submitted head `37f19f8c9560f2194bbdbf599e644d122324b994`. Exact-head CI run `29565948627` passed, but the Phase 1 language/package/runtime inventory omitted the repository's Node/TypeScript/npm packages and Node `>=20` declaration. P0 advanced to `IN PROGRESS`; the same PR was required to be corrected and reverified.
- 2026-07-17 — Re-reviewed PR #7 at current head `71ba0563bbbedfa1554c3f0edce70962fc199dc8`. The Node/TypeScript correction is present, but the active Bash pre-push hook remains omitted and the punch list prematurely marks the inventory item complete. The current head has no successful status, the PR is non-mergeable, and three review threads remain unresolved. P0 priority is unchanged; the same PR must be corrected and verified before additional inventory begins.
- 2026-07-17 — Classified draft PR #8 as a deferred governance/control-plane proposal rather than part of the active Autonomous vNext MVP. Its initial structural CI passed, but owner-wide scheduling, issue writes, enumeration, exact-head semantics, failure handling, credential scope, and overlap with two existing governance proposals require an Architect ownership and authority decision. No active priority changed.