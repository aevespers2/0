# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product
- 2026-07-16 — Defined the first product outcome as one reproducible, policy-gated, reversible local mission from contract intake through evidence report.
- 2026-07-16 — Kept scientific-discovery roadmap pull requests as proposals rather than active priorities until the Autonomous vNext health, safety, federation, and packaging baseline is accepted.
- 2026-07-16 — Classified draft PR #6, which proposes Repository `0` as a myelination/proposal layer and adds VTX envelope artifacts, as review-only work outside the active P0-P4 MVP; no portfolio reprioritization was made.
- 2026-07-16 — Retained that scope decision after the draft advanced: the current head fails CI, so no VTX/private-authority implementation is eligible to merge into the bounded-mission baseline.
- 2026-07-17 — Advanced the existing repository-health objective from `READY` to `IN PROGRESS` after PR #7 submitted a bounded Phase 1 inventory candidate; no product priority changed.
- 2026-07-17 — Retained P0 and the existing product objective while keeping all repository-health corrections on PR #7 rather than creating a competing baseline path.
- 2026-07-17 — Classified draft PR #8 as a deferred governance/control-plane proposal outside the active P0-P4 MVP. Owner-wide scheduling and issue-writing do not become active priorities merely because structural CI passed.

### Architecture
- Replaced the generic greenfield roadmap with a sequence aligned to the substantial existing Phase-0 implementation.
- 2026-07-16 — Recorded a cross-repository contract conflict: PR #6 documents `0:working -> 0:proposal -> 1:quarantine`, while Repository `1` draft PR #1 treats `0:working -> 1:quarantine` as the normal tested path and has no `proposal` partition edge.
- 2026-07-16 — Required the Architect to choose a canonical route model, assign schema/package ownership, and approve Repository `1` authority before VTX runtime/schema work can merge.
- 2026-07-17 — Recorded that PR #8 overlaps the closed QSO-FABRIC bootstrap proposal and QSO-GENOMES draft governance control plane. One canonical governance owner, opt-in scope, credential boundary, evidence model, and rollback path must be approved before adoption.

### Implementation
- No released implementation capability is claimed; existing source and tests remain candidate inputs pending current verification.
- 2026-07-16 — Observed draft PR #6 adding proposed architecture documents, VTX envelope/schema primitives, a Muse credential-gateway policy, safeguards, and tests. These remain unmerged candidate artifacts.
- 2026-07-17 — Observed PR #7 adding a documentation-only repository-health report and P0 progress records. The change remains a candidate and does not modify runtime, schema, workflow, dependency, credential, network, or deployment behavior.
- 2026-07-17 — PR #7 now inventories Python/pip, both Node/TypeScript/npm packages, Node `>=20`, and the executable Bash pre-push hook plus operator-invoked activation path; it also restores the Phase 1 item to pending and corrects release-artifact and rollback wording.
- 2026-07-17 — Observed PR #8 adding a portfolio scanner, scheduled and candidate workflows, a seven-role registry, and control-plane documentation. These are implemented candidate artifacts, not an accepted or activated portfolio-governance capability.

### Evidence
- 2026-07-16 — Earlier draft head `dbd8186caa2017f4dcc2f53e2ae25ce5ec244be8` completed Autonomous vNext CI run `29544823133` successfully, but that result is superseded for submission review because the branch advanced.
- 2026-07-16 — Current draft PR #6 head `09038ac55c7945b2abb013d59cf9a1b270a9e717` failed Autonomous vNext CI run `29546692277` during tests; the cognitive-runtime smoke and all federation validation steps were skipped.
- 2026-07-16 — Neither the earlier successful run nor the current failing run establishes signature verification, replay protection, receipt chaining, durable canonical storage, key custody, Repository `1` interoperability, secure transport, revocation, or deployable GitHub authority.
- 2026-07-17 — PR #7 submitted head `37f19f8c9560f2194bbdbf599e644d122324b994` completed Autonomous vNext CI run `29565948627` successfully.
- 2026-07-17 — Independent review found the original language/package/runtime inventory incomplete; later review also found the Bash hook and acceptance-state omissions.
- 2026-07-17 — PR #7 current head `991216f8c9f72a3bcb23b745f148697659217322` contains the bounded content corrections and is consistently identified in the PR body, but has no attached workflow run or commit status, is non-mergeable, and retains one unresolved Node/TypeScript review thread pending exact-head verification. The corrected rollback-scope thread is resolved.
- 2026-07-17 — PR #8 current head `f291db0446d84005a3764795ca880cafeec1ad4c` completed Portfolio Health Candidate CI run `29583289679` and Autonomous vNext CI run `29583289637` successfully, but neither run retained artifacts. The checks validate compilation and registry structure rather than enumeration, finding semantics, issue lifecycle, credential scope, failure recovery, or behavioral fixtures; GitHub currently reports the draft non-mergeable.

### Release
- The `0.0.1-baseline` candidate remains blocked until clean-environment tests, security checks, documentation verification, provenance, and rollback evidence pass.
- 2026-07-16 — Draft PR #6 is excluded from the current release scope unless later accepted through the architecture/security chain with reconciled cross-repository fixtures, exact-head passing evidence, and explicit authority approval.
- 2026-07-17 — A passing workflow on PR #7's earlier head does not make the repository release-ready. The final submitted head must pass attached exact-head CI and the remaining material review thread must be resolved before additional P0 inventory begins.
- 2026-07-17 — Draft PR #8 is excluded from the Autonomous vNext release. Its scanner, registry, scheduled workflow, token boundary, and issue lifecycle require a separately approved governance product and retained behavioral evidence.

### Deployment
- No remote publishing or deployment is authorized by the MVP directive.
- 2026-07-16 — Private-authority publication, GitHub adapters, webhooks, keys, and remote writes remain proposals only.
- 2026-07-17 — No deployment was attempted for PR #7; current-head verification and final review closure remain blocking.
- 2026-07-17 — No portfolio-wide token, six-hour schedule, central issue mutation, or automated recovery closure from PR #8 is authorized. The draft remains inert until ownership, least privilege, opt-in scope, tests, failure recovery, retained evidence, and rollback are approved.

## Entry Format
- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable