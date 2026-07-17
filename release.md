# Release Plan

## Current Decision

Status: `BLOCKED — HEALTH, CONTRACT, AND END-TO-END EVIDENCE REQUIRED`

Autonomous vNext has a substantial Phase-0 implementation and a defined first outcome: one reproducible, policy-gated, reversible local mission from contract intake through evidence report. No release is eligible because P0 remains `READY`, every repository-health punch-list phase is unchecked, the evidence log is empty, and no current build, test, security, documentation, provenance, or rollback bundle is attached to reviewed implementation baseline `fb3f284abfce5473eec3de442a435bd038f0146b`.

Draft PR #6 is not part of this candidate. Its proposed VTX envelope, Repository `0` proposal layer, private-authority publication design, and credential-gateway safeguards require a separately approved Repository `0` → Repository `1` contract. The current PR head `09038ac55c7945b2abb013d59cf9a1b270a9e717` has failing Autonomous vNext CI run `29546692277`: the test step failed and all smoke and federation validation steps were skipped.

## Versioning

- Scheme: Semantic Versioning.
- First eligible candidate: `0.0.1-baseline`.
- Draft VTX/private-authority work is excluded from `0.0.1-baseline` and requires a later separately versioned architecture/security decision.
- Domain-specific scientific engines remain separate proposals until the core P0-P4 platform baseline is accepted.
- Tag only an immutable commit satisfying every included gate.

## Release Scope

- Mission and action-record schemas.
- Deny-by-default policy, low-risk planning, bounded local execution, append-only audit/evidence, deterministic cognitive runtime, and federation proposal validation.
- One read-only or local-check mission from intake through plan, policy decision, execution result, evidence report, and rollback path.
- Clean environment, complete tests and smoke checks, security review, documentation verification, checksums, provenance, and rollback evidence.

## Explicit Exclusions

- Draft PR #6 and any Repository `0` myelination/proposal layer, VTX publication authority, credential gateway, remote adapter, webhook, or GitHub write path.
- Production secrets, keys, autonomous publication, silent remote mutation, destructive operations, and unrestricted networking.
- Scientific-discovery roadmap implementations before the core baseline is accepted.

## Selected Completed Work

None selected. Existing source, tests, workflows, federation utilities, documentation, and Apache-2.0 licensing are candidate inputs, but no task is `DONE` and no current evidence bundle verifies them together. Draft PR #6 remains unmerged and is excluded from release consideration.

## Planned Changelog Entries

- `Added`: verified bounded mission control loop and evidence bundle.
- `Security`: policy, command/path, secret, dependency, network, subprocess, workflow-permission, and patch-validation findings.
- `Documentation`: supported environment, operator workflow, limitations, stop conditions, and rollback.
- `Release`: baseline reports, source archive, checksums, provenance, and approval decision.
- `Excluded`: unapproved VTX/private-authority and cross-repository publication work.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0 is completed with evidence; included P1-P4 work is `DONE`. |
| Environment/build | NO EVIDENCE | Clean setup, schema/configuration checks, static validation, and supported platform matrix are recorded. |
| Tests/smoke | FAIL | Full suite, cognitive-runtime smoke, policy-denial paths, federation checks, and one end-to-end bounded mission pass at the exact candidate commit. Current PR #6 CI fails during tests. |
| Security | NO EVIDENCE | Secrets, dependencies, commands/paths, subprocesses, network, workflow permissions, patch application, and authority boundaries are reviewed. |
| Federation/rollback | NO EVIDENCE | Stale proposals fail closed; retries are idempotent; rollback restores the prior verified state. |
| Cross-repository contract | BLOCKED | Repository `0`/`1` authority, route semantics, package/schema ownership, and negative compatibility fixtures are approved before any VTX work is included. |
| Documentation | PARTIAL | Purpose and architecture exist; setup, platform assumptions, generated-output policy, and recovery are unverified. |
| Provenance | NO EVIDENCE | Commit, runtime/tool versions, commands, exit codes, reports, hashes, repository URL, and attestations are retained. |
| Approval | PENDING | Explicit approval after all blocking gates pass. |

## Artifact Requirements

- Markdown and machine-readable repository-health report.
- Complete static, test, smoke, federation, security, and rollback reports.
- Representative mission contract, action records, and evidence report containing no secrets.
- Source archive, SBOM where applicable, SHA-256 checksums, and provenance manifest.
- For any later VTX candidate: cross-repository contract fixture corpus, authority decision record, schema/package ownership record, compatibility results, credential-gateway threat model, and revocation evidence.

## Rollback Criteria

Withdraw the candidate if verification is non-reproducible, policy or stop conditions can be bypassed, stale proposals are accepted, retries duplicate actions, credentials or network authority exceed the mission, evidence is lost, documented commands fail, artifact hashes differ, cross-repository route semantics are inconsistent, or unapproved VTX/private-authority work enters the baseline. Restore the last reviewed commit or verified tag and retain failed-candidate evidence.

## Unresolved Blockers

- P0 and all repository-health phases remain incomplete; the evidence log is empty.
- No current clean-environment CI/test/security/documentation/provenance bundle exists for the reviewed implementation baseline.
- One complete policy-gated mission and its rollback path have not been verified.
- Draft PR #6 current head fails CI during tests; all later smoke and federation checks are skipped.
- Repository `0` draft PR #6 and Repository `1` draft PR #1 disagree on whether the canonical route includes `0:proposal` before `1:quarantine`.
- Repository `1` authority, schema/package ownership, key/capability custody, credential-gateway boundary, and remote-write policy require approval.
- Platform-specific Safari/Desktop federation behavior lacks release evidence.
- Scientific-discovery roadmap proposals remain intentionally outside the baseline release.

## Release Log

- 2026-07-16: Aligned the release scope with the approved bounded-mission MVP; candidate remained blocked pending repository health and end-to-end evidence.
- 2026-07-16: Excluded draft PR #6 from `0.0.1-baseline`, recorded the Repository `0`/`1` route-contract decision gate, and marked its current failing CI run as an important release blocker.
