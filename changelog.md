# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product

- 2026-07-16 — Defined the first product outcome as one reproducible, policy-gated, reversible local mission from contract intake through evidence, reflection, and rollback.
- 2026-07-16 — Kept scientific-discovery, VTX/private-authority, and cross-repository publication work outside the active bounded-mission baseline.
- 2026-07-17 — Advanced the repository-health objective to `IN PROGRESS` through PR #7 while retaining exact-head and review gates.
- 2026-07-19 — Replaced the earlier portfolio-health proposal with draft PR #10, a current-main candidate that reports repository health but cannot authorize release or bypass repository gates.
- 2026-07-19 — Merged PR #11, adding Gods observability/Jira and Clan Terraform scaffolding while preserving human approval for Terraform apply and automatic releases.
- 2026-07-20 — Established Repository `0` in portfolio documentation as A.L.I.S.T.A.I.R.E.'s bounded autonomous-development and proposal layer, not the unilateral canonical-state or credential authority.
- 2026-07-20 — Clarified the primary long-term product role: Repository `0` and Repository `1` are the portable first-install security and recovery pair for newly acquired, replaced, recovered, reset, or suspect owned devices.
- 2026-07-20 — Reframed the first executable outcome as a read-only device-baseline mission before higher-level A.L.I.S.T.A.I.R.E. services or ordinary tooling are trusted.

### Architecture

- Replaced the generic greenfield roadmap with a sequence aligned to the implemented Phase-0 system.
- Recorded the unresolved Repository `0`/Repository `1` route, schema, package, capability, and canonical-state ownership decision.
- Separated cognition, planning, policy, local execution, evidence, proposal exchange, privileged external state, and canonical governance into explicit trust zones.
- Documented the autonomous-development capability ladder and the rule that higher authority requires separately accepted capability, evidence, incident, and rollback controls.
- Required portfolio health, Jira, Terraform, VTX, release, deployment, and self-modifying policy to remain distinct authority boundaries.
- Added a portable-bootstrap lifecycle covering trusted/minimally exposed startup, read-only inventory, local proposal, Repository `1` quarantine and decision, bounded remediation, resulting-state receipt, canonical reconciliation, and continuous low-authority monitoring.
- Added platform-control domains for package managers, startup persistence, accounts, certificates, network interfaces, DNS, proxy, VPN, routes, firewall, hotspot/tethering, sharing, Bluetooth, recovery, and unsupported-state handling.

### Implementation

- Existing mission, action, policy, audit, planner, executor, cognitive, memory, reflection, federation, and evidence components remain candidate inputs pending release evidence.
- PR #10 implements a repaired portfolio-health candidate with bounded enumeration, current-head semantics, exact-source checks, fail-closed errors, and retained evidence; the candidate remains draft.
- PR #11 introduced merged observability and Terraform-governance scaffolds without automatic apply or release authority.
- PR #12 introduced the source comment-style policy and CI gate while preserving URL/URI and quoted-string syntax.
- The documentation candidate adds only MkDocs configuration, Pages content, exact-head documentation validation, and planning/release-document reconciliation; runtime behavior is unchanged.
- No device inventory adapter, remediation command, credential, monitoring service, remote administration, or enforcement capability was added by the portable-bootstrap clarification.

### Documentation

- Added a Pages-ready project overview and navigation model.
- Added system, trust-zone, runtime-sequence, portfolio-role, continuous-development, state-machine, evidence, and recovery diagrams.
- Added contract, state, compatibility, autonomous-development, onboarding, security, operations, incident, rollback, and release-evidence guides.
- Added pinned documentation dependencies and a strict exact-head documentation workflow with local-link checks, deterministic site archive, SHA-256 evidence, and retained artifacts.
- Reconciled `taskchain.md` and `release.md` with current PR #6, #7, #10, merged PR #11 and #12, and the documentation-only candidate.
- Added `docs/portable-first-install.md` and aligned Pages, task chain, release plan, and punch list with the clarified device-security mission.

### Evidence

- PR #7 current head `991216f8c9f72a3bcb23b745f148697659217322` remains non-mergeable without attached exact-head CI; its earlier passing workflow does not validate the current head.
- PR #10 head `7328cef2a6c9f033b3bee1720da51f567bad5b23` passed Portfolio Health Candidate CI run `29668233233` and Autonomous vNext CI run `29668233229`; its retained artifact digest is `sha256:e207daabfd46d788b687b614592a9b06182ca246642a85e35274b0ad4d25069e`.
- Merged scaffolding and documentation do not constitute accepted runtime, security, release, device-control, or deployment evidence.

### Security

- Maintained deny-by-default treatment for credentials, protected branches, workflow and secret administration, destructive operations, publication, release, deployment, Terraform apply, device remediation, and policy/capability changes.
- Required exact-head identity, device identity, baseline-policy identity, schema validation, stale/replay checks, path and command controls, secret redaction, least privilege, revocation, independent verification, and rollback for consequential actions.
- Preserved human approval for credentials, merges, releases, deployments, infrastructure apply, payments, sensitive publication, privileged device changes, emergency exceptions, and self-modification of authority controls.
- Required unusual state to remain separate from attribution and unsupported controls to be reported as `UNKNOWN` rather than secure.

### Release

- The first eligible candidate is now described as `0.0.1-portable-baseline`, subject to approval of the portable product boundary and without changing implementation eligibility.
- The candidate remains blocked pending current-main repository health, clean environment, Repository `0`/`1` gluing contract, one end-to-end read-only bootstrap mission, complete applicable tests, platform profiles, security review, strict documentation validation, provenance, rollback, and explicit approval.
- Draft PR #6 and #10 remain excluded from release authority until their separate architecture, governance, credential, and operational gates pass.
- Merged Gods/Clan scaffolding remains subject to `punchlists/gods-clan-pre-review.md` and does not authorize Jira mutation, Terraform apply, release, or deployment.
- The documentation candidate does not complete P0 or P0A or authorize Pages publication.

### Deployment

- No package, Pages site, device agent, portfolio schedule, Jira writer, Terraform apply, release, or deployment is authorized by this documentation work.
- Pages publication, portfolio token configuration, external issue mutation, privileged device changes, remote administration, and infrastructure apply require separately approved deployment plans, credentials, incident ownership, and rollback.

## Entry format

- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable
