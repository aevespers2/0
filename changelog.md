# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product
- 2026-07-16 — Defined the first product outcome as one reproducible, policy-gated, reversible local mission from contract intake through evidence report.
- 2026-07-16 — Kept scientific-discovery roadmap pull requests as proposals rather than active priorities until the Autonomous vNext health, safety, federation, and packaging baseline is accepted.
- 2026-07-16 — Classified draft PR #6, which proposes Repository `0` as a myelination/proposal layer and adds VTX envelope artifacts, as review-only work outside the active P0-P4 MVP; no portfolio reprioritization was made.
- 2026-07-16 — Retained that scope decision after the draft advanced: the current head fails CI, so no VTX/private-authority implementation is eligible to merge into the bounded-mission baseline.

### Architecture
- Replaced the generic greenfield roadmap with a sequence aligned to the substantial existing Phase-0 implementation.
- 2026-07-16 — Recorded a cross-repository contract conflict: PR #6 documents `0:working -> 0:proposal -> 1:quarantine`, while Repository `1` draft PR #1 currently treats `0:working -> 1:quarantine` as the normal tested path and has no `proposal` partition edge.
- 2026-07-16 — Required the Architect to choose a canonical route model, assign schema/package ownership, and approve Repository `1` authority before VTX runtime/schema work can merge.

### Implementation
- No released implementation capability is claimed; existing source and tests remain candidate inputs pending current verification.
- 2026-07-16 — Observed draft PR #6 adding proposed architecture documents, VTX envelope/schema primitives, a Muse credential-gateway policy, safeguards, and tests. These remain unmerged candidate artifacts.

### Evidence
- 2026-07-16 — Earlier draft head `dbd8186caa2017f4dcc2f53e2ae25ce5ec244be8` completed Autonomous vNext CI run `29544823133` successfully, but that result is superseded for submission review because the branch advanced.
- 2026-07-16 — Current draft head `09038ac55c7945b2abb013d59cf9a1b270a9e717` failed Autonomous vNext CI run `29546692277` during tests; the cognitive-runtime smoke and all federation validation steps were skipped.
- 2026-07-16 — Neither the earlier successful run nor the current failing run establishes signature verification, replay protection, receipt chaining, durable canonical storage, key custody, Repository `1` interoperability, secure transport, revocation, or deployable GitHub authority.

### Release
- The `0.0.1-baseline` candidate remains blocked until clean-environment tests, security checks, documentation verification, provenance, and rollback evidence pass.
- 2026-07-16 — Draft PR #6 is excluded from the current release scope unless later accepted through the architecture/security chain with reconciled cross-repository fixtures, exact-head passing evidence, and explicit authority approval.

### Deployment
- No remote publishing or deployment is authorized by the MVP directive.
- 2026-07-16 — Private-authority publication, GitHub adapters, webhooks, keys, and remote writes remain proposals only.

## Entry Format
- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable
