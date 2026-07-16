# Release Plan

## Current Decision
Status: `BLOCKED`

Autonomous vNext has a defined purpose and a substantial Phase-0 implementation, but no release is eligible. P0 remains `READY`, every repository-health punch-list phase is unchecked, the evidence log is empty, and no current build, test, security, documentation, or provenance result is attached to reviewed implementation head `957c836d51b676680d99e0e3faa62b8014da7e5b`.

## Versioning
- Scheme: Semantic Versioning.
- First eligible baseline candidate: `0.0.1-baseline`.
- A functional pre-release may follow only after the baseline identifies the supported Python/platform matrix and verifies the public APIs and federation boundaries.
- Do not tag merely because source files, tests, or a workflow are present; the recorded candidate commit must satisfy every included gate.

## Candidate Scope
- Mission and action-record schemas.
- Deny-by-default policy, planning, execution, audit, reflection, memory, and deterministic cognitive-runtime primitives.
- Local-authoritative federation status, proposal validation, dispatch, relay, recovery, and patch-application controls.
- Reproducible environment and dependency inventory.
- Full tests, cognitive-runtime smoke test, federation checks, security assessment, and documentation verification.
- Provenance-linked baseline report, checksums, and rollback instructions.

## Existing Candidate Assets
- `README.md` and `AUTONOMOUS_VNEXT.md` define the product purpose, architecture, non-goals, and operator commands.
- Mission/action schemas, runtime modules, federation utilities, tests, and `.github/workflows/autonomous-vnext-ci.yml` are present.
- Apache-2.0 licensing is present.

These assets are implemented inputs to the baseline; they are not selected as releasable work until the commands and gates below are independently reproduced at one immutable commit.

## Selected Completed Work
None. No task is `DONE`, and no evidence bundle ties the existing implementation to a clean environment, current CI run, security review, artifact hashes, and release approval.

## Planned Changelog Entries
- `Added`: verified Phase-0 mission, policy, audit, cognitive-runtime, and federation baseline.
- `Security`: deny-by-default command/path review, secret scan, dependency review, workflow-permission review, and guarded patch-application findings.
- `Documentation`: verified setup, supported platforms, operator workflow, limitations, and rollback instructions.
- `Release`: provenance manifest, baseline reports, checksums, and candidate decision.

## Acceptance Gates
| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0 phases completed, evidence logged, and P0 marked `DONE` or approved `CONDITIONAL PASS`. |
| Environment/dependencies | NO EVIDENCE | Supported Python/platform matrix and clean setup commands recorded; undeclared requirements classified. |
| Build/static validation | NO EVIDENCE | Schema/JSON checks, formatting/lint/type checks where configured, and workflow syntax results recorded. |
| Tests/smoke | NO EVIDENCE | Full pytest suite, cognitive-runtime smoke, and federation checks pass from a clean environment. |
| Security | NO EVIDENCE | Secret, dependency, command/path, subprocess, network, workflow-permission, and patch-application boundaries reviewed. |
| Documentation | PARTIAL | Purpose, architecture, commands, and license exist; commands, platform assumptions, generated-output policy, and rollback remain unverified. |
| Provenance | NO EVIDENCE | Candidate commit, tool/runtime versions, commands, exit codes, reports, artifact hashes, and repository URL recorded. |
| Repository-specific criteria | FAIL | Local-authoritative federation behavior, stale-head rejection, idempotency, and rollback are not attached to a current evidence bundle. |
| Approval | PENDING | Explicit release approval after all blocking gates pass. |

## Artifact Requirements
- Repository-health report in Markdown and machine-readable JSON.
- Complete test, smoke, static-validation, and federation reports.
- Dependency inventory, secret/security report, and workflow-permission review.
- Source archive and any generated reports with SHA-256 checksums.
- Provenance manifest containing commit SHA, Python/OS/tool versions, commands, timestamps, repository URL, and artifact hashes.

## Rollback Criteria
Withdraw the candidate if verification is non-reproducible, policy can be bypassed, patch validation accepts stale or unapproved input, federation actions duplicate or exceed authority, a severe security finding remains, documented commands fail, or artifact hashes differ. Before the first verified tag, rollback means deleting the candidate tag/release and returning to the reviewed pre-release commit while preserving failed-candidate evidence.

## Unresolved Blockers
- P0 and all nine punch-list phases remain unchecked; the evidence log is empty.
- The current CI workflow and pytest suite have not been linked to a successful run for the candidate commit.
- No clean-environment dependency/runtime baseline, security scan, or provenance bundle is recorded.
- macOS/Safari/Desktop relay behavior is platform-specific and lacks current release evidence.
- Generated and ignored runtime reports are not packaged under an explicit artifact-retention and checksum policy.

## Release Log
- 2026-07-16: Reconciled the release plan with the implemented Autonomous vNext surface; candidate remains `BLOCKED` pending the full P0 evidence baseline.