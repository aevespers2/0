# Release Plan

## Current Decision

Status: `BLOCKED — HEALTH AND END-TO-END EVIDENCE REQUIRED`

Autonomous vNext has a substantial Phase-0 implementation and a newly approved first outcome: one reproducible, policy-gated, reversible local mission from contract intake through evidence report. No release is eligible because P0 remains `READY`, every repository-health punch-list phase is unchecked, the evidence log is empty, and no current build, test, security, documentation, provenance, or rollback bundle is attached to candidate head `be3eb1a71c15d969e548d42219d27ca966d5641a`.

## Versioning

- Scheme: Semantic Versioning.
- First eligible candidate: `0.0.1-baseline`.
- Domain-specific scientific engines remain separate proposals until the core P0-P4 platform baseline is accepted.
- Tag only an immutable commit satisfying every included gate.

## Release Scope

- Mission and action-record schemas.
- Deny-by-default policy, low-risk planning, bounded local execution, append-only audit/evidence, deterministic cognitive runtime, and federation proposal validation.
- One read-only or local-check mission from intake through plan, policy decision, execution result, evidence report, and rollback path.
- Clean environment, complete tests and smoke checks, security review, documentation verification, checksums, provenance, and rollback evidence.

## Selected Completed Work

None selected. Existing source, tests, workflows, federation utilities, documentation, and Apache-2.0 licensing are candidate inputs, but no task is `DONE` and no current evidence bundle verifies them together.

## Planned Changelog Entries

- `Added`: verified bounded mission control loop and evidence bundle.
- `Security`: policy, command/path, secret, dependency, network, subprocess, workflow-permission, and patch-validation findings.
- `Documentation`: supported environment, operator workflow, limitations, stop conditions, and rollback.
- `Release`: baseline reports, source archive, checksums, provenance, and approval decision.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0 is completed with evidence; included P1-P4 work is `DONE`. |
| Environment/build | NO EVIDENCE | Clean setup, schema/configuration checks, static validation, and supported platform matrix are recorded. |
| Tests/smoke | NO EVIDENCE | Full suite, cognitive-runtime smoke, policy-denial paths, and one end-to-end bounded mission pass. |
| Security | NO EVIDENCE | Secrets, dependencies, commands/paths, subprocesses, network, workflow permissions, and patch application are reviewed. |
| Federation/rollback | NO EVIDENCE | Stale proposals fail closed; retries are idempotent; rollback restores the prior verified state. |
| Documentation | PARTIAL | Purpose and architecture exist; setup, platform assumptions, generated-output policy, and recovery are unverified. |
| Provenance | NO EVIDENCE | Commit, runtime/tool versions, commands, exit codes, reports, hashes, repository URL, and attestations are retained. |
| Approval | PENDING | Explicit approval after all blocking gates pass. |

## Artifact Requirements

- Markdown and machine-readable repository-health report.
- Complete static, test, smoke, federation, security, and rollback reports.
- Representative mission contract, action records, and evidence report containing no secrets.
- Source archive, SBOM where applicable, SHA-256 checksums, and provenance manifest.

## Rollback Criteria

Withdraw the candidate if verification is non-reproducible, policy or stop conditions can be bypassed, stale proposals are accepted, retries duplicate actions, credentials or network authority exceed the mission, evidence is lost, documented commands fail, or artifact hashes differ. Restore the last reviewed commit or verified tag and retain failed-candidate evidence.

## Unresolved Blockers

- P0 and all repository-health phases remain incomplete; the evidence log is empty.
- No current clean-environment CI/test/security/documentation/provenance bundle exists.
- One complete policy-gated mission and its rollback path have not been verified.
- Platform-specific Safari/Desktop federation behavior lacks release evidence.
- Scientific-discovery roadmap proposals remain intentionally outside the baseline release.

## Release Log

- 2026-07-16: Aligned the release scope with the approved bounded-mission MVP; candidate remains blocked pending repository health and end-to-end evidence.