# Portfolio Lifecycle Plan

> **Evidence-only coordination record.** This plan does not approve a merge, release, deployment, credential, schedule, network path, external write, or runtime claim. Repository-local lifecycle documents remain authoritative for implementation details; this central record carries current cross-repository status when a repository is intentionally left unchanged during exact-head review.

Reviewed: **2026-07-17 23:02 PDT**  
Scope: **16 owned repositories**  
Portfolio decision: **No repository is release-ready or deployment-ready.**

## Current evidence and priority

QuantumStateObjects PR #7 advanced without force-rewriting reviewed history to immutable head `47f018602aa71643169d8b7eabe5139f2507d474`. It remains open, unmerged, and mergeable against `main` head `3af0b2d57367631beb4d0eb5bdcd6a67aafa468b`. Exact-head CI run `29632052707` passed Python 3.11/3.13 checkout assertions, installation, compilation, 78 tests with zero failures/errors/skips, installed CLI smoke, wheel construction, checksums, and retained artifacts. The wheel SHA-256 is `8e14acfdc2adea0a4a87462d6118bc6214860cae47395a006ecfdfe8857b8c37` on both interpreters; artifact digests are `0b6b90314e68fcaaf63eafcb4e571bbf19e4899176a16fb1f7eae0864a7f1f15` and `d2b2fbeac69f968b37ab9c10624a397513cc792906d9d177c0867942d7b13500`. The prior 24 P2 review threads were resolved only after that run, but independent review then added three unresolved P2 blockers: falsy non-list attribution `artifacts` values are silently normalized and discarded; mixed-type event keys can crash ledger verification instead of returning fail-closed findings; and non-object genome `resources` can raise a raw attribute error rather than a deterministic runtime invariant. The successful run remains valid evidence for its submitted head but is not acceptance-complete. QuantumStateObjects `taskchain.md`, `punchlist.md`, `release.md`, `deploy.md`, and `changelog.md` on `main` remain deliberately untouched while PR #7 is under exact-head review.

QSO-GENOMES PR #2 remains the sole canonical compatibility-set candidate and remains non-mergeable without final exact-head acceptance evidence. QSO-SEEKER PR #7 was closed after discovery that its branch originated from an empty Git tree; replacement draft PR #8 is isolated expansion work and its initial Security Envelope run `29631542021` failed during editable installation, now tracked by Issue #9. QSO-FABRIC draft PR #4 advanced to head `6505ca55c116849c53daf8c652d5d4e01870c6ff`, but Issue #12 identifies non-atomic graph activation as a blocker requiring a single verified transaction visibility switch and crash/tamper/rollback evidence. These Seeker and Fabric candidates remain deferred expansion evidence and do not alter the canonical dependency order; no accepted upstream contracts, canonical per-object ledgers, durable promotion, or authorized four-QSO run are established.

1. **QSO-GENOMES:** reconcile and freeze canonical PR #2; exclude governance PR #3 and Experimenters PR #4.
2. **QuantumStateObjects:** remediate the three current PR #7 findings, rerun exact-head evidence, then require explicit merge authorization and merged-head acceptance.
3. **QSO-SEEKER:** restore PR #2 mergeability and obtain P0 disposition; keep PRs #4–#6 and #8 outside the hostile-input MVP, with malformed PR #7 closed.
4. **QSO-FABRIC:** reproduce P0 only after accepted upstream versions and hashes; PRs #2–#4 and Issues #5–#12 remain deferred.
5. **qso-field.github.io:** complete evidence-classified documentation gates.
6. **Bridge:** reproduce the evidence baseline before expansion work.
7. **QSO-DIGITALIS:** review the documentation charter only; no materialization or runtime activation.
8. All other repositories remain at their documented charter, provenance, incident, ownership, or baseline holds.

## Shared lifecycle controls

Every repository must retain a product objective, user outcome, bounded MVP, priority, architecture handoff, repository-specific acceptance criteria, non-goals, release gates, versioning and changelog policy, artifact requirements, deployment environment and permissions, health checks, observability, rollback triggers/procedure, and post-deployment validation. Readiness requires tests, security, documentation, provenance, permissions, environment validation, rollback evidence, privacy/licensing where applicable, and all repository-specific criteria at one immutable source head. Structural plans, scaffolds, merge-ref CI, synthetic tests, generic harnesses, network rehearsals, or retained candidate artifacts do not authorize release or deployment.

