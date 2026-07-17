# Portfolio Lifecycle Plan

> **Evidence-only coordination record.** This file does not approve a merge, release, deployment, token, schedule, issue writer, network path, or cross-repository mutation. Repository-local `taskchain.md`, `punchlist.md`, `release.md`, and `deploy.md` remain authoritative for implementation and acceptance details.

Reviewed: **2026-07-17 14:01 PDT**  
Scope: **16 owned repositories**  
Portfolio decision: **No repository is release-ready or deployment-ready.**  
Current issue evidence: Bridge Issues #4–#9 and #14–#21 remain deferred proposals outside its first-release boundary. QuantumStateObjects now has one canonical exact-head candidate, PR #6, but three unresolved configuration-contract findings block acceptance; QSO-GENOMES PR #2 remains the highest cross-repository unblocker and retains unresolved review findings.

## Portfolio priority and architecture handoff

1. **QSO-GENOMES:** repair, reconcile, and freeze canonical PR #2 with exact-head, dependency, provenance, immutable-contract, Aequitas, manifest, and downstream-consumer evidence; keep governance PR #3 and Experimenters PR #4 separate and excluded.
2. **QuantumStateObjects:** repair PR #6's schema/hash-pin mismatch, repository/path contract bypass, and canonical-name casing; rerun exact-head CI, resolve review threads, then complete merged-head and local runtime/message/ledger/freeze evidence. Keep Experimenters PR #3 deferred.
3. **QSO-SEEKER:** obtain Architect disposition of the P0 baseline; keep action-orchestration PR #4 outside the hostile-input MVP unless separately chartered.
4. **QSO-FABRIC:** reproduce and accept the existing four-QSO runtime before considering Experimenters runtime PR #2.
5. **qso-field.github.io:** review PR #19's link baseline, then continue claim, accessibility, privacy/licensing, reproducibility, and upstream-contract gates.
6. **Bridge:** lifecycle planning is structurally complete through `taskchain.md`, `punchlist.md`, `release.md`, and `deploy.md`; implementation remains blocked on current-head reproduction.
7. All other repositories remain at their documented charter, provenance, incident, ownership, or evidence-baseline holds.

## Shared lifecycle controls

For every repository, the lifecycle record must preserve the product objective, user outcome, MVP boundary, priority, architecture handoff, acceptance criteria, non-goals, versioning and changelog intent, required artifacts, deployment environment and permissions, health checks, observability, rollback triggers/procedure, and post-deployment validation. No repository may be marked ready until repository-specific tests, security, documentation, provenance, permissions, environment, rollback, and acceptance criteria pass at one immutable source head. Structural planning, local replay, merge-ref CI, exact-head focused tests, or retained candidate artifacts do not authorize release when independent review, merged-head verification, full runtime behavior, upstream contracts, privacy/licensing, or rollback remain incomplete.

## aevespers2/0

- **Objective / outcome / MVP / priority:** establish a reproducible Autonomous vNext health baseline and prove one policy-gated, reversible local mission; P0 repository inventory and health precede mission expansion, scientific engines, VTX/private publication, or portfolio governance.
- **Handoff / acceptance / non-goals:** Architect dispositions PR #7 evidence; clean setup, full tests, policy denial, stop conditions, federation rejection, provenance, and rollback must pass. No credentials, silent remote writes, destructive operations, or owner-wide issue automation.
- **Release / artifacts / deploy / recovery:** blocked `0.0.1-baseline`; require repository map, exact-head logs, security/static/test reports, mission evidence, source archive, checksums, provenance, review dispositions, bounded health/observability, and rollback. Restore all candidate-touched files and rerun non-mutating validation after rollback.

## aevespers2/1

- **Objective / outcome / MVP / priority:** decide the Partitioned Versioning Trust Core charter and reconcile the Repository `0` → Repository `1` route; P0 is a local-only deny-by-default transition, receipt, checkpoint, recovery, and advisory path-audit model.
- **Handoff / acceptance / non-goals:** Architect chooses whether `0:proposal` is authoritative, staging, or removed; deterministic positive/negative, replay/expiry, receipt chaining, checkpoint recovery, threat-model, and capability-lifecycle evidence are required. No remote service, production secrets, or autonomous approval.
- **Release / artifacts / deploy / recovery:** no eligible version; require schemas, fixtures, token-preflight tests, threat model, clean-checkout logs, key/capability lifecycle, provenance, health checks, and rollback. Keep operations local and verify no credential or remote writer mutates canonical history.

## aevespers2/AionUi

