# Punch List

## Current Task
**P0 / P0A — Repository health and portable first-install security baseline**

**Goal:** Produce a verified, reproducible baseline of the repository's current health and an approved portable-bootstrap contract before any device-remediation or higher-authority MVP implementation proceeds.

## Phase 0 — Portable Product Boundary and Repository `0`/`1` Contract
- [ ] Approve Repository `0` as the bootstrap, inspection, remediation-planning, bounded-execution, evidence, and maintenance layer for owned or explicitly authorized devices.
- [ ] Approve Repository `1` or an alternative as the independent baseline, capability, receipt, revocation, checkpoint, and recovery authority.
- [ ] Define the canonical route from Repository `0` local proposal to Repository `1` quarantine and decision.
- [ ] Define device identity, ownership scope, replacement/retirement state, baseline-policy identity, and supported platform profile identity.
- [ ] Define inventory, proposal, capability, execution-receipt, resulting-state, revocation, freeze, and recovery-checkpoint envelopes.
- [ ] Define exact human approvals for privileged remediation, credential changes, account changes, certificate/profile changes, network routing, firewall, hotspot/tethering, Bluetooth/sharing, package removal, and destructive recovery.
- [ ] Define prohibited uses: unauthorized-device control, interception, counter-intrusion, covert monitoring, automatic deletion, evidence destruction, and unsupported claims of compromise or security.
- [ ] Define privacy, redaction, retention, export, and deletion requirements for device inventories.
- [ ] Record unsupported or unobservable controls as `UNKNOWN` rather than compliant.
- [ ] Add shared positive, negative, stale, replay, unsupported-version, expected-head, wrong-device, partial-failure, revocation, freeze, and rollback fixtures with Repository `1`.

**Acceptance criteria:** The portable first-install role, device scope, Repository `0`/`1` authority split, cross-repository route, schemas, platform support model, prohibited uses, privacy rules, stop conditions, and rollback are approved without activating credentials or device-control authority.

## Phase 1 — Repository Inventory
- [ ] Record the repository purpose, default branch, primary languages, package managers, and runtime versions.
- [ ] Inventory top-level directories and identify application, library, script, test, documentation, configuration, and generated-output areas.
- [ ] Inventory all manifests, lockfiles, build files, container files, and deployment descriptors.
- [ ] Inventory all GitHub Actions workflows, reusable workflows, Dependabot configuration, issue templates, and security policy files.
- [ ] List open pull requests, open issues, stale branches, and recent commits that may affect the baseline.

**Acceptance criteria:** A concise repository map exists and every discovered build, test, CI, or deployment entry point is identified.

## Phase 2 — Environment and Dependency Baseline
- [ ] Determine the supported operating systems and runtime versions.
- [ ] Verify dependency manifests and lockfiles are mutually consistent.
- [ ] Identify outdated, deprecated, unmaintained, duplicated, or conflicting dependencies.
- [ ] Identify dependencies with known security advisories or unsupported runtime requirements.
- [ ] Record commands for clean installation in a fresh environment.
- [ ] Confirm secrets and credentials are not committed in tracked files or examples.
- [ ] Define trusted-bootstrap assumptions for a new, recovered, or suspect device before Homebrew or another package manager is trusted.

**Acceptance criteria:** A clean-install command sequence is documented, dependency risks are classified, and no unresolved credential exposure remains unreported.

## Phase 3 — Build and Static Validation
- [ ] Run or inspect the canonical build command.
- [ ] Run formatting checks.
- [ ] Run linting and static analysis.
- [ ] Run type checking where applicable.
- [ ] Validate configuration, schemas, JSON, YAML, TOML, and Markdown links where applicable.
- [ ] Record all warnings separately from failures.

**Acceptance criteria:** Every available static validation command has a recorded PASS, FAIL, or NOT CONFIGURED result with evidence.

## Phase 4 — Test Baseline
- [ ] Discover all unit, integration, end-to-end, smoke, and regression tests.
- [ ] Run the complete test suite from a clean environment where possible.
- [ ] Record test count, duration, skipped tests, flaky tests, and failures.
- [ ] Identify untested critical paths.
- [ ] Confirm test fixtures are deterministic and do not require undocumented secrets or external services.
- [ ] Establish a minimal smoke test if no executable test baseline exists.
- [ ] Specify one read-only portable-bootstrap fixture for each supported platform profile.

**Acceptance criteria:** The current test state is reproducible, failures are linked to causes or follow-up items, and critical coverage gaps are documented.

