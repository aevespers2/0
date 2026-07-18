# Portfolio Lifecycle Plan

> **Evidence-only coordination record.** This file does not approve a merge, release, deployment, token, schedule, issue writer, network path, or cross-repository mutation. Repository-local `taskchain.md`, `punchlist.md`, `release.md`, and `deploy.md` remain authoritative for implementation and acceptance details.

Reviewed: **2026-07-17 17:00 PDT**  
Scope: **16 owned repositories**  
Portfolio decision: **No repository is release-ready or deployment-ready.**  
Current issue/change evidence: no owned-repository issue was newly updated during this review window. Bridge Issues #4–#9 and #14–#21 remain deferred. QuantumStateObjects PR #7 is open, unmerged, mergeable, and exact-head verified at `3f8abdb2a10b6bd35f8dabab9747ccccce0afccc`; run `29620384422` passed 26 tests on Python 3.11/3.13 and retained head-bound artifacts. Four runtime findings were resolved, but five P2 findings now block acceptance: strict UTF-8 decoding, schema-required manifest blocks, rejection of Boolean schema versions, canonical instance IDs, and record-content hash verification before ingest. QSO-GENOMES PR #2 remains the highest cross-repository unblocker and is still non-mergeable and unaccepted. QSO-SEEKER PR #2 is also currently non-mergeable; new draft PR #6 exercised a live network checkpoint and retained evidence, but its Security Envelope failed before adversarial and hidden-control tests. New QSO-FABRIC draft PR #3 retained a successful Crossref network-probe artifact, but it remains an expansion candidate outside the network-disabled P0 acceptance path. Draft QSO-SEEKER PR #5, QSO-DIGITALIS PR #2, and Repository `0` PR #8 remain separate expansion/governance proposals and do not change the active MVP priority.

## Portfolio priority and architecture handoff

1. **QSO-GENOMES:** reconcile and freeze canonical PR #2 with exact-head, dependency, provenance, immutable-contract, Aequitas, manifest, negative-fixture, and downstream-consumer evidence; keep governance PR #3 and Experimenters PR #4 separate and excluded.
2. **QuantumStateObjects:** repair the five current PR #7 findings, rerun exact-head CI with retained artifacts, resolve review threads, and complete merged-head acceptance. The 26-test runtime-primitives slice is in `REVIEW`, not release-ready capability.
3. **QSO-SEEKER:** restore PR #2 mergeability and obtain Architect P0 disposition, then complete versioned canonical-record/attribution, independent sanitizer isolation, digest handoff, and adversarial fixtures. Keep action-orchestration PR #4, collection/private-overlay/field-publication PR #5, and live-network checkpoint PR #6 outside the hostile-input MVP; PR #6 cannot advance while its Security Envelope fails.
4. **QSO-FABRIC:** reproduce and accept the existing Atlas/Nova/Orion/Lyra network-disabled harness before considering Experimenters runtime PR #2 or gromerical/Crossref network-probe PR #3.
5. **qso-field.github.io:** review PR #19's link baseline, then continue claim, accessibility, privacy/licensing, reproducibility, and upstream-contract gates.
6. **Bridge:** lifecycle planning is structurally complete; implementation remains blocked on current-head reproduction.
7. **QSO-DIGITALIS:** review draft PR #2 only as a documentation/architecture charter candidate; no scaffold materialization, field runtime, transport, storage, or downstream contract activation is authorized.
8. All other repositories remain at their documented charter, provenance, incident, ownership, or evidence-baseline holds.

## Shared lifecycle controls

Every repository must preserve its product objective, user outcome, MVP boundary, priority, architecture handoff, acceptance criteria, non-goals, versioning/changelog intent, required artifacts, deployment environment and permissions, health checks, observability, rollback triggers/procedure, and post-deployment validation. No repository may be marked ready until repository-specific tests, security, documentation, provenance, permissions, environment, rollback, privacy/license where applicable, and acceptance criteria pass at one immutable source head. Structural planning, scaffold materialization, local replay, merge-ref CI, exact-head focused tests, live-network rehearsals, or retained candidate artifacts do not authorize release when independent review, merged-head verification, full behavior, upstream contracts, legal/privacy boundaries, or rollback remain incomplete.

## aevespers2/0

- **Objective / outcome / MVP / priority:** establish a reproducible Autonomous vNext health baseline and prove one policy-gated, reversible local mission; repository inventory and health precede mission expansion, scientific engines, VTX/private publication, or portfolio governance.
- **Handoff / acceptance / non-goals:** Architect dispositions PR #7 evidence; clean setup, full tests, policy denial, stop conditions, federation rejection, provenance, and rollback must pass. Draft PR #8 is a non-mergeable portfolio control-plane proposal outside P0; no six-hour schedule, owner-wide token, central issue writer, or automated closure is authorized.
- **Release / artifacts / deploy / recovery:** blocked `0.0.1-baseline`; require repository map, exact-head logs, security/static/test reports, mission evidence, source archive, checksums, provenance, review dispositions, bounded health/observability, and rollback. Restore candidate-touched files and rerun non-mutating validation after rollback.

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

- **Objective / outcome / MVP / priority:** review draft PR #2 as a bounded Digital Consciousness Field charter candidate or retire/archive the repository; P0 remains documentation-only.
- **Handoff / acceptance / non-goals:** Architect/user approve a non-overlapping evidence-envelope contract, capability separation, trust/data/privacy/license/retention boundaries, verification, migration, rollback, and retirement criteria. PR #2's roadmap and materializer are scaffold proposals, not implementation. No literal-consciousness claim, raw/executable transport, credentials, unrestricted shared memory, implicit trust, autonomous approval, or settlement authority.
- **Release / artifacts / deploy / recovery:** possible `0.0.1-charter.1` remains blocked; require approved charter, overlap map, schemas/policies/fixtures only after approval, security/privacy/license review, exact-head evidence, checksums, provenance, downstream acceptance, health/observability, and rollback. No materialization or deployment is authorized.

## aevespers2/QSO-FABRIC

- **Objective / outcome / MVP / priority:** stabilize the Atlas/Nova/Orion/Lyra harness as a reproducible, bounded, read-only, network-disabled integration experiment; P0 acceptance of the existing runtime precedes new collectives or external retrieval.
- **Handoff / acceptance / non-goals:** Architect independently reproduces P0; draft Experimenters PR #2 and draft gromerical/Crossref network-probe PR #3 remain separate expansion candidates. PR #3 exact head `a20b72ca828b504939c85ec76f2a893ca1a12c05` passed network-probe run `29621710598` and retained artifact digest `30c93d83513e681b2e8a8ecdd5d1a434a61edee34b7e84b7dcb79a5af4010d`, but that evidence does not satisfy the network-disabled P0 boundary. P0 still requires deterministic hashes, tamper detection, limits, interruption, freeze/rollback, and no network, credentials, or repository writes. No autonomous learning, payments, sentience claims, or portfolio control plane.
- **Release / artifacts / deploy / recovery:** blocked `0.1.0-alpha.1`; require versioned event/ledger/freeze/report contracts, fixture matrix, test/security/integration reports, sample ledgers, SBOM/checksums, provenance, health/observability, rollback, and post-run validation. The PR #3 live-network artifact is review evidence only and cannot authorize release, deployment, or a claim that any QSO executed.

## aevespers2/qso-field.github.io

- **Objective / outcome / MVP / priority:** publish a documentation-only, evidence-classified QSO ecosystem portal; P0 links, capability states, contradiction audit, responsibility map, notices, and reproducible accessible site.
- **Handoff / acceptance / non-goals:** Architect reviews PR #19 as one bounded slice; require link, claim, contradiction, accessibility, security, privacy, licensing, provenance, and upstream-contract evidence. No runtime, credentials, agents, financial product, or unsupported capability claims.
- **Release / artifacts / deploy / recovery:** blocked `0.1.0-docs.1`; PR #19's link check passed with retained evidence, but publication remains blocked. Require static bundle, reports/checksums, Pages health checks, observability, and rollback to the previous verified site if navigation or evidence labels regress.

