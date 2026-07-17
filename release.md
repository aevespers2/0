# Release Plan

## Current Decision

Status: `BLOCKED — HEALTH BASELINE, SECURITY, AND END-TO-END EVIDENCE REQUIRED`

Autonomous vNext has a substantial Phase-0 implementation and a defined first outcome: one reproducible, policy-gated, reversible local mission from contract intake through evidence report. P0 is now `IN PROGRESS`, but no release is eligible. PR #7 at submitted head `37f19f8c9560f2194bbdbf599e644d122324b994` provides a documentation-only Phase 1 inventory candidate and exact-head Autonomous vNext CI run `29565948627` completed successfully, including tests, cognitive-runtime smoke, federation/status writers, proposal verification, relay checks, guarded patch application, and the federation state report.

That evidence does not complete or accept the repository-health baseline. One unresolved current review thread shows that the claimed language/package/runtime inventory omits the Node/TypeScript/npm surfaces under `packages/communication-fabric-mcp-template` and `packages/lifetime-network-mcp-server`, including their manifests, TypeScript sources, scripts, and declared Node `>=20` runtime. GitHub currently reports PR #7 non-mergeable. The candidate must be corrected on the same review path, reverified if its head changes, and accepted before any Phase 1 item or release scope is treated as complete.

Draft PR #6 remains outside this candidate. Its proposed VTX envelope, Repository `0` proposal layer, private-authority publication design, and credential-gateway safeguards require a separately approved Repository `0` → Repository `1` contract. Head `09038ac55c7945b2abb013d59cf9a1b270a9e717` has failing Autonomous vNext CI run `29546692277`: the test step failed and all smoke and federation validation steps were skipped.

## Versioning

- Scheme: Semantic Versioning.
- First eligible candidate: `0.0.1-baseline`.
- PR #7 may contribute repository-health documentation only after its inventory is corrected, the review finding is resolved, and exact-head evidence is retained.
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

None accepted for release. PR #7 records useful candidate inventory and a successful exact-head CI run, but its first Phase 1 item is incomplete because the Node/TypeScript/npm surface is omitted, the review thread is unresolved, and the PR is currently non-mergeable. Existing source, tests, workflows, federation utilities, documentation, and Apache-2.0 licensing remain candidate inputs rather than releasable completed work.

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
| Repository inventory | REVIEW | PR #7 records a bounded inventory candidate, but it must include or explicitly evidence exclusion of all Node/TypeScript/npm surfaces and resolve the current review thread. |
| Environment/build | PARTIAL | Exact-head CI succeeded for PR #7, but clean setup, manifest/lockfile consistency, Node build paths, schema/configuration checks, static validation, and supported platform matrix remain incomplete. |
| Tests/smoke | PARTIAL | Run `29565948627` passed configured tests and smoke checks at PR #7 head; the complete P0 baseline, policy-denial paths, one end-to-end bounded mission, and release-candidate replay remain unverified. Draft PR #6 still fails during tests. |
| Security | NO EVIDENCE | Secrets, Python and npm dependencies, commands/paths, subprocesses, network, workflow permissions, patch application, generated artifacts, and authority boundaries are reviewed at the final candidate. |
| Federation/rollback | NO EVIDENCE | Stale proposals fail closed; retries are idempotent; one mission rollback restores the prior verified state. |
| Cross-repository contract | BLOCKED | Repository `0`/`1` authority, route semantics, package/schema ownership, and negative compatibility fixtures are approved before any VTX work is included. |
| Documentation | REVIEW | Purpose and an initial inventory exist, but the inventory is materially incomplete and setup, platform assumptions, generated-output policy, and recovery remain unverified. |
| Provenance | PARTIAL | PR #7 records source/blob identities and exact-head workflow evidence; complete commands, versions, reports, artifact hashes, attestations, and final-candidate provenance are absent. |
| Approval | PENDING | Explicit approval after all blocking gates pass. |

## Artifact Requirements

- Corrected Markdown and machine-readable repository-health report covering Python, Node/TypeScript/npm, manifests, lockfiles, workflows, runtimes, deployment descriptors, and generated outputs.
- Complete static, build, test, smoke, federation, security, documentation, and rollback reports at one immutable release-candidate commit.
- Representative mission contract, action records, and evidence report containing no secrets.
- Source archive, Python and npm dependency/SBOM records where applicable, SHA-256 checksums, and provenance manifest.
- Review-thread disposition map and exact-head workflow logs for every included candidate change.
- For any later VTX candidate: cross-repository contract fixture corpus, authority decision record, schema/package ownership record, compatibility results, credential-gateway threat model, and revocation evidence.

## Rollback Criteria

Withdraw the candidate if repository inventory omits an active language, package, runtime, workflow, or deployment surface; verification is non-reproducible; policy or stop conditions can be bypassed; stale proposals are accepted; retries duplicate actions; credentials or network authority exceed the mission; evidence is lost; documented commands fail; artifact hashes differ; cross-repository route semantics are inconsistent; or unapproved VTX/private-authority work enters the baseline. Restore the last reviewed commit or verified tag and retain failed-candidate evidence, workflow logs, and review dispositions.

## Unresolved Blockers

- PR #7 omits the Node/TypeScript/npm packages and Node `>=20` runtime from the claimed Phase 1 inventory; one current review thread is unresolved and GitHub reports the PR non-mergeable.
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
- 2026-07-17: Recorded PR #7 as a bounded P0 health candidate. Exact-head CI passed, but the first inventory item remains unaccepted because Node/TypeScript/npm and Node `>=20` are omitted, the review finding is unresolved, and the PR is currently non-mergeable.