## Phase 5 — GitHub Actions and Automation Audit
- [ ] Inspect each workflow trigger, permissions block, runner, timeout, cache, artifact, and concurrency setting.
- [ ] Identify deprecated action versions or deprecated Node runtimes.
- [ ] Confirm workflows use least-privilege permissions.
- [ ] Confirm untrusted pull requests cannot access secrets or privileged write operations.
- [ ] Check that required build, lint, test, and security jobs are represented.
- [ ] Review recent workflow runs and classify failures as current, intermittent, obsolete, or configuration-related.
- [ ] Produce a focused upgrade list for failing or deprecated Actions.

**Acceptance criteria:** Each workflow has a health status, security assessment, and explicit remediation item where needed.

## Phase 6 — Security and Supply-Chain Baseline
- [ ] Run or configure dependency vulnerability scanning.
- [ ] Run or configure secret scanning and credential-pattern checks.
- [ ] Review unsafe shell usage, arbitrary code execution paths, deserialization, file handling, network calls, and subprocess boundaries.
- [ ] Review installation scripts and CI steps for unpinned downloads or mutable references.
- [ ] Confirm generated artifacts and reports preserve provenance.
- [ ] Identify missing SECURITY.md, reporting instructions, or threat-model documentation.
- [ ] Threat-model package sources, shell initialization, launch agents, scheduled tasks, system services, extensions, device-management profiles, certificates, DNS, proxies, VPNs, routes, forwarding, firewall, hotspot/tethering, sharing, and Bluetooth.
- [ ] Define read-only inventory commands separately from any remediation commands.
- [ ] Verify that no inventory finding can automatically authorize a privileged change.

**Acceptance criteria:** High-risk findings are explicitly listed, supply-chain and device-boundary weaknesses are documented, and no severe finding is silently deferred.

## Phase 7 — Documentation and Reproducibility Audit
- [ ] Verify README setup and usage instructions against the actual repository.
- [ ] Confirm all documented commands and paths exist.
- [ ] Identify undocumented prerequisites, environment variables, services, and platform assumptions.
- [ ] Verify license, contribution guidance, changelog, and release notes status.
- [ ] Record the shortest reproducible path from clone to successful smoke test.
- [ ] Verify the portable-first-install guide, platform matrix, device identity lifecycle, lost/replaced-device workflow, and Repository `1` contract remain aligned.

**Acceptance criteria:** A new contributor can follow the documented path without hidden steps, or every blocking documentation gap is listed.

## Phase 8 — Defect and Regression Triage
- [ ] Consolidate failures from dependencies, build, lint, type checks, tests, workflows, security checks, documentation validation, and portable-bootstrap fixtures.
- [ ] Separate confirmed defects from warnings, technical debt, missing features, and unverified hypotheses.
- [ ] Rank findings by severity, user impact, exploitability, and MVP blocking effect.
- [ ] Identify likely recently introduced regressions using commit history and workflow evidence.
- [ ] Create bounded follow-up tasks with files, acceptance criteria, and verification commands.
- [ ] Keep unusual state separate from attribution; do not treat an anomaly as proof of a particular attacker.

**Acceptance criteria:** Every significant finding has a severity, evidence source, owner role, and next action.

## Phase 9 — Baseline Report and Gate Decision
- [ ] Create or update a repository health report containing the inventory, commands run, results, failures, warnings, and unresolved risks.
- [ ] Record exact tool and runtime versions.
- [ ] Record the commit SHA used for the baseline.
- [ ] Record supported, advisory, unavailable, and out-of-scope controls for each platform profile.
- [ ] Mark P0 and P0A as PASS, CONDITIONAL PASS, or FAIL independently.
- [ ] Unlock P1 only when no unclassified critical blocker remains and the portable product boundary is approved.
- [ ] Update `taskchain.md` with the result and Builder log evidence.

**Acceptance criteria:** The baseline is reproducible from the recorded commit and provides a clear go/no-go decision for the first read-only portable-bootstrap mission.

## Builder Execution Order
1. Complete Phase 0 in parallel with read-only Phase 1 evidence preparation.
2. Complete Phase 1 and Phase 2.
3. Complete Phase 3 and Phase 4.
4. Complete Phase 5 and Phase 6.
5. Complete Phase 7 and Phase 8.
6. Complete Phase 9 and update `taskchain.md`.

## Evidence Log
Record commit links, commands, outputs, workflow URLs, issue references, blockers, platform limitations, privacy decisions, and remediation tasks below.

- 2026-07-20 — Added the portable first-install product-boundary, platform, device-identity, Repository `0`/`1` gluing, privacy, and fail-closed evidence requirements. No implementation or privileged authority was enabled.
