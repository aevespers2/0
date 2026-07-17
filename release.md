# Release Plan

## Current Decision

Status: `BLOCKED — HEALTH BASELINE, SECURITY, AND END-TO-END EVIDENCE REQUIRED`

Autonomous vNext has a substantial Phase-0 implementation and a defined first outcome: one reproducible, policy-gated, reversible local mission from contract intake through evidence report. P0 is `IN PROGRESS`, but no release is eligible. PR #7 now contains a documentation-only repository-health candidate covering Python, Node/TypeScript/npm, and the active Bash pre-push hook and operator-invoked activation path; its Phase 1 punch-list item remains pending.

The content corrections are not accepted release evidence. Autonomous vNext CI run `29565948627` passed only on earlier head `37f19f8c9560f2194bbdbf599e644d122324b994`. PR #7 has since advanced four commits beyond previously recorded head `8ebfd345881eff3e2b308e31934afdee596483f3` to current head `991216f8c9f72a3bcb23b745f148697659217322`; that current head has no attached workflow run or commit status, and GitHub reports the PR non-mergeable. Two review threads remain unresolved: the retained Node/TypeScript thread pending exact-head verification and an outdated rollback thread that still requires explicit disposition even though the current branch content now includes every candidate-touched documentation file. The PR body still identifies `8ebfd345881eff3e2b308e31934afdee596483f3` as the final submitted head, so candidate identity and provenance must be reconciled before acceptance.

Draft PR #6 remains outside this candidate. Its proposed VTX envelope, Repository `0` proposal layer, private-authority publication design, and credential-gateway safeguards require a separately approved Repository `0` → Repository `1` contract. Head `09038ac55c7945b2abb013d59cf9a1b270a9e717` has failing Autonomous vNext CI run `29546692277`: the test step failed and all smoke and federation validation steps were skipped.

Draft PR #8 is also excluded. Current head `f291db0446d84005a3764795ca880cafeec1ad4c` passed Portfolio Health Candidate CI run `29583289679` and Autonomous vNext CI run `29583289637`, and GitHub currently reports the PR mergeable. However, the candidate CI retained no artifacts and verifies compilation and registry structure only. It does not establish complete repository enumeration and pagination, finding accuracy, safe issue lifecycle, private/organization coverage, disabled-Issues behavior, partial-failure recovery, token scope and revocation, behavioral fixtures, provenance, or rollback. The PR remains draft and overlaps governance proposals in QSO-GENOMES and the closed QSO-FABRIC bootstrap path.

## Versioning

- Scheme: Semantic Versioning.
- First eligible candidate: `0.0.1-baseline`.
- PR #7 may contribute repository-health documentation only after one immutable final head is declared consistently in the PR body and release evidence, that exact head passes verification, and every material review thread is explicitly resolved.
- Draft VTX/private-authority work is excluded from `0.0.1-baseline` and requires a later separately versioned architecture/security decision.
- Draft portfolio-control-plane work is excluded from `0.0.1-baseline` and requires a separately versioned governance product after ownership, scope, credentials, behavioral validation, provenance, and rollback are approved.
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
- Draft PR #8 and any owner-wide scheduled scanner, portfolio token, central issue writer/closer, or autonomous recovery workflow.
- Production secrets, keys, autonomous publication, silent remote mutation, destructive operations, and unrestricted networking.
- Scientific-discovery roadmap implementations before the core baseline is accepted.

## Selected Completed Work

None accepted for release. PR #7 contains corrected source-level inventory and rollback content for Python, Node/TypeScript/npm, Bash hook activation, and every documentation file touched by the candidate, but current head `991216f8c9f72a3bcb23b745f148697659217322` has no successful workflow or commit status, is non-mergeable, retains two unresolved review threads, and is inconsistent with the head declared in the PR body. PR #8 has successful exact-head structural CI and is currently mergeable, but no retained artifacts or behavioral/governance acceptance evidence and remains draft and outside scope. Existing source, tests, workflows, hooks, federation utilities, documentation, and Apache-2.0 licensing remain candidate inputs rather than releasable completed work.

## Planned Changelog Entries

- `Documentation`: verified repository map, supported Python and Node runtimes, Bash hook/runtime activation, package managers, manifests, workflows, generated-output boundaries, setup, and recovery instructions.
- `Added`: verified bounded mission control loop and evidence bundle.
- `Security`: policy, command/path, secret, dependency, network, subprocess, workflow-permission, local-hook, patch-validation, and cross-runtime supply-chain findings.
- `Release`: baseline reports, source archive, checksums, provenance, and approval decision.
- `Excluded`: unapproved VTX/private-authority, cross-repository publication, and portfolio-governance control-plane work.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0 is completed with evidence; included P1-P4 work is `DONE`. |
| Repository inventory | REVIEW | Python, Node/TypeScript/npm, Bash hook activation, and complete documentation rollback scope are recorded, but a single final candidate head must be declared consistently, pass exact-head CI, and have every material review thread explicitly resolved. |
| Environment/build | PARTIAL | Manifest and runtime evidence is recorded, but current PR #7 head `991216f8c9f72a3bcb23b745f148697659217322` has no attached workflow; clean setup, lockfile consistency, Node build paths, Bash-hook activation/configuration, schema/configuration checks, static validation, and supported platform matrix remain incomplete. |
| Tests/smoke | STALE | Run `29565948627` passed configured tests and smoke checks on an earlier head only. The current submitted head, complete P0 baseline, Node builds, hook/configuration paths, policy-denial paths, one end-to-end bounded mission, and release-candidate replay remain unverified. Draft PR #6 still fails during tests. |
| Security | NO EVIDENCE | Secrets, Python and npm dependencies, commands/paths, subprocesses, network, workflow permissions, local Git hooks, patch application, generated artifacts, and authority boundaries are reviewed at the final candidate. |
| Federation/rollback | NO EVIDENCE | Stale proposals fail closed; retries are idempotent; one mission rollback restores the prior verified state; documentation-only rollback reverts every file touched by the candidate, including `release.md` and `changelog.md`. |
| Cross-repository contract | BLOCKED | Repository `0`/`1` authority, route semantics, package/schema ownership, and negative compatibility fixtures are approved before any VTX work is included. |
| Portfolio governance | BLOCKED | One canonical governance owner, explicit opt-in repository scope, least-privilege credential/revocation design, enumeration and pagination rules, exact-head success semantics, partial-failure recovery, safe issue lifecycle, deterministic behavioral fixtures, retained artifacts, and rollback are approved before PR #8 or an equivalent control plane is adopted. |
| Documentation | REVIEW | Purpose and the initial full language/package/runtime inventory exist; PR-body/current-head reconciliation, setup, platform assumptions, generated-output policy, recovery, exact-head verification, and explicit review-thread disposition remain incomplete. |
| Provenance | PARTIAL | PR #7 records source/blob identities and earlier-head workflow evidence, but its body identifies a superseded final head and the current head lacks workflow logs, complete commands, versions, reports, artifact hashes, attestations, and final-candidate provenance. PR #8 has exact-head successful runs but no retained artifacts and no behavioral evidence bundle. |
| Deployment | BLOCKED | `deploy.md` records the 2026-07-17 review; no deployment, portfolio schedule, token configuration, or issue-writing automation is authorized until an applicable release is explicitly ready and every deployment gate passes. |
| Approval | PENDING | Explicit approval after all blocking gates pass. |

## Artifact Requirements

