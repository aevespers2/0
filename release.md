# Release Plan

## Current decision

Status: `BLOCKED — HEALTH BASELINE, SECURITY, END-TO-END EVIDENCE, AND APPROVAL REQUIRED`

Autonomous vNext has substantial Phase-0 source, tests, federation utilities, portfolio-observability scaffolding, and a defined first outcome: one reproducible, policy-gated, reversible local mission from contract intake through evidence and reflection. P0 remains `IN PROGRESS`; no application, package, Pages site, governance control plane, credential gateway, Terraform change, release, or deployment is approved by the presence of this implementation or documentation.

## Current candidate state

- **PR #7:** open draft, non-mergeable, head `991216f8c9f72a3bcb23b745f148697659217322`; useful repository-inventory corrections, but the passing workflow applies to an earlier head and current-main reconciliation remains required.
- **PR #6:** open draft and mergeable, head `beb8dd2974aa936d1c0a23989b19c18e28e40e95`; VTX, Repository `0` proposal-layer, and credential-gateway candidate excluded from the first bounded-mission release.
- **PR #10:** open draft and mergeable, head `7328cef2a6c9f033b3bee1720da51f567bad5b23`; exact-head candidate CI and retained evidence passed, but governance ownership, trusted-main behavior, token scope, issue lifecycle, and operational approval remain incomplete.
- **PR #11:** merged Gods observability/Jira and Clan Terraform scaffolds; automatic apply, release, and deployment remain human-approved, and `punchlists/gods-clan-pre-review.md` remains controlling hardening work.
- **PR #12:** merged the source comment-style policy and CI gate.
- **Documentation foundation:** Pages-ready architecture, contracts, autonomous-development, onboarding, security, operations, recovery, and release-evidence material is proposed without changing runtime behavior or passing product release gates.

## Versioning

- Scheme: Semantic Versioning.
- First eligible runtime candidate: `0.0.1-baseline`.
- Tag only an immutable commit satisfying every included gate.
- Documentation and governance candidates do not inherit runtime release eligibility.
- VTX/private-authority, portfolio-governance, Jira mutation, Terraform apply, and scientific-domain work require separately versioned and approved products or capabilities.

## First release scope

- Complete repository-health inventory for Python, Node/TypeScript/npm, Bash hooks, workflows, documentation, integrations, generated outputs, and deployment surfaces.
- Mission and action-record schemas.
- Deny-by-default policy, low-risk planning, bounded local execution, append-only audit/evidence, deterministic cognitive runtime, and federation proposal validation.
- One read-only or local-check mission from intake through plan, policy decision, execution result, evidence report, reflection, and rollback.
- Clean environment, complete applicable tests and smoke checks, security review, strict documentation build, provenance, checksums, and rollback evidence.

## Explicit exclusions

- unrestricted credentials, silent remote writes, protected-branch mutation, autonomous merge, publication, release, deployment, payment, or destructive operations;
- draft PR #6 and any VTX/private-authority or Repository `0` → Repository `1` transition without accepted ownership and compatibility contracts;
- draft PR #10 or equivalent owner-wide scanner as a release-authorizing control plane;
- automatic Jira mutation, Terraform apply, release, or deployment from merged PR #11 scaffolding;
- scientific-discovery roadmap implementations before the core baseline is accepted;
- claims that tensor-state abstractions are physical quantum computation.

