# Release Plan

## Current Decision

Status: `BLOCKED — HEALTH BASELINE, SECURITY, AND END-TO-END EVIDENCE REQUIRED`

Autonomous vNext has a substantial Phase-0 implementation and a defined first outcome: one reproducible, policy-gated, reversible local mission from contract intake through evidence report. P0 is `IN PROGRESS`, but no release is eligible. PR #7 contains a documentation-only repository-health candidate covering Python and Node/TypeScript/npm surfaces, but the inventory remains incomplete because the active Bash pre-push hook and its activation path are absent, while `punchlist.md` marks the item complete before its acceptance gates have passed.

Autonomous vNext CI run `29565948627` passed only on earlier head `37f19f8c9560f2194bbdbf599e644d122324b994`; it does not verify current submitted head `71ba0563bbbedfa1554c3f0edce70962fc199dc8`. The current head has no attached successful workflow run or commit status, GitHub reports the PR non-mergeable, and three review threads remain unresolved: the retained Node/TypeScript thread pending exact-head CI, the current premature punch-list-completion finding, and the current missing Bash-runtime finding. Exact-head verification and review disposition are required before Phase 1 item 1 can be accepted.

Draft PR #6 remains outside this candidate. Its proposed VTX envelope, Repository `0` proposal layer, private-authority publication design, and credential-gateway safeguards require a separately approved Repository `0` → Repository `1` contract. Head `09038ac55c7945b2abb013d59cf9a1b270a9e717` has failing Autonomous vNext CI run `29546692277`: the test step failed and all smoke and federation validation steps were skipped.

## Versioning

- Scheme: Semantic Versioning.
- First eligible candidate: `0.0.1-baseline`.
- PR #7 may contribute repository-health documentation only after the complete language/runtime inventory is corrected, the final head passes exact-head verification, Phase 1 item 1 remains pending until acceptance, and all material review threads are resolved.
- Draft VTX/private-authority work is excluded from `0.0.1-baseline` and requires a later separately versioned architecture/security decision.
- Domain-specific scientific engines remain separate proposals until the core P0-P4 platform baseline is accepted.
- Tag only an immutable commit satisfying every included gate.

## Release Scope

- Verified repository inventory covering every implementation language, package manager, manifest, runtime, workflow, deployment surface, and active local hook, including Python, Node/TypeScript/npm, and Bash automation.
- Mission and action-record schemas.
- Deny-by-default policy, low-risk planning, bounded local execution, append-only audit/evidence, deterministic cognitive runtime, and federation proposal validation.
- One read-only or local-check mission from intake through plan, policy decision, execution result, evidence report, and rollback path.
- Clean environment, complete tests and smoke checks, security review, documentation verification, checksums, provenance, and rollback evidence.

## Explicit Exclusions

- Draft PR #6 and any Repository `0` myelination/proposal layer, VTX publication authority, credential gateway, remote adapter, webhook, or GitHub write path.
- Production secrets, keys, autonomous publication, silent remote mutation, destructive operations, and unrestricted networking.
- Scientific-discovery roadmap implementations before the core baseline is accepted.

## Selected Completed Work

None accepted for release. PR #7 contains a corrected Python and Node/TypeScript/npm inventory, but it still omits the active Bash pre-push runtime, marks the Phase 1 item complete before acceptance, has no successful workflow or commit status on current head `71ba0563bbbedfa1554c3f0edce70962fc199dc8`, retains three unresolved threads, and is non-mergeable. Existing source, tests, workflows, hooks, federation utilities, documentation, and Apache-2.0 licensing remain candidate inputs rather than releasable completed work.

## Planned Changelog Entries