- Accepted Markdown and machine-readable repository-health report covering Python, Node/TypeScript/npm, Bash hooks and activation, manifests, lockfiles, workflows, runtimes, deployment descriptors, and generated outputs.
- Complete static, build, test, smoke, federation, security, documentation, and rollback reports at one immutable release-candidate commit.
- Representative mission contract, action records, and evidence report containing no secrets.
- Source archive, Python and npm dependency/SBOM records where applicable, SHA-256 checksums, and provenance manifest.
- Review-thread disposition map and exact-head workflow logs for every included candidate change.
- For any later VTX candidate: cross-repository contract fixture corpus, authority decision record, schema/package ownership record, compatibility results, credential-gateway threat model, and revocation evidence.
- For any later portfolio-control-plane candidate: canonical-owner ADR, opt-in inventory, permission matrix, token issuance/revocation evidence, pagination and access-failure fixtures, zero/one/multiple-finding golden outputs, issue create/update/close/idempotency tests, partial-failure recovery evidence, retained JSON/Markdown artifacts, and disable/rollback procedure.

## Rollback Criteria

Withdraw the candidate if repository inventory omits an active language, package, runtime, hook, workflow, or deployment surface; task completion is recorded before acceptance; candidate identity is inconsistent across the PR body, release plan, workflow evidence, and artifacts; verification is non-reproducible; policy or stop conditions can be bypassed; stale proposals are accepted; retries duplicate actions; credentials or network authority exceed the mission; evidence is lost; documented commands fail; artifact hashes differ; cross-repository route semantics are inconsistent; or unapproved VTX/private-authority or portfolio-governance work enters the baseline. Restore the last reviewed commit or verified tag, revert every candidate-touched documentation file including `release.md` and `changelog.md`, disable any scheduled workflow or issue writer before credential revocation, and retain failed-candidate evidence, workflow logs, issue-state snapshots, and review dispositions.

## Unresolved Blockers

- PR #7 current head `991216f8c9f72a3bcb23b745f148697659217322` has no attached workflow run or commit status; the earlier passing run applies only to a superseded head, and GitHub reports the PR non-mergeable.
- Two PR #7 review threads remain unresolved. The Node/TypeScript thread remains open pending exact-head verification; an outdated rollback thread still requires explicit disposition even though the current branch content now includes `release.md` and `changelog.md` in rollback scope.
- PR #7's body still declares superseded head `8ebfd345881eff3e2b308e31934afdee596483f3` as final. Candidate head identity must be reconciled and frozen before CI replay, provenance capture, or acceptance.
- Draft PR #8 current head `f291db0446d84005a3764795ca880cafeec1ad4c` passed exact-head structural workflows and is currently mergeable, but retained no artifacts and lacks behavioral, credential, failure-recovery, issue-lifecycle, provenance, and rollback acceptance evidence.
- Approval is required to select one canonical portfolio-governance owner—preferably a dedicated governance/control repository unless Repository `0` ownership is justified—and reconcile the overlapping Repository `0`, QSO-GENOMES, and closed QSO-FABRIC proposals before any owner-wide schedule, portfolio token, or issue writer is activated.
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
- 2026-07-17: Deployment review found the Bash-hook omission and premature punch-list completion; both were corrected in the PR, but current-head verification remained absent.
- 2026-07-17: Recorded three release-gate defects at PR #7 head `8ebfd345881eff3e2b308e31934afdee596483f3`: incomplete review-thread disposition wording, Bash omission from the artifact checklist, and incomplete documentation rollback scope.
- 2026-07-17: Excluded draft PR #8 from `0.0.1-baseline`. Current head `f291db0446d84005a3764795ca880cafeec1ad4c` passed structural exact-head CI, but retained no artifacts and requires a canonical governance-owner and authority decision plus behavioral evidence before adoption.
- 2026-07-17: Reconciled PR #7 at current head `991216f8c9f72a3bcb23b745f148697659217322`. The release-gate and rollback content defects are corrected, but current-head CI/status evidence is absent, two threads remain unresolved, the PR is non-mergeable, and the PR body still declares a superseded final head. PR #8 is now mergeable but remains draft and excluded pending artifacts, behavioral validation, and governance approval.
