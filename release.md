# Release Plan

## Current Decision

Status: `BLOCKED — HEALTH BASELINE, SECURITY, AND END-TO-END EVIDENCE REQUIRED`

Autonomous vNext has a substantial Phase-0 implementation and a defined first outcome: one reproducible, policy-gated, reversible local mission from contract intake through evidence report. P0 is `IN PROGRESS`, but no release is eligible. PR #7 now contains a documentation-only correction that records both Python and Node/TypeScript/npm surfaces, including the two MCP package manifests, scripts, dependency ranges, strict `ES2022`/`NodeNext` configuration, missing package lockfiles, and declared Node `>=20` runtime.

The correction resolves the content omission but is not yet accepted evidence. Autonomous vNext CI run `29565948627` passed only on earlier head `37f19f8c9560f2194bbdbf599e644d122324b994`; it does not verify the corrected submitted state. The corrected lineage beginning at `d4898cc2d96efd8ab1c6c796b03aee22d1287a6e` currently has no attached successful workflow run or commit status, GitHub reports the PR non-mergeable, and review-thread disposition remains open. The final corrected head must pass exact-head verification before Phase 1 item 1 can be accepted.

Draft PR #6 remains outside this candidate. Its proposed VTX envelope, Repository `0` proposal layer, private-authority publication design, and credential-gateway safeguards require a separately approved Repository `0` → Repository `1` contract. Head `09038ac55c7945b2abb013d59cf9a1b270a9e717` has failing Autonomous vNext CI run `29546692277`: the test step failed and all smoke and federation validation steps were skipped.

## Versioning

- Scheme: Semantic Versioning.
- First eligible candidate: `0.0.1-baseline`.
- PR #7 may contribute repository-health documentation only after the corrected final head passes exact-head verification and its review threads are resolved.
- Draft VTX/private-authority work is excluded from `0.0.1-baseline` and requires a later separately versioned architecture/security decision.
- Domain-specific scientific engines remain separate proposals until the core P0-P4 platform baseline is accepted.
- Tag only an immutable commit satisfying every included gate.

## Release Scope

- Verified repository inventory covering every implementation language, package manager, manifest, runtime, workflow, and deployment surface, including Python and Node/TypeScript/npm packages.
- Mission and action-record schemas.
- Deny-by-default policy, low-risk planning, bounded local execution, append-only audit/evidence, deterministic cognitive runtime, and federation proposal validation.
- One read-only or local-check mission from intake through plan, policy decision, execution result, evidence report, and rollback path.
- Clean environment, complete tests and smoke checks, security review, documentation verification, checksums, provenance, and rollback evidence.

## Explicit Exclusions

- Draft PR #6 and any Repository `0` myelination/proposal layer, VTX publication authority, credential gateway, remote adapter, webhook, or GitHub write path.
- Production secrets, keys, autonomous publication, silent remote mutation, destructive operations, and unrestricted networking.
- Scientific-discovery roadmap implementations before the core baseline is accepted.

## Selected Completed Work

None accepted for release. PR #7 now contains the corrected language/package/runtime inventory, but the correction has no successful workflow or commit status attached to its final submitted head, the review threads are unresolved, and the PR is currently non-mergeable. Existing source, tests, workflows, federation utilities, documentation, and Apache-2.0 licensing remain candidate inputs rather than releasable completed work.

## Planned Changelog Entries

- `Documentation`: verified repository map, supported Python and Node runtimes, package managers, manifests, workflows, generated-output boundaries, setup, and recovery instructions.
- `Added`: verified bounded mission control loop and evidence bundle.
- `Security`: policy, command/path, secret, dependency, network, subprocess, workflow-permission, patch-validation, and cross-runtime supply-chain findings.
- `Release`: baseline reports, source archive, checksums, provenance, and approval decision.
- `Excluded`: unapproved VTX/private-authority and cross-repository publication work.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0 is completed with evidence; included P1-P4 work is `DONE`. |
| Repository inventory | REVIEW | The Python and Node/TypeScript/npm content correction is present, but the final corrected head must pass exact-head CI and both review threads must be resolved. |
| Environment/build | PARTIAL | Manifest and runtime evidence is recorded, but the corrected head has no attached workflow; clean setup, lockfile consistency, Node build paths, schema/configuration checks, static validation, and supported platform matrix remain incomplete. |
| Tests/smoke | STALE | Run `29565948627` passed configured tests and smoke checks on an earlier head only. The final corrected head, complete P0 baseline, policy-denial paths, one end-to-end bounded mission, and release-candidate replay remain unverified. Draft PR #6 still fails during tests. |
| Security | NO EVIDENCE | Secrets, Python and npm dependencies, commands/paths, subprocesses, network, workflow permissions, patch application, generated artifacts, and authority boundaries are reviewed at the final candidate. |
| Federation/rollback | NO EVIDENCE | Stale proposals fail closed; retries are idempotent; one mission rollback restores the prior verified state. |
| Cross-repository contract | BLOCKED | Repository `0`/`1` authority, route semantics, package/schema ownership, and negative compatibility fixtures are approved before any VTX work is included. |
| Documentation | REVIEW | Purpose and the corrected initial language/package/runtime inventory exist; setup, platform assumptions, generated-output policy, recovery, exact-head verification, and review disposition remain incomplete. |
| Provenance | PARTIAL | PR #7 records source/blob identities and earlier-head workflow evidence; final-head workflow logs, complete commands, versions, reports, artifact hashes, attestations, and final-candidate provenance are absent. |
| Approval | PENDING | Explicit approval after all blocking gates pass. |

## Artifact Requirements

- Accepted Markdown and machine-readable repository-health report covering Python, Node/TypeScript/npm, manifests, lockfiles, workflows, runtimes, deployment descriptors, and generated outputs.
- Complete static, build, test, smoke, federation, security, documentation, and rollback reports at one immutable release-candidate commit.
- Representative mission contract, action records, and evidence report containing no secrets.
- Source archive, Python and npm dependency/SBOM records where applicable, SHA-256 checksums, and provenance manifest.
- Review-thread disposition map and exact-head workflow logs for every included candidate change.
- For any later VTX candidate: cross-repository contract fixture corpus, authority decision record, schema/package ownership record, compatibility results, credential-gateway threat model, and revocation evidence.

## Rollback Criteria

Withdraw the candidate if repository inventory omits an active language, package, runtime, workflow, or deployment surface; verification is non-reproducible; policy or stop conditions can be bypassed; stale proposals are accepted; retries duplicate actions; credentials or network authority exceed the mission; evidence is lost; documented commands fail; artifact hashes differ; cross-repository route semantics are inconsistent; or unapproved VTX/private-authority work enters the baseline. Restore the last reviewed commit or verified tag and retain failed-candidate evidence, workflow logs, and review dispositions.

## Unresolved Blockers

- PR #7's corrected final head has no attached successful workflow run or commit status; the earlier passing run applies only to a superseded head.
- The Node/TypeScript omission thread and the release-reconciliation thread remain unresolved; GitHub reports the PR non-mergeable.
- P0 and the remaining repository-health phases are incomplete.
- No complete clean-environment build/static/security/documentation/provenance bundle exists across both Python and Node surfaces.
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
- 2026-07-17: Reconciled the release gate after the package inventory correction. The correction is present, but acceptance remains blocked until the final corrected head passes exact-head CI and both review threads are resolved.