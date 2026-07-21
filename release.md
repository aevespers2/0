# Release Plan

## Current decision

Status: `BLOCKED — HEALTH BASELINE, PORTABLE-BOOTSTRAP CONTRACT, SECURITY, END-TO-END EVIDENCE, AND APPROVAL REQUIRED`

Autonomous vNext has substantial Phase-0 source, tests, federation utilities, portfolio-observability scaffolding, and a clarified first-install purpose: on a newly acquired, replaced, recovered, reset, or suspect owned device, Repository `0` should establish a read-only inventory and evidence-backed remediation proposal before higher-level A.L.I.S.T.A.I.R.E. services or ordinary tooling are trusted. Repository `1` remains the candidate independent baseline, capability, revocation, receipt, and recovery authority. P0 remains `IN PROGRESS`; no application, package, Pages site, device-management service, governance control plane, credential gateway, Terraform change, release, or deployment is approved by the presence of this implementation or documentation.

The documentation branch now contains [Portable Security Contract v0](docs/portable-security-contract-v0.md), a shared pre-acceptance route, identity, result-state, capability, receipt, revocation, correction, privacy, canonicalization, versioning, and fixture specification aligned with Repository `1`. This removes some documentary ambiguity but does not establish an accepted schema, contract owner, key store, signature standard, device identity, platform baseline, or operational authority.

## Current candidate state

- **PR #7:** open draft, non-mergeable, head `991216f8c9f72a3bcb23b745f148697659217322`; useful repository-inventory corrections, but the passing workflow applies to an earlier head and current-main reconciliation remains required.
- **PR #6:** open draft and mergeable, head `beb8dd2974aa936d1c0a23989b19c18e28e40e95`; VTX, Repository `0` proposal-layer, and credential-gateway candidate excluded from the first bounded portable-bootstrap release.
- **PR #10:** open draft and mergeable, head `7328cef2a6c9f033b3bee1720da51f567bad5b23`; exact-head candidate CI and retained evidence passed, but governance ownership, trusted-main behavior, token scope, issue lifecycle, and operational approval remain incomplete.
- **PR #11:** merged Gods observability/Jira and Clan Terraform scaffolds; automatic apply, release, and deployment remain human-approved, and `punchlists/gods-clan-pre-review.md` remains controlling hardening work.
- **PR #12:** merged the source comment-style policy and CI gate.
- **Documentation foundation:** Pages-ready architecture, portable first-install security, Portable Security Contract v0, contracts, autonomous-development, onboarding, security, operations, recovery, and release-evidence material is proposed without changing runtime behavior or passing product release gates.

## Versioning

- Scheme: Semantic Versioning.
- First eligible runtime candidate: `0.0.1-portable-baseline`.
- Shared portable-security contract candidate: `0.x` until both repositories pass the same fixture corpus and the Architect approves one immutable version.
- Tag only an immutable commit satisfying every included gate.
- Documentation and governance candidates do not inherit runtime release eligibility.
- Per-platform profiles must state their support level and may version independently from the core contract.
- VTX/private-authority, remote administration, portfolio-governance, Jira mutation, Terraform apply, and scientific-domain work require separately versioned and approved products or capabilities.

## First release scope

- Complete repository-health inventory for Python, Node/TypeScript/npm, Bash hooks, workflows, documentation, integrations, generated outputs, and deployment surfaces.
- Approved Repository `0`/`1` portable-bootstrap route, device identity, baseline policy, evidence envelope, capability, receipt, revocation, correction, and recovery contracts.
- Accepted Portable Security Contract version plus machine-readable schema examples and identical cross-repository fixtures.
- Mission and action-record schemas.
- Deny-by-default policy, low-risk planning, bounded local execution, append-only audit/evidence, deterministic cognitive runtime, and federation proposal validation.
- One read-only or local-check bootstrap mission covering supported portions of platform identity, package-manager state, startup persistence, accounts, certificates, network interfaces, DNS/proxy/VPN/routes, firewall, hotspot/tethering, sharing, and Bluetooth.
- Explicit `UNKNOWN` results for controls the platform or current permissions cannot inspect.
- Clean environment, complete applicable tests and smoke checks, security review, strict documentation build, provenance, checksums, and rollback evidence.