- **Objective / outcome / MVP / priority:** determine mirror, maintained fork, or derivative identity and reproduce inherited AionUi 1.7.0; provenance, naming, notices, supported platform, clean npm baseline, reproducible build, security/accessibility, and rollback precede features or binaries.
- **Handoff / acceptance / non-goals:** Architect and user approve product/distribution identity and upstream baseline; require divergence report, `npm ci`, lint/format/tests, platform smoke, credential/storage/network review. No rebranding or unsigned public binaries before acceptance.
- **Release / artifacts / deploy / recovery:** preserve inherited 1.7.0 history; local changes need differentiated prerelease/changelog. Require license/notices, dependency/SBOM, build/test logs, platform artifact, checksums, health/observability, provenance, and rollback. Distribution remains blocked.

## aevespers2/ALISTAIRE-

- **Objective / outcome / MVP / priority:** resolve duplicate Alistaire repository identity and produce one evidence-bounded QSO composition charter; P0 is a canonical-repository decision and documentation-only contract/lifecycle/freeze/security/evaluation charter.
- **Handoff / acceptance / non-goals:** Architect designates the canonical repository and migration/archive role; require explicit subsystem contracts, deterministic evaluation, bounded learning, stop controls, and truthful maturity labels. No AGI, consciousness, autonomy, or production-readiness claims.
- **Release / artifacts / deploy / recovery:** no version; require dual-repository inventory, migration/dependency map, diagrams, evaluation fixtures, privacy/security model, changelog, approval, provenance, and rollback. Preserve both histories and prevent duplicate package/release identity.

## aevespers2/Alistaire-agi

- **Objective / outcome / MVP / priority:** resolve duplication with `ALISTAIRE-` and establish one authoritative product location; broad documentation is not implementation evidence.
- **Handoff / acceptance / non-goals:** Architect classifies substantive versus placeholder content and preserves history; require one unambiguous package/release identity and bounded first Builder task. No runtime, AGI, autonomous tools, persistence, or speculative capability filling.
- **Release / artifacts / deploy / recovery:** no release candidate; require inventory, migration record, charter, dependency map, license/security/privacy decisions, evidence classification, changelog, health plan, provenance, and rollback. No package, tests, CI, or deployment evidence exists.

## aevespers2/Bridge

- **Objective / outcome / MVP / priority:** reproduce the Bridge evidence baseline and verify one deterministic request-to-evidence path; P0 repository/evidence health precedes versioned request validation, bounded processing, idempotent ledger, evidence report, publication provenance, and rollback.
- **Handoff / acceptance / non-goals:** Architect owns baseline and integration acceptance; require positive/negative/timeout/retry/idempotency/ordering fixtures, visible failures, source hashes, and reproducible publication. Issues #4–#9 and #14–#21 remain deferred; no broad acquisition, continuous monitoring, automated conclusions, case-management UI, or optical communications in the first release.
- **Release / artifacts / deploy / recovery:** first eligible `0.1.0-alpha.1` remains blocked. Planning files define exact-head tests, security, provenance, artifacts, health, observability, rollback, and post-validation, but implementation evidence is absent. Restore the last verified evidence snapshot and preserve rejected-candidate evidence after rollback.

## aevespers2/datarepo-temporal-invariants

- **Objective / outcome / MVP / priority:** contain and explain tracked `.forensics/last_run_epoch.txt` drift before fork/overlay work resumes; P0 is evidence capture, writer/root-cause identification, out-of-tree mutable state, atomic locking, worktree isolation, and independent validation.
- **Handoff / acceptance / non-goals:** Architect/Inspector closes the incident before Builder repair; test competing benign/adversarial hypotheses and verify no unexplained refs, hooks, tokens, or schedulers. Do not assume malicious intent or normalize evidence before preservation.
- **Release / artifacts / deploy / recovery:** publication is fail-closed; require marker values/hashes, logs, worktrees, hooks, refs, process/scheduler evidence, lock tests, security report, health/observability, provenance, and rollback. Disable live-worktree writers and verify no unexplained mutation.

## aevespers2/Misc

- **Objective / outcome / MVP / priority:** contain and classify the XYZ defensive firmware-assessment prototype, then migrate it to an approved owner or retire it; current work is portfolio P4 holding.
- **Handoff / acceptance / non-goals:** Architect selects a destination or retirement path; require representative/adversarial hardware evidence and limitations. No unauthorized assessment, flashing, disruptive defaults, sensitive data, certification, ATO, or automatic publication claims.
- **Release / artifacts / deploy / recovery:** version 0.3.0 remains unaccepted prototype metadata; require capability inventory, trusted baselines, hardware matrix, dry-run evidence, false-positive/negative analysis, SBOM/checksums, CI, legal/license review, health/observability, provenance, and rollback. Publication is not approved.

