# Task Chain

## Product directive

- **Next objective:** Establish a reproducible repository-health and portable device-security baseline for Autonomous vNext, then verify one end-to-end local bootstrap mission that is policy-gated, reversible, and fully evidenced.
- **User outcome:** After a laptop, phone, workstation, or other owned environment is acquired, replaced, reset, recovered, or suspected of compromise, the operator can install Repository `0`, inventory the device before trusting ordinary tooling, compare it with an approved baseline, prepare bounded remediation, and submit evidence-backed proposals to Repository `1` without hidden authority or silent remote action.
- **MVP scope:** existing mission/action schemas; deny-by-default policy; low-risk planning; local executor checks; append-only evidence; deterministic cognitive runtime; federation proposal validation; one read-only portable-bootstrap mission covering platform identity, package-manager state, startup persistence, accounts, certificates, network interfaces, DNS/proxy/VPN/routes, firewall, hotspot/tethering, sharing, and Bluetooth where the platform permits observation; and the documentation-only [Portable Security Contract v0](docs/portable-security-contract-v0.md) defining the shared Repository `0`/`1` route, identifiers, result semantics, capability, receipt, revocation, privacy, and fixture requirements.
- **Priority:** Repository health and the portable first-install contract remain ahead of new scientific engines, cross-repository publication, portfolio-wide authority, automatic infrastructure apply, release, or deployment.
- **Success criteria:** clean setup is documented; supported platforms and unsupported controls are explicit; complete applicable suites and smoke paths pass at one immutable commit; denial and stop conditions are tested; device observations are provenance-bound; Repository `1` rejects stale or invalid proposals; evidence includes commands, versions, hashes, review state, and rollback; and both repositories pass one identical versioned contract fixture corpus.
- **Non-goals:** credential discovery, silent pushes, unrestricted networking, destructive operations, intrusive surveillance, traffic interception, counter-intrusion, control of unauthorized devices, production scientific claims, automatic Terraform apply, private publication authority, or owner-wide mutation before the core baseline and governance boundary are accepted.

## Portable first-install security foundation

Repository `0` is the candidate bootstrap, inspection, remediation-planning, bounded-execution, and continuous-maintenance layer installed before higher-level A.L.I.S.T.A.I.R.E. components are trusted. Repository `1` is the proposed independent trust core that owns accepted baselines, capability decisions, revocation, canonical receipts, and recovery checkpoints.

The canonical documentation target is:

`new/recovered/suspect device → Repository 0 read-only inventory → non-authoritative local proposal → versioned proposal envelope → Repository 1 quarantine/decision → bounded capability → Repository 0 reversible remediation → resulting-state receipt → Repository 1 reconciliation`

A passing local check is not proof that a device is fully secure. Unsupported or unobservable platform state is recorded as `UNKNOWN`, and consequential remediation remains blocked until the applicable capability and approval exist.

## Shared contract candidate

`docs/portable-security-contract-v0.md` now records a concrete pre-acceptance contract candidate. It defines required device, environment, ownership, platform-profile, baseline, policy, producer, time, nonce, expected-head, digest, and evidence identifiers; `PASS`/`FAIL`/`UNKNOWN`/`NOT_APPLICABLE` semantics; proposal, capability, receipt, revocation, correction, privacy, canonicalization, fixture, and versioning requirements.

The document reduces ambiguity but does not select a production key store, device-identity derivation, signature standard, platform baseline owner, or human approval owner. It is not an accepted schema or operational authority until Repository `1` carries an aligned version, both repositories pass the same deterministic fixtures at immutable heads, and the Architect approves the version.

## MVP roadmap

| Priority | Task | Depends on | Status |
|---|---|---|---|
| P0 | Repository health baseline for the implemented Autonomous vNext surface | — | IN PROGRESS |
| P0A | Approve the portable first-install product boundary and Repository `0`/`1` bootstrap contract | P0 evidence | REVIEW |
| P0B | Approve or revise Portable Security Contract v0 and assign contract ownership | P0A, Repository `1` alignment | REVIEW |
| P1 | Verify one end-to-end read-only portable-bootstrap mission and evidence bundle | P0, P0A, P0B | PROPOSED |
| P2 | Establish architecture, package, device-identity, baseline-policy, contract, and ADR compatibility | P1 | PROPOSED |
| P3 | Harden configuration, secrets, command/path policy, package sources, startup state, networking, Bluetooth/sharing, incident response, and rollback | P2 | PROPOSED |
| P4 | Package and document the verified Phase-0 runtime and per-platform baseline profiles | P3 | PROPOSED |
| P5 | Evaluate remote adapters, portfolio governance, VTX/private authority, scientific engines, and infrastructure automation as separate products | P4 and separate approval | BLOCKED |

