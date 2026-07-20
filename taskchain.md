# Task Chain

## Product directive

- **Next objective:** Establish a reproducible health baseline for Autonomous vNext, then verify one end-to-end local mission that is policy-gated, reversible, and fully evidenced.
- **User outcome:** An operator can submit an explicit mission contract and receive a bounded plan, policy decision, execution result, audit record, reflection result, and rollback path without hidden authority or silent remote action.
- **MVP scope:** existing mission/action schemas; deny-by-default policy; low-risk planning; local executor checks; append-only evidence; deterministic cognitive runtime; federation proposal validation; one read-only or local-check mission from intake through report.
- **Priority:** Repository health and the bounded autonomous-builder contract remain ahead of new scientific engines, cross-repository publication, portfolio-wide authority, automatic infrastructure apply, release, or deployment.
- **Success criteria:** clean setup is documented; complete applicable suites and smoke paths pass at one immutable commit; denial and stop conditions are tested; federation rejects stale or invalid proposals; evidence includes commands, versions, hashes, review state, and rollback.
- **Non-goals:** credential discovery, silent pushes, unrestricted networking, destructive operations, production scientific claims, automatic Terraform apply, private publication authority, or owner-wide mutation before the core baseline and governance boundary are accepted.

## MVP roadmap

| Priority | Task | Depends on | Status |
|---|---|---|---|
| P0 | Repository health baseline for the implemented Autonomous vNext surface | — | IN PROGRESS |
| P1 | Verify one end-to-end bounded mission and evidence bundle | P0 | PROPOSED |
| P2 | Establish architecture, package, contract, and ADR compatibility baseline | P1 | PROPOSED |
| P3 | Harden configuration, secrets, command/path policy, federation, incident response, and rollback | P2 | PROPOSED |
| P4 | Package and document the verified Phase-0 runtime | P3 | PROPOSED |
| P5 | Evaluate portfolio governance, VTX/private authority, scientific engines, and infrastructure automation as separate products | P4 and separate approval | BLOCKED |

## P0 repository-health path — draft PR #7

**Status:** `STALE REVIEW PATH — CURRENT HEAD LACKS ATTACHED EXACT-HEAD CI AND IS NON-MERGEABLE`

PR #7 documents the Python, Node/TypeScript/npm, and Bash-hook surfaces at head `991216f8c9f72a3bcb23b745f148697659217322`. The passing Autonomous vNext run applies to an earlier head. Current content corrections remain useful candidate evidence, but P0 must not advance until the submitted head is verified, the remaining material review thread is resolved, and the candidate is reconciled with current `main`, including merged Gods/Clan and comment-policy changes.

**Directive:** preserve PR #7 as historical P0 evidence or rebuild its inventory from current `main`. Do not mark the phase complete from superseded workflow results.

## VTX and Repository 1 boundary — draft PR #6

**Status:** `DEFERRED ARCHITECTURE AND SECURITY PROPOSAL`

PR #6 remains open, draft, and mergeable at head `beb8dd2974aa936d1c0a23989b19c18e28e40e95`. It proposes Repository `0` as a myelination/proposal layer, VTX envelope primitives, and a credential-gateway policy while keeping Repository `1` authoritative.

**Directive:** do not issue a token or merge the proposal into the bounded-mission release until Repository `1` authority, canonical route semantics, package/schema ownership, negative compatibility fixtures, credential custody, revocation, and rollback are approved.

## Portfolio-health control plane — draft PR #10

**Status:** `REVIEWABLE CANDIDATE — GOVERNANCE AND TRUSTED-MAIN ACCEPTANCE REQUIRED`

PR #10 supersedes PR #8 and is open, draft, and mergeable at head `7328cef2a6c9f033b3bee1720da51f567bad5b23`. Its exact-head candidate workflows passed and retained evidence. It improves enumeration, current-head semantics, failure handling, exact-source checkout, artifact retention, and fail-closed reporting.

**Directive:** keep the control plane inert until the Architect approves the canonical owner, opt-in scope, private-repository treatment, least-privilege `PORTFOLIO_TOKEN`, issue lifecycle, finding semantics, trusted-main scan review, disable/revoke procedure, and the rule that scanner output cannot authorize release.

## Merged integration scaffolds — PR #11

**Status:** `MERGED SCAFFOLD — PRE-REVIEW HARDENING REMAINS`

The Gods observability/Jira and Clan Terraform scaffold is now present on `main`. It preserves human approval for Terraform apply and automatic release actions. `punchlists/gods-clan-pre-review.md` remains controlling evidence for workflow pinning, credential configuration, exact-head verification, and operational acceptance.

**Directive:** treat monitoring and planning as distinct from Jira mutation, Terraform apply, release, or deployment. Do not infer authority from merged scaffolding.

## Source comment policy — PR #12

**Status:** `MERGED POLICY`

The repository now rejects double-slash source comments while preserving URL/URI syntax, division operators, and quoted strings. All new source changes must satisfy `scripts/check_comment_style.py` and the associated workflow.

## Documentation foundation candidate

**Status:** `REVIEW — DOCUMENTATION AND VALIDATION ONLY`

The current documentation branch adds a Pages-ready MkDocs site covering the project overview, architecture, A.L.I.S.T.A.I.R.E. portfolio role, contracts, autonomous-development lifecycle, onboarding, security, operations, recovery, and release evidence. It also adds exact-head documentation validation. It does not modify runtime behavior or authorize Pages publication, credentials, merges, releases, deployments, Terraform apply, or owner-wide mutation.

**Directive:** require strict site rendering, link validation, existing repository CI, and review of all claim/authority boundaries before merge. The documentation candidate does not complete P0.

## Portfolio proposal rule

Scientific-discovery, VTX/private-authority, portfolio-governance, Jira, Terraform, and other external-integration candidates remain bounded proposals or scaffolds until the core P0-P4 platform baseline and their own authority, security, evidence, incident, and rollback gates are accepted.

## Builder rules

Builders execute only the highest-priority unblocked task. Each task names files, tests, constraints, stop conditions, evidence, and rollback. Scope must not be widened to absorb an unrelated proposal or failure. A passing workflow validates only the exact tested head and cannot by itself authorize merge, release, deployment, credentials, or infrastructure change.

## Builder log

Record commits, commands, workflow runs, artifact hashes, policy decisions, stop conditions, residual risks, and follow-up work.

- 2026-07-17 — PR #7 corrected repository inventory content but remained non-mergeable without attached exact-head CI for its current head.
- 2026-07-19 — PR #10 replaced the earlier portfolio-health proposal with a current-main, exact-head-validated, evidence-retaining candidate; governance and trusted-main acceptance remain open.
- 2026-07-19 — PR #11 merged Gods/Clan observability and Terraform scaffolds while preserving human approval for apply and releases and retaining a hardening punch list.
- 2026-07-19 — PR #12 merged the source comment-style policy and repository gate.
- 2026-07-20 — Added a documentation-only Pages, architecture, onboarding, security, operations, and release-evidence foundation without changing product priority or runtime scope.