## aevespers2/QSO-DIGITALIS

- **Objective / outcome / MVP / priority:** approve a unique charter or retire/archive the repository; P0 is documentation-only purpose, users, contracts, trust/data/privacy/license boundaries, ecosystem role, verification, and retirement criteria.
- **Handoff / acceptance / non-goals:** Architect/user decision precedes skeleton or schema work; require a non-overlapping stable contract or explicit retirement. Do not infer identity, twin, wallet, runtime, networking, execution, or settlement capability from the name.
- **Release / artifacts / deploy / recovery:** no version; require charter, overlap analysis, verification plan, changelog, privacy/license decision, retirement record, provenance, health plan, and rollback. No implementation or deployment surface is approved.

## aevespers2/QSO-FABRIC

- **Objective / outcome / MVP / priority:** stabilize the Atlas/Nova/Orion/Lyra harness as a reproducible, bounded, read-only integration experiment; P0 acceptance of the existing runtime precedes new collectives.
- **Handoff / acceptance / non-goals:** Architect independently reproduces P0; draft Experimenters PR #2 remains separate. Require deterministic hashes, tamper detection, limits, interruption, freeze/rollback, and no network, credentials, or repository writes. No autonomous learning, payments, sentience claims, or portfolio control plane.
- **Release / artifacts / deploy / recovery:** blocked `0.1.0-alpha.1`; require versioned event/ledger/freeze/report contracts, fixture matrix, test/security/integration reports, sample ledgers, SBOM/checksums, provenance, health/observability, rollback, and post-run validation. Prior CI without retained artifacts does not authorize release.

## aevespers2/qso-field.github.io

- **Objective / outcome / MVP / priority:** publish a documentation-only, evidence-classified QSO ecosystem portal; P0 links, capability states, contradiction audit, responsibility map, notices, and reproducible accessible site.
- **Handoff / acceptance / non-goals:** Architect reviews PR #19 as one bounded slice; require link, claim, contradiction, accessibility, security, privacy, licensing, provenance, and upstream-contract evidence. No runtime, credentials, agents, financial product, or unsupported capability claims.
- **Release / artifacts / deploy / recovery:** blocked `0.1.0-docs.1`; PR #19's link check passed with retained evidence, but publication remains blocked. Require static bundle, reports/checksums, Pages health checks, observability, and rollback to the previous verified site if navigation or evidence labels regress.

## aevespers2/QSO-GENOMES

- **Objective / outcome / MVP / priority:** reconcile, scope-contain, freeze, and independently accept one Atlas/Nova/Orion/Lyra compatibility-set head; this remains the highest portfolio unblocker.
- **Handoff / acceptance / non-goals:** Architect controls provenance-preserving reconciliation and merge order; PR #2 is the sole compatibility path, while PR #3 and PR #4 are excluded. Require mergeable immutable head, exact-head suite, resolved P1/P2 findings, explicit digest scopes, immutable/Aequitas validation, negative fixtures, and downstream acceptance. No executable behavior, credentials, mutation, payments, or governance automation in alpha.
- **Release / artifacts / deploy / recovery:** blocked `0.1.0-alpha.1`; require schemas/genomes/protocol/migration/Aequitas, compatibility manifest, fixtures, reconciliation records, review map, CI/clean-checkout/downstream reports, checksums, provenance, health validation, and rollback. Preserve all reviewed heads and reject digest/identity/immutability drift.

## aevespers2/QSO-PAYMENTS

- **Objective / outcome / MVP / priority:** publish a documentation-only payment-intent and authorization boundary before simulation; distinguish intent, authorization, allocation, receipts, disputes, escrow, adapters, custody, and settlement.
- **Handoff / acceptance / non-goals:** Architect/user approves terminology, jurisdiction assumptions, environment labels, privacy/license, and prohibited capabilities. No credentials, custody, signing, transfers, returns, certification, or executable payment path.
- **Release / artifacts / deploy / recovery:** no executable version; require charter, static artifact, link/HTML/accessibility/security/privacy reports, claim review, checksums, provenance, health checks, and rollback. Restore prior verified documentation and verify no adapter or credential path became active.

## aevespers2/QSO-SEEKER