## P0 repository-health path — draft PR #7

**Status:** `STALE REVIEW PATH — CURRENT HEAD LACKS ATTACHED EXACT-HEAD CI AND IS NON-MERGEABLE`

PR #7 documents the Python, Node/TypeScript/npm, and Bash-hook surfaces at head `991216f8c9f72a3bcb23b745f148697659217322`. The passing Autonomous vNext run applies to an earlier head. Current content corrections remain useful candidate evidence, but P0 must not advance until the submitted head is verified, the remaining material review thread is resolved, and the candidate is reconciled with current `main`, including merged Gods/Clan and comment-policy changes.

**Directive:** preserve PR #7 as historical P0 evidence or rebuild its inventory from current `main`. Do not mark the phase complete from superseded workflow results.

## VTX and Repository 1 boundary — draft PR #6

**Status:** `DEFERRED ARCHITECTURE AND SECURITY PROPOSAL`

PR #6 remains open, draft, and mergeable at head `beb8dd2974aa936d1c0a23989b19c18e28e40e95`. It proposes Repository `0` as a myelination/proposal layer, VTX envelope primitives, and a credential-gateway policy while keeping Repository `1` authoritative.

**Directive:** do not issue a token or merge the proposal into the bounded-mission release until Repository `1` authority, portable-bootstrap route semantics, device identity, baseline and evidence schema ownership, negative compatibility fixtures, credential custody, revocation, and rollback are approved. Reconcile any VTX envelope with Portable Security Contract v0 rather than creating a competing route or identity vocabulary.

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

The current documentation branch adds a Pages-ready MkDocs site covering the project overview, architecture, A.L.I.S.T.A.I.R.E. portfolio role, portable first-install security, Portable Security Contract v0, contracts, autonomous-development lifecycle, onboarding, security, operations, recovery, and release evidence. It also adds exact-head documentation validation. It does not modify runtime behavior or authorize Pages publication, credentials, merges, releases, deployments, Terraform apply, device administration, or owner-wide mutation.

**Directive:** require strict site rendering, link validation, existing repository CI, comparison with the aligned Repository `1` contract, and review of all claim/authority boundaries before merge. The documentation candidate does not complete P0, P0A, or P0B.

## Portfolio proposal rule

Scientific-discovery, VTX/private-authority, portfolio-governance, Jira, Terraform, remote administration, and other external-integration candidates remain bounded proposals or scaffolds until the core P0-P4 platform baseline and their own authority, security, evidence, incident, and rollback gates are accepted.

## Builder rules

Builders execute only the highest-priority unblocked task. Each task names files, tests, constraints, stop conditions, evidence, and rollback. Scope must not be widened to absorb an unrelated proposal or failure. A passing workflow validates only the exact tested head and cannot by itself authorize merge, release, deployment, credentials, device control, or infrastructure change.

## Builder log

Record commits, commands, workflow runs, artifact hashes, policy decisions, stop conditions, residual risks, and follow-up work.

- 2026-07-17 — PR #7 corrected repository inventory content but remained non-mergeable without attached exact-head CI for its current head.
- 2026-07-19 — PR #10 replaced the earlier portfolio-health proposal with a current-main, exact-head-validated, evidence-retaining candidate; governance and trusted-main acceptance remain open.
- 2026-07-19 — PR #11 merged Gods/Clan observability and Terraform scaffolds while preserving human approval for apply and releases and retaining a hardening punch list.
- 2026-07-19 — PR #12 merged the source comment-style policy and repository gate.
- 2026-07-20 — Added a documentation-only Pages, architecture, onboarding, security, operations, and release-evidence foundation without changing product priority or runtime scope.
- 2026-07-20 — Clarified Repository `0` and Repository `1` as the portable first-install security and recovery pair; added P0A and a read-only device-bootstrap outcome without activating device-control authority.
- 2026-07-20 — Added Portable Security Contract v0 and P0B, aligning the proposed cross-repository route, identifiers, result states, capability/receipt/revocation boundaries, privacy controls, and shared fixture requirements without adding implementation or privileged authority.