- `Documentation`: verified repository map, supported Python and Node runtimes, Bash hook/runtime activation, package managers, manifests, workflows, generated-output boundaries, setup, and recovery instructions.
- `Added`: verified bounded mission control loop and evidence bundle.
- `Security`: policy, command/path, secret, dependency, network, subprocess, workflow-permission, local-hook, patch-validation, and cross-runtime supply-chain findings.
- `Release`: baseline reports, source archive, checksums, provenance, and approval decision.
- `Excluded`: unapproved VTX/private-authority and cross-repository publication work.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0 is completed with evidence; included P1-P4 work is `DONE`. |
| Repository inventory | REVIEW | Python and Node/TypeScript/npm are recorded, but the active Bash pre-push hook and activation path are missing; Phase 1 item 1 must remain pending until the final corrected head passes exact-head CI and all material review threads are resolved. |
| Environment/build | PARTIAL | Manifest and runtime evidence is recorded, but the corrected head has no attached workflow; clean setup, lockfile consistency, Node build paths, Bash-hook activation/configuration, schema/configuration checks, static validation, and supported platform matrix remain incomplete. |
| Tests/smoke | STALE | Run `29565948627` passed configured tests and smoke checks on an earlier head only. The final corrected head, complete P0 baseline, Node builds, hook/configuration paths, policy-denial paths, one end-to-end bounded mission, and release-candidate replay remain unverified. Draft PR #6 still fails during tests. |
| Security | NO EVIDENCE | Secrets, Python and npm dependencies, commands/paths, subprocesses, network, workflow permissions, local Git hooks, patch application, generated artifacts, and authority boundaries are reviewed at the final candidate. |
| Federation/rollback | NO EVIDENCE | Stale proposals fail closed; retries are idempotent; one mission rollback restores the prior verified state. |
| Cross-repository contract | BLOCKED | Repository `0`/`1` authority, route semantics, package/schema ownership, and negative compatibility fixtures are approved before any VTX work is included. |
| Documentation | REVIEW | Purpose and the Python/Node inventory exist; the Bash hook/runtime, acceptance-state consistency, setup, platform assumptions, generated-output policy, recovery, exact-head verification, and review disposition remain incomplete. |
| Provenance | PARTIAL | PR #7 records source/blob identities and earlier-head workflow evidence; final-head workflow logs, complete commands, versions, reports, artifact hashes, attestations, and final-candidate provenance are absent. |
| Deployment | BLOCKED | `deploy.md` records the 2026-07-17 review; no deployment is authorized until a release is explicitly ready and every deployment gate passes. |
| Approval | PENDING | Explicit approval after all blocking gates pass. |

## Artifact Requirements

- Accepted Markdown and machine-readable repository-health report covering Python, Node/TypeScript/npm, Bash hooks, manifests, lockfiles, workflows, runtimes, deployment descriptors, and generated outputs.
- Complete static, build, test, smoke, federation, security, documentation, and rollback reports at one immutable release-candidate commit.
- Representative mission contract, action records, and evidence report containing no secrets.
- Source archive, Python and npm dependency/SBOM records where applicable, SHA-256 checksums, and provenance manifest.
- Review-thread disposition map and exact-head workflow logs for every included candidate change.
- For any later VTX candidate: cross-repository contract fixture corpus, authority decision record, schema/package ownership record, compatibility results, credential-gateway threat model, and revocation evidence.

## Rollback Criteria

Withdraw the candidate if repository inventory omits an active language, package, runtime, hook, workflow, or deployment surface; task completion is recorded before acceptance; verification is non-reproducible; policy or stop conditions can be bypassed; stale proposals are accepted; retries duplicate actions; credentials or network authority exceed the mission; evidence is lost; documented commands fail; artifact hashes differ; cross-repository route semantics are inconsistent; or unapproved VTX/private-authority work enters the baseline. Restore the last reviewed commit or verified tag and retain failed-candidate evidence, workflow logs, and review dispositions.

## Unresolved Blockers

- PR #7 current head `71ba0563bbbedfa1554c3f0edce70962fc199dc8` has no attached successful workflow run or commit status; the earlier passing run applies only to a superseded head.
- Three review threads remain unresolved, including current findings that the active Bash pre-push hook is absent from the inventory and Phase 1 item 1 is marked complete before exact-head verification and review closure; GitHub reports the PR non-mergeable.
- P0 and the remaining repository-health phases are incomplete.
- No complete clean-environment build/static/security/documentation/provenance bundle exists across Python, Node, and local-hook surfaces.
- One complete policy-gated mission and its rollback path have not been verified.
- Draft PR #6 current head fails CI during tests; all later smoke and federation checks are skipped.
- Repository `0` draft PR #6 and Repository `1` draft PR #1 disagree on whether the canonical route includes `0:proposal` before `1:quarantine`.
- Repository `1` authority, schema/package ownership, key/capability custody, credential-gateway boundary, and remote-write policy require approval.
- Platform-specific Safari/Desktop federation behavior lacks release evidence.
- Scientific-discovery roadmap proposals remain intentionally outside the baseline release.

## Release Log

- 2026-07-16: Aligned the release scope with the approved bounded-mission MVP; candidate remained blocked pending repository health and end-to-end evidence.
- 2026-07-16: Excluded draft PR #6 from `0.0.1-baseline`, recorded the Repository `0`/`1` route-contract decision gate, and marked its current failing CI run as an important release blocker.
- 2026-07-17: Recorded PR #7 as a bounded P0 health candidate. The earlier submitted head passed CI but omitted Node/TypeScript/npm evidence.
- 2026-07-17: Reconciled the package inventory correction, while retaining the exact-head CI and review-closure gates.
- 2026-07-17: Deployment review found two additional material acceptance defects: the active Bash pre-push hook is missing from the inventory and the punch list prematurely marks Phase 1 item 1 complete. Created `deploy.md` at commit `34eae9d3613db17ac24ca3f40060115142d19401`; no deployment was attempted.