## Explicit exclusions

- unrestricted credentials, silent remote writes, protected-branch mutation, autonomous merge, publication, release, deployment, payment, destructive operations, intrusive surveillance, traffic interception, counter-intrusion, or control of devices without ownership or explicit authorization;
- automatic deletion or remediation based only on anomaly or suspicion;
- draft PR #6 and any VTX/private-authority or Repository `0` → Repository `1` transition without accepted ownership and compatibility contracts;
- draft PR #10 or equivalent owner-wide scanner as a release-authorizing control plane;
- automatic Jira mutation, Terraform apply, release, or deployment from merged PR #11 scaffolding;
- scientific-discovery roadmap implementations before the core baseline is accepted;
- claims that a successful check proves a device is uncompromised or that tensor-state abstractions are physical quantum computation.

## Acceptance gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0, P0A, and P0B are complete with evidence; included P1-P4 tasks are accepted. |
| Repository inventory | REVIEW | Rebuild or reconcile the inventory against current `main`, including merged integrations and policy surfaces, then verify the exact candidate head. |
| Portable product boundary | BLOCKED | Approve the first-install purpose, supported platforms, operator and device scope, Repository `0`/`1` responsibility split, and prohibited uses. |
| Portable Security Contract v0 | REVIEW | Align both repositories, select the canonical owner, approve or revise identifiers and semantics, add schemas and 18 fixture classes, and validate immutable exact heads. |
| Environment/build | PARTIAL | Clean setup, supported runtimes, lockfile state, package-manager checks, Bash-hook setup, documentation installation, and platform assumptions are reproduced. |
| Tests/smoke | PARTIAL | Current-main exact-head tests, cognitive smoke, policy denial, federation negative cases, documentation build, and one bounded bootstrap mission pass. |
| Platform profiles | NO ACCEPTED BUNDLE | macOS, Linux, Windows, Android, iOS, and constrained-environment controls are classified as supported, advisory, unavailable, or out of scope with deterministic fixtures where practical. |
| Security | NO ACCEPTED BUNDLE | Secrets, dependencies, actions, commands/paths, package sources, startup persistence, network, subprocess, Bluetooth/sharing, local hooks, patch application, credentials, artifacts, integrations, privacy, and authority boundaries are reviewed. |
| Federation/rollback | NO ACCEPTED BUNDLE | Stale and invalid proposals fail closed; retries are idempotent; rollback restores the prior verified state. |
| Cross-repository contract | BLOCKED | Repository `0`/`1` authority, bootstrap route, device identity, schema/package ownership, capability custody, receipt/revocation/correction semantics, canonicalization, and compatibility fixtures are approved. |
| Lost/replaced device recovery | NO EVIDENCE | Prior identity revocation, new-device bootstrap, minimum credential reissue, recovery evidence, and unsupported remote-revocation outcomes are documented and tested without live secrets. |
| Portfolio governance | BLOCKED | Canonical owner, opt-in scope, least privilege, pagination/access semantics, current-head rules, issue lifecycle, partial-failure recovery, evidence, disablement, and rollback are approved. |
| Gods/Clan integration | REVIEW | Pre-review punch list, credentials, workflow pinning, exact-head evidence, operational scope, and human-approval boundaries are accepted. |
| Documentation | REVIEW | Strict MkDocs rendering, local-link checks, exact-head evidence, claim review, cross-repository contract comparison, and publication decision pass. |
| Provenance | PARTIAL | Complete commands, versions, reports, source/archive hashes, dependency records, SBOM where applicable, attestations, and artifact retention bind to one head. |
| Deployment | BLOCKED | No package, Pages, scanner schedule, device agent, Jira writer, Terraform apply, release, or deployment is authorized until its own gates pass. |
| Approval | PENDING | Authorized human explicitly approves the exact head, scope, residual risks, and rollback. |

## Artifact requirements