## Acceptance gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0 is complete with evidence; included P1-P4 tasks are accepted. |
| Repository inventory | REVIEW | Rebuild or reconcile the inventory against current `main`, including merged integrations and policy surfaces, then verify the exact candidate head. |
| Environment/build | PARTIAL | Clean setup, supported runtimes, lockfile state, Node package checks, Bash-hook setup, documentation installation, and platform assumptions are reproduced. |
| Tests/smoke | PARTIAL | Current-main exact-head tests, cognitive smoke, policy denial, federation negative cases, documentation build, and one bounded mission pass. |
| Security | NO ACCEPTED BUNDLE | Secrets, dependencies, actions, commands/paths, network, subprocess, local hooks, patch application, credentials, artifacts, integrations, and authority boundaries are reviewed. |
| Federation/rollback | NO ACCEPTED BUNDLE | Stale and invalid proposals fail closed; retries are idempotent; rollback restores the prior verified state. |
| Cross-repository contract | BLOCKED | Repository `0`/`1` authority, route semantics, schema/package ownership, capability custody, and compatibility fixtures are approved. |
| Portfolio governance | BLOCKED | Canonical owner, opt-in scope, least privilege, pagination/access semantics, current-head rules, issue lifecycle, partial-failure recovery, evidence, disablement, and rollback are approved. |
| Gods/Clan integration | REVIEW | Pre-review punch list, credentials, workflow pinning, exact-head evidence, operational scope, and human-approval boundaries are accepted. |
| Documentation | REVIEW | Strict MkDocs rendering, local-link checks, exact-head evidence, claim review, and publication decision pass. |
| Provenance | PARTIAL | Complete commands, versions, reports, source/archive hashes, dependency records, SBOM where applicable, attestations, and artifact retention bind to one head. |
| Deployment | BLOCKED | No package, Pages, scanner schedule, Jira writer, Terraform apply, release, or deployment is authorized until its own gates pass. |
| Approval | PENDING | Authorized human explicitly approves the exact head, scope, residual risks, and rollback. |

## Artifact requirements

- accepted machine-readable and Markdown repository-health report;
- complete static, build, test, smoke, federation, security, documentation, and rollback reports at one immutable candidate;
- representative mission, denial, action, evidence, reflection, stale proposal, malformed proposal, replay, and recovery fixtures containing no secrets;
- source archive, dependency and SBOM records where applicable, SHA-256 manifest, and provenance statement;
- review-thread and contradiction disposition map;
- for portfolio governance: owner ADR, opt-in inventory, permission matrix, token issuance/revocation evidence, enumeration and failure fixtures, issue lifecycle/idempotency tests, retained artifacts, and disable/rollback procedure;
- for VTX/Repository `1`: owner ADR, route and state model, schema/package versions, compatibility fixtures, key/capability custody, gateway threat model, revocation, and rollback;
- for Gods/Clan: accepted punch-list evidence, Jira and Terraform authority matrix, plan/apply separation, credential controls, and incident recovery.

## Rollback criteria

Withdraw or roll back when candidate identity is inconsistent; required source or runtime surfaces are omitted; exact-head verification is absent; commands are non-reproducible; policy or stop conditions can be bypassed; stale/replayed proposals are accepted; retries duplicate actions; credentials or network authority exceed scope; evidence is lost; artifact hashes differ; route or schema semantics conflict; or an unapproved external writer, release, deployment, Terraform apply, or governance action enters the candidate.

Restore the last verified commit or tag, revert candidate-touched source and documentation, disable schedules and external writers before revoking credentials, restore or compensate external state, and retain failed-candidate logs, artifacts, issue snapshots, and review decisions.

## Unresolved blockers

- P0 has not been accepted against current `main`.
- PR #7 is stale, non-mergeable, and lacks current-head attached CI.
- PR #6 requires Repository `1`, route, schema, capability, credential, and revocation decisions.
- PR #10 requires canonical governance ownership, trusted-main scan review, private-repository scope, token policy, issue lifecycle, and operational approval.
- Gods/Clan pre-review tasks remain open; merged scaffolding is not production authority.
- No complete current-main clean-environment, end-to-end mission, security, documentation, provenance, and rollback bundle exists.
- Platform-specific Safari/Desktop federation behavior remains unverified for release.
- Pages publication and support ownership remain unapproved.

## Release log

- 2026-07-16 — Defined the bounded-mission `0.0.1-baseline` outcome and excluded VTX/private-authority work.
- 2026-07-17 — Recorded PR #7 as a repository-health candidate while retaining exact-head and review gates.
- 2026-07-19 — PR #10 replaced the earlier portfolio-health proposal with an exact-head-validated, evidence-retaining candidate; governance acceptance remains open.
- 2026-07-19 — PR #11 merged Gods/Clan scaffolding with human approval preserved for Terraform apply and releases.
- 2026-07-19 — PR #12 merged the source comment-style policy and CI gate.
- 2026-07-20 — Added a documentation-only Pages and developer-documentation foundation; runtime and release gates remain blocked.