- **Objective / outcome / MVP / priority:** prove a read-only fail-closed path from untrusted public content to inert canonical and attribution records; P0 security/CLI baseline precedes retrieval expansion.
- **Handoff / acceptance / non-goals:** Architect dispositions PR #2; PR #4 action-orchestration remains separate. Require clean immutable-head replay, deterministic outputs/hashes, credential-free/network-free sanitizer and digest handoff. No crawling, private-source access, executable processing, or runtime authority.
- **Release / artifacts / deploy / recovery:** blocked `0.1.0-alpha.1`; require schemas/fixtures, CLI/PDF samples, split-job workflows, security/hidden-control reports, exact-head logs, retained artifacts, SBOM/checksums, provenance, health/observability, and rollback. Restore accepted P0 state and verify no network, credential, or content-execution authority.

## aevespers2/QSO-STUDIO

- **Objective / outcome / MVP / priority:** approve a product/UX charter and accurate documentation before building a human-review interface; P0 users, workflows, platform, data, privacy, license, and authority precede UI implementation.
- **Handoff / acceptance / non-goals:** Architect/user approves the charter; draft PR #1 Experimenters scaffold remains roadmap-only. Require accurate paths/publication claims, reproducible accessible docs, and a read-only fixture-backed workflow. No runtime execution, credentials, unrestricted writes, autonomous approval, or payment control.
- **Release / artifacts / deploy / recovery:** blocked `0.0.1-charter.1`; require charter, diagrams, documentation artifact, integrity/link/accessibility/security reports, fixtures/contracts, checksums, provenance, health checks, and rollback. No site/application deployment is authorized.

## aevespers2/QuantumStateObjects

- **Objective / outcome / MVP / priority:** accept one runnable package/configuration candidate, validate local runtime primitives, validate upstream contracts, then run four bounded QSOs. P0-A is final-head acceptance of canonical PR #6; P0-B is local instance/message/ledger/limits/freeze/rollback evidence.
- **Handoff / acceptance / non-goals:** PR #6 head `6e382853e6746f8eb18e97c64481dccfe6684652` is the sole selected path. Run `29610600428` checked out and asserted the exact head; Python 3.11/3.13 passed 11 tests, CLI/configuration smoke, wheel builds, and retained-artifact upload. Three unresolved P2 findings require schema support for `genome.sha256`, enforcement of the declared QSO-GENOMES repository/path contract, and canonical case-sensitive Atlas/Nova/Orion/Lyra names. Require final-head and merged-head checks, deterministic hashes, message/ledger/limits/freeze/rollback evidence, and no external code execution, network, credentials, or repository writes. No verified four-QSO claim before upstream acceptance.
- **Release / artifacts / deploy / recovery:** metadata `0.1.0`, first eligible `0.1.0-alpha.1`; candidate artifact digests and wheel hashes are recorded, but source/sdist, merged-head tests, full runtime/freeze/rollback/security reports, event/attribution samples, SBOM, provenance, privacy/license approval, and rollback remain required. `deploy.md` defines a disposable credential-free first target, canonical configuration health checks, observability, rollback, and post-validation; deployment remains prohibited.

## Portfolio release and deployment gates

Any future deployment must begin with bounded non-mutating/manual validation, record exact source identity and permissions, retain health and provenance artifacts, exercise rollback, and perform post-deployment smoke, integrity, observability, revocation, cleanup, and disablement checks. A successful verification run does not authorize publication, persistent hosting, scheduling, external integration, credentials, or production use.

## Review log

- **2026-07-17:** established one evidence-only lifecycle view for all 16 repositories without approving release or deployment.
- **2026-07-17:** recorded qso-field PR #19 as a successful documentation-link candidate while retaining all remaining publication gates.
- **2026-07-17:** kept QSO-SEEKER PR #4, QSO-FABRIC PR #2, QSO-GENOMES PR #4, QSO-STUDIO PR #1, and QuantumStateObjects PR #3 as deferred candidates that cannot supersede active P0 objectives.
- **2026-07-17:** corrected the issue review to reflect Bridge's open expansion backlog and completed Bridge's lifecycle planning structure; release and deployment remain blocked.
- **2026-07-17:** advanced QuantumStateObjects from a missing CLI to a preferred matrix-tested PR #4 candidate, then corrected its exact-head claim after workflow logs proved the synthetic merge ref was tested.
- **2026-07-17:** advanced QuantumStateObjects again to sole canonical PR #6. Exact-head run `29610600428` passed 11 tests and retained Python 3.11/3.13 artifacts, but three configuration-contract review findings block acceptance. Updated repository-local task, punch, release, changelog, and deployment plans; no release or deployment was authorized.