## aevespers2/QSO-GENOMES

- **Objective / outcome / MVP / priority:** reconcile, scope-contain, freeze, and independently accept one Atlas/Nova/Orion/Lyra compatibility-set head; this remains the highest portfolio unblocker.
- **Handoff / acceptance / non-goals:** Architect controls provenance-preserving reconciliation and merge order; PR #2 is the sole compatibility path, while PR #3 and PR #4 are excluded. Current PR #2 head `688216ea60b9b2dc5bf3598048acf9ad2cf96033` remains non-mergeable. Require mergeable immutable head, exact-head suite, resolved findings, explicit digest scopes, immutable/Aequitas validation, negative fixtures, and downstream acceptance. No executable behavior, credentials, mutation, payments, or governance automation in alpha.
- **Release / artifacts / deploy / recovery:** blocked `0.1.0-alpha.1`; require schemas/genomes/protocol/migration/Aequitas, compatibility manifest, fixtures, reconciliation records, review map, CI/clean-checkout/downstream reports, checksums, provenance, health validation, and rollback. Preserve all reviewed heads and reject digest/identity/immutability drift.

## aevespers2/QSO-PAYMENTS

- **Objective / outcome / MVP / priority:** publish a documentation-only payment-intent and authorization boundary before simulation; distinguish intent, authorization, allocation, receipts, disputes, escrow, adapters, custody, and settlement.
- **Handoff / acceptance / non-goals:** Architect/user approves terminology, jurisdiction assumptions, environment labels, privacy/license, and prohibited capabilities. No credentials, custody, signing, transfers, returns, certification, or executable payment path.
- **Release / artifacts / deploy / recovery:** no executable version; require charter, static artifact, link/HTML/accessibility/security/privacy reports, claim review, checksums, provenance, health checks, and rollback. Restore prior verified documentation and verify no adapter or credential path became active.

## aevespers2/QSO-SEEKER

- **Objective / outcome / MVP / priority:** prove a read-only fail-closed path from untrusted public content to inert canonical and attribution records; PR #2 P0 and P1-P3 contracts/isolation precede retrieval expansion or live collection.
- **Handoff / acceptance / non-goals:** PR #2 head `306dfa4104c12594b23dda8111e1c80edb0be397` is open but currently non-mergeable; exact-head run `29580240905` passed, but retained artifacts and Architect disposition remain absent. Draft PR #5 is a later public-collection/private-overlay/scheduled-workflow/license/field-publication proposal and remains excluded. Draft PR #6 head `14e39d81b3f3559bb9dba5b2a545e4a6cf900d49` completed live-checkpoint run `29621521854` and retained artifact digest `e47870406164fac6b37c402fb155da988c157919cfe60ad7fc17262e2534d9c2`, but Security Envelope run `29621523420` failed at capability-envelope verification and skipped adversarial/deterministic and hidden-control checks. No crawling, private-source access, executable processing, scheduled live collection, or runtime authority is accepted for P0.
- **Release / artifacts / deploy / recovery:** blocked `0.1.0-alpha.1`; require a mergeable accepted P0 head, schemas/fixtures, CLI/PDF samples, split-job workflows, passing security/hidden-control reports, exact-head retained artifacts, source/license/privacy review, SBOM/checksums, provenance, health/observability, rollback, and post-validation. Disable live-network workflows/adapters and restore the accepted P0 state on rollback.

## aevespers2/QSO-STUDIO

- **Objective / outcome / MVP / priority:** approve a product/UX charter and accurate documentation before building a human-review interface; P0 users, workflows, platform, data, privacy, license, and authority precede UI implementation.
- **Handoff / acceptance / non-goals:** Architect/user approves the charter; draft PR #1 Experimenters scaffold remains roadmap-only. Require accurate paths/publication claims, reproducible accessible docs, and a read-only fixture-backed workflow. No runtime execution, credentials, unrestricted writes, autonomous approval, or payment control.
- **Release / artifacts / deploy / recovery:** blocked `0.0.1-charter.1`; require charter, diagrams, documentation artifact, integrity/link/accessibility/security reports, fixtures/contracts, checksums, provenance, health checks, and rollback. No site/application deployment is authorized.