- accepted machine-readable and Markdown repository-health report;
- approved portable-bootstrap charter, platform matrix, device-identity lifecycle, baseline-policy manifest, and Repository `0`/`1` contract;
- accepted Portable Security Contract source, machine-readable schemas, examples, fixture corpus, compatibility report, and version/migration record;
- complete static, build, test, smoke, federation, security, documentation, and rollback reports at one immutable candidate;
- representative mission, denial, device inventory, action, evidence, reflection, stale proposal, malformed proposal, replay, revocation, loss/replacement, correction, and recovery fixtures containing no secrets;
- source archive, dependency and SBOM records where applicable, SHA-256 manifest, and provenance statement;
- review-thread and contradiction disposition map;
- for portfolio governance: owner ADR, opt-in inventory, permission matrix, token issuance/revocation evidence, enumeration and failure fixtures, issue lifecycle/idempotency tests, retained artifacts, and disable/rollback procedure;
- for VTX/Repository `1`: owner ADR, route and state model, device/baseline schema versions, compatibility fixtures, key/capability custody, gateway threat model, revocation, and rollback;
- for Gods/Clan: accepted punch-list evidence, Jira and Terraform authority matrix, plan/apply separation, credential controls, and incident recovery.

## Rollback criteria

Withdraw or roll back when candidate identity is inconsistent; required source, runtime, or platform surfaces are omitted; exact-head verification is absent; commands are non-reproducible; policy or stop conditions can be bypassed; stale/replayed proposals are accepted; retries duplicate actions; credentials or network/device authority exceed scope; evidence is lost; artifact hashes differ; route, device identity, baseline, contract version, canonicalization, or schema semantics conflict; unsupported state is reported as secure; or an unapproved external writer, release, deployment, Terraform apply, remote administration, or governance action enters the candidate.

Restore the last verified commit or tag, revert candidate-touched source and documentation, disable schedules and external writers before revoking credentials, restore or compensate external state, and retain failed-candidate logs, artifacts, device inventories, issue snapshots, and review decisions.

## Unresolved blockers

- P0 has not been accepted against current `main`.
- The portable first-install charter and P0A are not approved.
- Portable Security Contract v0 remains a documentation candidate without approved owner, schemas, fixtures, key custody, signature/canonicalization standard, or human authority assignments.
- PR #7 is stale, non-mergeable, and lacks current-head attached CI.
- PR #6 requires Repository `1`, route, device identity, schema, capability, credential, and revocation decisions.
- PR #10 requires canonical governance ownership, trusted-main scan review, private-repository scope, token policy, issue lifecycle, and operational approval.
- Per-platform baseline controls, privacy/retention rules, clean-room bootstrap assumptions, and mobile limitations remain unspecified or unverified.
- Gods/Clan pre-review tasks remain open; merged scaffolding is not production authority.
- No complete current-main clean-environment, end-to-end bootstrap mission, security, documentation, provenance, and rollback bundle exists.
- Platform-specific Safari/Desktop federation behavior remains unverified for release.
- Pages publication and support ownership remain unapproved.

## Release log

- 2026-07-16 — Defined the bounded-mission `0.0.1-baseline` outcome and excluded VTX/private-authority work.
- 2026-07-17 — Recorded PR #7 as a repository-health candidate while retaining exact-head and review gates.
- 2026-07-19 — PR #10 replaced the earlier portfolio-health proposal with an exact-head-validated, evidence-retaining candidate; governance acceptance remains open.
- 2026-07-19 — PR #11 merged Gods/Clan scaffolding with human approval preserved for Terraform apply and releases.
- 2026-07-19 — PR #12 merged the source comment-style policy and CI gate.
- 2026-07-20 — Added a documentation-only Pages and developer-documentation foundation; runtime and release gates remain blocked.
- 2026-07-20 — Reframed the first eligible candidate as a portable, read-only device-security baseline paired with Repository `1`; no device-management or credential authority was activated.
- 2026-07-20 — Added Portable Security Contract v0 as a shared documentation candidate and introduced P0B; no machine-readable contract, fixture evidence, capability, credential, release, or deployment authority was activated.
