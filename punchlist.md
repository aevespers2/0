# Punch List

## Current Task
**P0 — Repository health baseline**

**Goal:** Produce a verified, reproducible baseline of the repository's current health before MVP implementation proceeds.

## Phase 1 — Repository Inventory
- [x] Record the repository purpose, default branch, primary languages, package managers, and runtime versions. Evidence: `docs/repository-health-baseline.md` on `builder/repository-purpose-runtime-baseline-v1`; baseline source commit `7333f441138bdc0d596232581c52e5e1134cd142`.
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

**Acceptance criteria:** High-risk findings are explicitly listed, supply-chain weaknesses are documented, and no severe finding is silently deferred.

## Phase 7 — Documentation and Reproducibility Audit
- [ ] Verify README setup and usage instructions against the actual repository.
- [ ] Confirm all documented commands and paths exist.
- [ ] Identify undocumented prerequisites, environment variables, services, and platform assumptions.
- [ ] Verify license, contribution guidance, changelog, and release notes status.
- [ ] Record the shortest reproducible path from clone to successful smoke test.

**Acceptance criteria:** A new contributor can follow the documented path without hidden steps, or every blocking documentation gap is listed.

## Phase 8 — Defect and Regression Triage
- [ ] Consolidate failures from dependencies, build, lint, type checks, tests, workflows, security checks, and documentation validation.
- [ ] Separate confirmed defects from warnings, technical debt, missing features, and unverified hypotheses.
- [ ] Rank findings by severity, user impact, exploitability, and MVP blocking effect.
- [ ] Identify likely recently introduced regressions using commit history and workflow evidence.
- [ ] Create bounded follow-up tasks with files, acceptance criteria, and verification commands.

**Acceptance criteria:** Every significant finding has a severity, evidence source, owner role, and next action.

## Phase 9 — Baseline Report and Gate Decision
- [ ] Create or update a repository health report containing the inventory, commands run, results, failures, warnings, and unresolved risks.
- [ ] Record exact tool and runtime versions.
- [ ] Record the commit SHA used for the baseline.
- [ ] Mark P0 as PASS, CONDITIONAL PASS, or FAIL.
- [ ] Unlock P1 only when no unclassified critical blocker remains.
- [ ] Update `taskchain.md` with the result and Builder log evidence.

**Acceptance criteria:** The baseline is reproducible from the recorded commit and provides a clear go/no-go decision for the next MVP task.

## Builder Execution Order
1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 and Phase 4.
3. Complete Phase 5 and Phase 6.
4. Complete Phase 7 and Phase 8.
5. Complete Phase 9 and update `taskchain.md`.

## Evidence Log
Record commit links, commands, outputs, workflow URLs, issue references, blockers, and remediation tasks below.

- 2026-07-17 — Completed bounded Phase 1 item 1 on `builder/repository-purpose-runtime-baseline-v1`. Recorded purpose, `main` default branch, Python/JSON/YAML/Markdown roles, pip behavior, absent root Python manifests, Ubuntu/Python 3.11 CI runtime, source blob identities, stop condition, and rollback in `docs/repository-health-baseline.md`. No runtime or workflow behavior changed.