## aevespers2/QuantumStateObjects

- **Objective / outcome / MVP / priority:** accept one runnable package/configuration and bounded runtime-primitives candidate, validate accepted upstream contracts, then run four bounded QSOs. P0-A is final PR #7 acceptance; P0-B is atomic local lifecycle/message/ledger/limits/freeze/rollback evidence.
- **Handoff / acceptance / non-goals:** PR #7 head `3f8abdb2a10b6bd35f8dabab9747ccccce0afccc` is open, unmerged, mergeable, and reconciled with `main` without force rewriting. Run `29620384422` passed exact-head Python 3.11/3.13 installation, 26 tests, CLI/configuration smoke, wheel construction, checksums, and retained artifacts with digests `72dde0a1337d76be9cce5be5f70ebd37966090eb4980ba542037be7bf5acbb1f` and `429a0d7d5f980780adb7fb5434f98ffe820af5246e424d9dba800cd07e142c33`. Delegated-ingest atomicity, canonical message-inclusive freeze checkpoints, rollback capacity, and strict event-ledger shape validation are repaired and their threads resolved. Five unresolved P2 findings now require strict UTF-8 decoding, complete manifest blocks, integer-not-Boolean schema versions, canonical instance IDs, and verification that each record's `content_sha256` matches its content before mutation. No Atlas/Nova/Orion/Lyra running claim without authorized append-only evidence.
- **Release / artifacts / deploy / recovery:** blocked `0.1.0-alpha.1`; require repaired exact/merged heads, complete negative/adversarial/runtime/security reports, event/attribution/checkpoint samples, source/sdist/SBOM/checksums/provenance, accepted QSO-GENOMES/QSO-SEEKER contracts, privacy/license approval, health/observability, rollback drill, and approval. The first target remains disposable, credential-free, network-disabled, synthetic, bounded, and human-controlled.

## Portfolio release and deployment gates

Any future deployment must begin with bounded non-mutating/manual validation, record exact source identity and permissions, retain health and provenance artifacts, exercise rollback, and perform post-deployment smoke, integrity, observability, revocation, cleanup, and disablement checks. A successful verification run or live-network rehearsal does not authorize publication, persistent hosting, scheduling, external integration, credentials, production use, or runtime claims for named QSOs.

## Review log

- **2026-07-17:** established one evidence-only lifecycle view for all 16 repositories without approving release or deployment.
- **2026-07-17:** completed Bridge lifecycle planning and preserved its expansion backlog outside the first release.
- **2026-07-17:** advanced QuantumStateObjects through canonical PR #7 exact-head configuration evidence.
- **2026-07-17:** reconciled QuantumStateObjects PR #7 with current `main`, recorded run `29617877793` and the 22-test runtime-primitives slice, then retained the release block after five additional runtime/evidence findings raised the unresolved total to eight.
- **2026-07-17:** classified QSO-SEEKER draft PR #5 as a later collection/private-overlay/scheduled-field proposal outside P0-P3 and QSO-DIGITALIS draft PR #2 as a charter/scaffold candidate only.
- **2026-07-17:** retained Repository `0` draft PR #8 as a non-mergeable governance/control-plane proposal outside the current Autonomous vNext baseline; no owner-wide schedule, token, or issue writer was authorized.
- **2026-07-17:** advanced QuantumStateObjects PR #7 to immutable head `3f8abdb2a10b6bd35f8dabab9747ccccce0afccc` with a successful 26-test Python 3.11/3.13 run and retained artifacts; four runtime findings were resolved, while a new record-content hash finding leaves five acceptance blockers.
- **2026-07-17:** classified QSO-SEEKER draft PR #6 and QSO-FABRIC draft PR #3 as deferred live-network expansions. The Seeker checkpoint retained evidence but failed its Security Envelope; the Fabric probe retained evidence but remains outside the network-disabled P0 boundary.