## aevespers2/0

- **Objective / outcome / MVP / priority:** establish a reproducible Autonomous vNext health baseline and one policy-gated, reversible local mission; repository inventory and health precede scientific, VTX, or portfolio-control expansion.
- **Handoff / acceptance / non-goals:** Architect disposes PR #7 after clean setup, full tests, denial/stop/federation/provenance/rollback evidence. PR #8 remains an unaccepted control-plane proposal; no owner-wide token, scheduled writer, automatic closure, or autonomous approval.
- **Release / version / changelog / artifacts:** blocked `0.0.1-baseline`; require repository map, exact-head test/security/static reports, mission evidence, source archive, checksums, provenance, review dispositions, and a changelog tied to accepted behavior.
- **Deploy / health / observability / rollback / post-validation:** no target approved. Health requires bounded local operation and visible denials; retain structured audit evidence, restore candidate-touched files on failure, rerun non-mutating validation, and verify no external mutation.

## aevespers2/1

- **Objective / outcome / MVP / priority:** decide the Partitioned Versioning Trust Core charter and the Repository `0` → `1` route; P0 is local, deny-by-default transition, receipt, checkpoint, recovery, and advisory path audit.
- **Handoff / acceptance / non-goals:** Architect decides whether `0:proposal` is authoritative, staging, or removed. Require deterministic positive/negative, replay/expiry, receipt chaining, checkpoint recovery, threat-model, and capability-lifecycle evidence; no remote service, production secrets, or autonomous approval.
- **Release / version / changelog / artifacts:** no eligible version; require schemas, fixtures, token-preflight tests, threat model, clean-checkout logs, key/capability lifecycle, provenance, checksums, and change history.
- **Deploy / health / observability / rollback / post-validation:** local-only hold. Observe transition/denial/receipt integrity without secrets; revoke capabilities and restore the last trusted checkpoint on failure; verify no credential or remote writer altered canonical history.

## aevespers2/AionUi

- **Objective / outcome / MVP / priority:** classify the repository as mirror, maintained fork, or derivative and reproduce inherited AionUi 1.7.0 before feature work.
- **Handoff / acceptance / non-goals:** Architect/user approve product and distribution identity; require divergence, provenance, naming/notices, supported-platform, `npm ci`, lint/format/test, platform smoke, accessibility, and credential/storage/network review. No rebranding or unsigned public binary.
- **Release / version / changelog / artifacts:** preserve inherited 1.7.0; local changes require a differentiated prerelease and changelog. Require license/notices, dependency inventory/SBOM, build/test logs, platform artifacts, checksums, and provenance.
- **Deploy / health / observability / rollback / post-validation:** distribution blocked. Health checks cover startup/build/platform behavior and accessibility; retain non-secret diagnostics; roll back to the reproduced upstream baseline and revalidate packaging and notices.

## aevespers2/ALISTAIRE-

- **Objective / outcome / MVP / priority:** resolve duplicate Alistaire repository identity and produce one evidence-bounded composition charter.
- **Handoff / acceptance / non-goals:** Architect designates the canonical repository and migration/archive role; require explicit subsystem contracts, deterministic evaluation, bounded learning, stop controls, and truthful maturity labels. No AGI, consciousness, autonomy, or production-readiness claim.
- **Release / version / changelog / artifacts:** no version; require dual-repository inventory, migration/dependency map, diagrams, evaluation fixtures, privacy/security model, changelog, approval, and provenance.
- **Deploy / health / observability / rollback / post-validation:** no deployment. Prevent duplicate package/release identity; observe migration decisions and retained history; restore both repositories to pre-migration state if identity or provenance is lost.

## aevespers2/Alistaire-agi

- **Objective / outcome / MVP / priority:** resolve duplication with `ALISTAIRE-` and select one authoritative product location; current broad documentation is not implementation evidence.
- **Handoff / acceptance / non-goals:** Architect classifies substantive versus placeholder content and assigns one bounded first Builder task. No runtime, AGI, autonomous tools, persistence, or speculative capability filling.
- **Release / version / changelog / artifacts:** no candidate; require inventory, migration record, charter, dependency map, license/security/privacy decisions, evidence classification, changelog, and provenance.
- **Deploy / health / observability / rollback / post-validation:** no package, CI, or target exists. Health is repository identity and content integrity only; preserve history and undo any migration that creates ambiguity or data loss.

## aevespers2/Bridge

- **Objective / outcome / MVP / priority:** reproduce the Bridge evidence baseline and verify one deterministic request-to-evidence path before expansion.
- **Handoff / acceptance / non-goals:** Architect owns baseline and integration acceptance; require positive/negative/timeout/retry/idempotency/ordering fixtures, visible failures, source hashes, and reproducible publication. Issues #4–#9 and #14–#21 remain deferred; no broad acquisition, continuous monitoring, automated conclusions, case-management UI, or optical communications in MVP.
- **Release / version / changelog / artifacts:** blocked `0.1.0-alpha.1`; require exact-head tests, contracts, security, provenance, source/checksum/report artifacts, health evidence, and a changelog tied to accepted interfaces.
- **Deploy / health / observability / rollback / post-validation:** no target approved. Health requires deterministic ingestion/evidence and explicit PASS/FAIL/UNKNOWN; observe retries/order/provenance; restore the last verified snapshot and preserve rejected-candidate evidence.

## aevespers2/datarepo-temporal-invariants

- **Objective / outcome / MVP / priority:** contain and explain tracked `.forensics/last_run_epoch.txt` drift before fork/overlay work resumes.
- **Handoff / acceptance / non-goals:** Architect/Inspector closes the incident before repair; capture writer/root cause, move mutable state out of tree, prove atomic locking and worktree isolation, and test benign/adversarial hypotheses. Do not assume malicious intent or normalize evidence prematurely.
- **Release / version / changelog / artifacts:** publication fail-closed; require marker values/hashes, logs, worktrees, hooks, refs, processes/schedulers, lock tests, security report, provenance, and incident changelog.
- **Deploy / health / observability / rollback / post-validation:** disable live-worktree writers on regression; observe marker/ref/process changes; restore the last clean state without deleting evidence; verify no unexplained mutation remains.

## aevespers2/Misc

- **Objective / outcome / MVP / priority:** contain and classify the XYZ defensive firmware-assessment prototype, then migrate it to an approved owner or retire it; portfolio P4.
- **Handoff / acceptance / non-goals:** Architect chooses destination or retirement; require representative/adversarial hardware evidence and limitations. No unauthorized assessment, flashing, disruptive defaults, sensitive data, certification, ATO, or automatic publication.
- **Release / version / changelog / artifacts:** metadata `0.3.0` remains unaccepted; require capability inventory, trusted baselines, hardware matrix, dry-run evidence, false-positive/negative analysis, SBOM/checksums, CI, legal/license review, changelog, and provenance.
- **Deploy / health / observability / rollback / post-validation:** no publication or field deployment. Observe hardware/firmware identity and safe dry-run results; restore known firmware/configuration and verify device integrity after rollback.

## aevespers2/QSO-DIGITALIS

- **Objective / outcome / MVP / priority:** review draft PR #2 as a bounded Digital Consciousness Field documentation charter or retire/archive the repository; P0 remains documentation-only.
- **Handoff / acceptance / non-goals:** Architect/user approve non-overlapping contracts, capability separation, trust/data/privacy/license/retention boundaries, verification, migration, rollback, and retirement. No literal-consciousness claim, executable/raw transport, credentials, unrestricted memory, implicit trust, autonomous approval, or settlement authority.
- **Release / version / changelog / artifacts:** possible `0.0.1-charter.1` remains blocked; require approved charter, overlap map, documentation artifacts, security/privacy/license review, exact-head evidence, checksums, changelog, provenance, and downstream acceptance.
- **Deploy / health / observability / rollback / post-validation:** no materialization or deployment. Health is documentation consistency and link/integrity status; roll back to the prior charter state if claims, boundaries, or provenance regress.

## aevespers2/QSO-FABRIC

- **Objective / outcome / MVP / priority:** stabilize a reproducible, bounded, read-only, network-disabled Atlas/Nova/Orion/Lyra integration experiment after accepted upstream contract consumption.
- **Handoff / acceptance / non-goals:** Architect independently reproduces P0. PRs #2–#4 and Issues #5–#12 remain deferred expansion; Issue #12 confirms PR #4 graph persistence is not yet atomically visible or rollback-qualified. Fixture-backed persistence, network probes, curricula, skills, scaffold manifests, and sandbox receipts do not prove canonical execution. No autonomous learning, payments, sentience claim, production credential, or portfolio control plane.
- **Release / version / changelog / artifacts:** blocked `0.1.0-alpha.1`; require versioned event/ledger/freeze/report/memory contracts, accepted upstream versions/hashes, fixture/adversarial matrices, exact- and merged-head reports, per-object ledgers, freeze/rollback samples, atomic transaction activation evidence, SBOM/checksums, provenance, and changelog.
- **Deploy / health / observability / rollback / post-validation:** no durable run or promotion. Health requires deterministic per-object evidence, complete verified transaction visibility, and bounded resources; observe contract/hash identities and promotion decisions; restore the accepted snapshot and prove no unapproved persistence or network activity.

## aevespers2/qso-field.github.io

- **Objective / outcome / MVP / priority:** publish a documentation-only, evidence-classified QSO ecosystem portal.
- **Handoff / acceptance / non-goals:** Architect reviews PR #19; require link, claim, contradiction, accessibility, security, privacy, licensing, provenance, and upstream-contract evidence. No runtime, credentials, agents, financial product, or unsupported capability claim.
- **Release / version / changelog / artifacts:** blocked `0.1.0-docs.1`; require static bundle, link/accessibility/security/privacy/license reports, checksums, provenance, and changelog.
- **Deploy / health / observability / rollback / post-validation:** Pages publication remains blocked. Health checks cover navigation, evidence labels, accessibility, and content integrity; observe build/link failures; roll back to the previous verified site and repeat smoke checks.

## aevespers2/QSO-GENOMES

- **Objective / outcome / MVP / priority:** reconcile, scope-contain, freeze, and independently accept one Atlas/Nova/Orion/Lyra compatibility-set head; highest portfolio unblocker.
- **Handoff / acceptance / non-goals:** Architect controls provenance-preserving reconciliation and merge order; PR #2 is canonical, PRs #3–#4 excluded. Require a mergeable immutable head, exact-head suite, resolved findings, explicit digest scopes, immutable/Aequitas validation, negative fixtures, and downstream acceptance. No executable behavior, credentials, mutation, payments, or governance automation.
- **Release / version / changelog / artifacts:** blocked `0.1.0-alpha.1`; require schemas/genomes/protocol/migration/Aequitas, compatibility manifest, fixtures, reconciliation records, review map, CI/clean-checkout/downstream reports, checksums, changelog, and provenance.
- **Deploy / health / observability / rollback / post-validation:** no runtime deployment. Health validates schema, identity, immutability, and exact hashes; observe drift and consumer compatibility; preserve all reviewed heads and roll back any digest/identity/immutability regression.

## aevespers2/QSO-PAYMENTS

- **Objective / outcome / MVP / priority:** publish a documentation-only payment-intent and authorization boundary before simulation.
- **Handoff / acceptance / non-goals:** Architect/user approve terminology, jurisdiction assumptions, environment labels, privacy/license, and prohibited capabilities. No credentials, custody, signing, transfers, returns, certification, or executable payment path.
- **Release / version / changelog / artifacts:** no executable version; require charter, static artifact, link/HTML/accessibility/security/privacy reports, claim review, checksums, changelog, and provenance.
- **Deploy / health / observability / rollback / post-validation:** documentation only. Health checks confirm no adapter or credential path is active; observe link/claim changes; restore prior verified documentation if boundaries regress.

## aevespers2/QSO-SEEKER

- **Objective / outcome / MVP / priority:** prove a read-only, fail-closed path from untrusted public content to inert canonical and attribution records.
- **Handoff / acceptance / non-goals:** restore PR #2 mergeability and obtain Architect P0 disposition; require versioned contracts, sanitizer isolation, digest handoff, adversarial fixtures, and retained exact-head evidence. PRs #4–#6 and #8 remain outside P0; PR #7 was closed after an empty-tree branch error, while replacement draft PR #8 remains blocked by failed editable installation and missing exact-head Security Envelope evidence. No crawling, private-source access, executable processing, scheduled collection, or runtime authority.
- **Release / version / changelog / artifacts:** blocked `0.1.0-alpha.1`; require accepted schemas/fixtures, CLI/PDF samples, split-job workflows, passing security/hidden-control reports, source/license/privacy review, SBOM/checksums, changelog, provenance, and rollback bundle.
- **Deploy / health / observability / rollback / post-validation:** no live collection. Health requires fail-closed sanitizer and deterministic hash semantics; observe source/license/hash identities and rejections; disable network workflows/adapters and restore accepted P0 on regression.

## aevespers2/QSO-STUDIO

- **Objective / outcome / MVP / priority:** approve a product/UX charter and accurate documentation before building a human-review interface.
- **Handoff / acceptance / non-goals:** Architect/user approve users, workflows, platform, data, privacy, license, and authority; draft PR #1 remains roadmap-only. No runtime execution, credentials, unrestricted writes, autonomous approval, or payment control.
- **Release / version / changelog / artifacts:** blocked `0.0.1-charter.1`; require charter, diagrams, documentation artifact, integrity/link/accessibility/security reports, fixtures/contracts, checksums, changelog, and provenance.
- **Deploy / health / observability / rollback / post-validation:** no site/application target. Health is documentation and fixture-workflow integrity; observe accessibility/security failures; restore the approved charter/docs baseline and repeat validation.

## aevespers2/QuantumStateObjects

- **Objective / outcome / MVP / priority:** accept one runnable package/configuration and bounded runtime-primitives candidate, then validate accepted upstream contracts before any four-QSO experiment. PR #7 final acceptance remains P0.
- **Handoff / acceptance / non-goals:** PR #7 head `47f018602aa71643169d8b7eabe5139f2507d474` is open, unmerged, and mergeable against `main` head `3af0b2d57367631beb4d0eb5bdcd6a67aafa468b`; run `29632052707` passed 78 tests on Python 3.11/3.13 with retained head-bound artifacts. Three unresolved P2 findings now block acceptance: reject falsy non-list attribution artifact collections rather than silently dropping them; report mixed-type event keys as malformed evidence without crashing; and validate genome `resources` as an object before reading limits. No upstream integration, generated-code execution, credentials, network input, external write, or Atlas/Nova/Orion/Lyra running claim.
- **Release / version / changelog / artifacts:** blocked `0.1.0-alpha.1`; require repair and exact-head reverification of the three findings, explicit merge authorization, merged-head verification, complete negative/adversarial/runtime/security reports, event/attribution/checkpoint samples, source/sdist/wheel/SBOM/checksums/provenance, accepted QSO-GENOMES/QSO-SEEKER contracts, privacy/license approval, rollback drill, changelog, and approval.
- **Deploy / health / observability / rollback / post-validation:** no target approved. First target remains disposable, credential-free, network-disabled, synthetic, bounded, and human-controlled. Health requires exact identities, canonical state/ledgers, atomic failure, deterministic replay, bounded resources, and denied capabilities; observe lifecycle/hash/rejection evidence; preserve failed artifacts, restore the last accepted checkpoint or clean environment, verify no external mutation, and repeat smoke/integrity/cleanup validation.

## Review log

- **2026-07-17:** maintained one evidence-only lifecycle plan for all 16 repositories; no repository was marked release-ready or deployment-ready.
- **2026-07-17:** recorded QuantumStateObjects PR #7 immutable head `47f018602aa71643169d8b7eabe5139f2507d474`, exact-head run `29632052707`, 78 passing tests, wheel/checksum/head-SHA artifacts, and retained artifact digests.
- **2026-07-17:** retained the QuantumStateObjects merge/release/deployment block after three new P2 findings were filed following the successful run; left all default-branch lifecycle files unchanged to avoid exact-head review drift.
- **2026-07-17:** recorded QSO-SEEKER PR #7 closure, draft PR #8 installation failure/Issue #9, and QSO-FABRIC PR #4 atomicity blocker/Issue #12 as deferred expansion evidence without changing canonical portfolio priority.
- **2026-07-17:** confirmed no completed lifecycle transition, release, deployment, rollback, or approval decision occurred in the remaining repositories.