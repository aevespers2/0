# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product
- 2026-07-16 — Defined the first product outcome as one reproducible, policy-gated, reversible local mission from contract intake through evidence report.
- 2026-07-16 — Kept scientific-discovery roadmap pull requests as proposals rather than active priorities until the Autonomous vNext health, safety, federation, and packaging baseline is accepted.
- 2026-07-16 — Classified draft PR #6, which proposes Repository `0` as a myelination/proposal layer and adds VTX envelope artifacts, as review-only work outside the active P0-P4 MVP; no portfolio reprioritization was made.
- 2026-07-16 — Retained that scope decision after the draft advanced: the current head fails CI, so no VTX/private-authority implementation is eligible to merge into the bounded-mission baseline.
- 2026-07-17 — Advanced the existing repository-health objective from `READY` to `IN PROGRESS` after PR #7 submitted a bounded Phase 1 inventory candidate; no product priority changed.
- 2026-07-17 — Retained P0 and the existing product objective after final-head review found additional inventory and acceptance-state defects; the correction stays on PR #7 rather than creating a competing path.

### Architecture
- Replaced the generic greenfield roadmap with a sequence aligned to the substantial existing Phase-0 implementation.
- 2026-07-16 — Recorded a cross-repository contract conflict: PR #6 documents `0:working -> 0:proposal -> 1:quarantine`, while Repository `1` draft PR #1 currently treats `0:working -> 1:quarantine` as the normal tested path and has no `proposal` partition edge.
- 2026-07-16 — Required the Architect to choose a canonical route model, assign schema/package ownership, and approve Repository `1` authority before VTX runtime/schema work can merge.

### Implementation
- No released implementation capability is claimed; existing source and tests remain candidate inputs pending current verification.
- 2026-07-16 — Observed draft PR #6 adding proposed architecture documents, VTX envelope/schema primitives, a Muse credential-gateway policy, safeguards, and tests. These remain unmerged candidate artifacts.
- 2026-07-17 — Observed PR #7 adding a documentation-only repository-health report and P0 progress records. The change remains a candidate and does not modify runtime, schema, workflow, dependency, credential, network, or deployment behavior.
- 2026-07-17 — PR #7 corrected its Node/TypeScript/npm inventory, but the current candidate still omits the active Bash pre-push hook and its documented activation path.

### Evidence
- 2026-07-16 — Earlier draft head `dbd8186caa2017f4dcc2f53e2ae25ce5ec244be8` completed Autonomous vNext CI run `29544823133` successfully, but that result is superseded for submission review because the branch advanced.
- 2026-07-16 — Current draft head `09038ac55c7945b2abb013d59cf9a1b270a9e717` failed Autonomous vNext CI run `29546692277` during tests; the cognitive-runtime smoke and all federation validation steps were skipped.
- 2026-07-16 — Neither the earlier successful run nor the current failing run establishes signature verification, replay protection, receipt chaining, durable canonical storage, key custody, Repository `1` interoperability, secure transport, revocation, or deployable GitHub authority.
- 2026-07-17 — PR #7 submitted head `37f19f8c9560f2194bbdbf599e644d122324b994` completed Autonomous vNext CI run `29565948627` successfully.
- 2026-07-17 — Independent review found the claimed language/package/runtime inventory incomplete because it omitted the repository's Node/TypeScript/npm packages, their manifests and scripts, and the declared Node `>=20` runtime.
- 2026-07-17 — Current PR #7 head `71ba0563bbbedfa1554c3f0edce70962fc199dc8` has no successful workflow run or commit status and is non-mergeable. Three review threads remain unresolved: the retained Node/TypeScript thread pending exact-head CI, a premature punch-list-completion finding, and a missing Bash-hook/runtime finding.

### Release
- The `0.0.1-baseline` candidate remains blocked until clean-environment tests, security checks, documentation verification, provenance, and rollback evidence pass.
- 2026-07-16 — Draft PR #6 is excluded from the current release scope unless later accepted through the architecture/security chain with reconciled cross-repository fixtures, exact-head passing evidence, and explicit authority approval.
- 2026-07-17 — A passing workflow on PR #7's earlier head does not make the repository release-ready. The same PR must inventory the active Bash hook, keep the Phase 1 item pending until acceptance, pass final-head verification, and close material review threads before additional P0 inventory begins.

### Deployment
- No remote publishing or deployment is authorized by the MVP directive.
- 2026-07-16 — Private-authority publication, GitHub adapters, webhooks, keys, and remote writes remain proposals only.
- 2026-07-17 — Deployment review recorded the Bash-inventory and acceptance-state defects; no deployment was attempted or authorized.

## Entry Format
- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable
