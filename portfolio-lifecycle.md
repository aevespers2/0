# Portfolio Lifecycle Plan

> **Evidence-only coordination record.** This file authorizes no merge, release, deployment, credential use, schedule, network path, generated-code execution, or external repository write. Repository-local implementation evidence remains authoritative; this central plan records lifecycle status without altering reviewed candidate heads.

Reviewed: **2026-07-18 13:01 PDT**  
Scope: **16 owned repositories**  
Portfolio decision: **No repository is release-ready or deployment-ready.**

## Meaningful change since the prior review

QuantumStateObjects PR #7 advanced by normal history to exact submitted head `291d7419bf29a3d979762c4655c05a2a672c6f82` against unchanged `main` head `3af0b2d57367631beb4d0eb5bdcd6a67aafa468b`. Exact-head CI run `29657511858` passed Python 3.11.15 and 3.13.14 with 150 tests and zero failures, errors, or skips; both jobs retained JUnit, wheel, checksum, checked-out-head, and artifact evidence. Wheel SHA-256 values are `df74cfbca5fc6c7744cbbbb897dec97f99c6f2eac19bcc97b49dc0ca38e1ad5d` and `e1c06a8d500b98c22722b463bda75e1b2d5f444365cd099e8b6fe411c1d0eb40`; artifact digests are `b0b302798c234922e9f75323d60da85dd810c957bd4af4922512f1a5aa714388` and `930f14ed7a411b5d6c36f901c0d80280db093cef2b367e406641e81289da6d49`. The interruption-reason atomicity finding is resolved, but eight P2 findings now block acceptance: repository-field shape, singleton-string message allowlists, inconsistent `max_records` default handling, structured configuration enum handling, structured message-kind handling, outgoing-recipient canonical validation before hashing, non-message receive inputs, and deterministic wrapping of configuration/genome file-read failures. PR #7 remains open, mergeable, unmerged, and not release- or deployment-ready. QuantumStateObjects `taskchain.md`, `punchlist.md`, `release.md`, `deploy.md`, and `changelog.md` on `main` were not changed.

QSO-GENOMES PR #2 remains the sole canonical compatibility-set candidate at `688216ea60b9b2dc5bf3598048acf9ad2cf96033`, is non-mergeable, and retains unresolved exact-set, immutable-protocol, identity, digest-scope, dependency, exact-head, duplicate-entry, and provenance findings. New PR #5 is stacked on that candidate head, not on `main`; it adds governance/remediation and optional reconciliation-branch workflows and therefore remains a deferred expansion candidate rather than an accepted compatibility-set dependency. QSO-SEEKER merge commit `c0867fc9062ab8539eeb783b456911123d0a91b0` remains blocked from downstream authority by five unresolved post-merge canonical-contract findings. QSO-FABRIC remains blocked on accepted upstream versions/hashes, per-object evidence, and atomic rollback-qualified persistence. No canonical four-QSO run is authorized.

## Portfolio priority and handoff order

1. **QSO-GENOMES:** reconcile, exact-head verify, and freeze canonical PR #2; keep PRs #3–#5 outside the compatibility-set acceptance path.
2. **QSO-SEEKER:** repair the five post-merge contract findings and obtain exact-head plus merged-head Security Envelope evidence before declaring v1 downstream-authoritative.
3. **QuantumStateObjects:** remediate the eight PR #7 findings through separate bounded slices, preserve every reviewed head, complete Issue #8 security adjudication, obtain explicit merge approval, then verify the merged head against accepted upstream contracts.
4. **QSO-FABRIC:** reproduce only after exact accepted upstream schema/version/hash inputs exist; PRs #2–#4 and Issues #5–#12 remain deferred.
5. **qso-field.github.io, Bridge, and QSO-DIGITALIS:** continue their documented evidence, baseline, and charter gates without displacing the canonical QSO path.
6. **All remaining repositories:** retain charter, incident, ownership, provenance, or baseline holds.

## Shared lifecycle controls

Every repository must retain a product objective, user outcome, bounded MVP, priority, architecture handoff, repository-specific acceptance criteria, explicit non-goals, release gates, versioning and changelog policy, artifact requirements, deployment environment and permissions, health checks, observability, rollback triggers/procedure, and post-deployment validation. Readiness requires tests, security, documentation, provenance, permissions, environment validation, rollback evidence, privacy/licensing where applicable, and every repository-specific criterion at one immutable source head. Scaffolds, synthetic tests, merge-ref CI, generic harnesses, network rehearsals, manifests marked candidate or pending review, and retained but unaccepted artifacts do not authorize release or deployment.

## Current default-branch evidence

| Repository | Reviewed default head | Lifecycle state |
|---|---|---|
| `aevespers2/0` | `3313ea25c271f00111b07e1fb1a804a525366c6a` before this plan update | Planning baseline in progress |
| `aevespers2/1` | `6685872ceafdefa4961e261abb45202e664e3666` | Trust-core charter hold |
| `aevespers2/AionUi` | `66b89879a0ef204a11cf0ea17fb58e5ad88dd930` | Fork-identity/reproduction hold |
| `aevespers2/datarepo-temporal-invariants` | `5d549f1082d4bc0ee59a34d09f24b4fa44e6e9bb` | Integrity incident hold |
| `aevespers2/Bridge` | `12616ad0e2f04572d8bf6af606f078489607b83f` | Baseline before expansion |
| `aevespers2/qso-field.github.io` | `67893241cc5809d4dae29502bd76809d0de37a9d` | Documentation candidate blocked |
| `aevespers2/QuantumStateObjects` | `3af0b2d57367631beb4d0eb5bdcd6a67aafa468b` | Main intentionally unchanged; PR #7 under review |
| `aevespers2/QSO-DIGITALIS` | `72debb75922484aa5b6b634de6a9723da9518f5d` | Documentation-charter hold |
| `aevespers2/QSO-GENOMES` | `f5e2bafe5696257465fdb7bda628f7d5f76c62f9` | Canonical PR #2 blocked |
| `aevespers2/QSO-SEEKER` | `c0867fc9062ab8539eeb783b456911123d0a91b0` | Merged contract acceptance-regressed |
| `aevespers2/QSO-PAYMENTS` | `8ab3b97b44fc1a38cec9aa4e8b0aac3ac6bda161` | Documentation-only hold |
| `aevespers2/QSO-FABRIC` | `380265fc50d5994d2233a521057427aca2885b95` | Upstream and atomicity blocked |
| `aevespers2/QSO-STUDIO` | `0d63d4f4988caceb5716c5214cc298d63068a2cb` | Product/UX charter hold |
| `aevespers2/ALISTAIRE-` | `7adbbf963616d09b4ebafea7c0963a2fac5688a9` | Duplicate-identity hold |
| `aevespers2/Alistaire-agi` | `504222dbecb1e1e49c01d74e536de5b6fa93c39a` | Consolidation hold |
| `aevespers2/Misc` | `59bf5c4110029f139f6f0e54e19940eadbbd0a19` | Containment/migration hold |

## aevespers2/0

- **Objective / user outcome / MVP / priority:** establish a reproducible Autonomous vNext repository-health baseline and one policy-gated, reversible local mission; P0 health precedes domain, publication, or owner-wide governance expansion.
- **Architecture / acceptance / non-goals:** Architect disposes repository PR #7 only after complete inventory, clean setup, exact-head tests, denial/stop/federation/provenance/rollback evidence, and material review closure. Draft control-plane PR #8 remains excluded; no owner-wide token, scheduled writer, silent mutation, or autonomous approval.
- **Release / version / changelog / artifacts:** blocked `0.0.1-baseline`; require repository map, exact-head static/test/security reports, mission evidence, source archive, checksums, provenance, review dispositions, and behavior-bound changelog.
- **Deploy / health / observability / rollback / validation:** no target approved; observe bounded local operation and visible denials, restore candidate-touched files on failure, rerun non-mutating validation, and confirm no external mutation.

## aevespers2/1

- **Objective / user outcome / MVP / priority:** decide the Partitioned Versioning Trust Core charter and Repository `0` to `1` route; MVP is local deny-by-default transition, receipt, checkpoint, recovery, and advisory-path audit.
- **Architecture / acceptance / non-goals:** Architect decides whether `0:proposal` is authoritative, staging, or removed; require deterministic positive/negative, replay/expiry, receipt-chain, checkpoint-recovery, threat-model, and capability-lifecycle evidence. No remote service, production secrets, or autonomous approval.
- **Release / version / changelog / artifacts:** no eligible version; require approved schemas, fixtures, preflight tests, clean-checkout logs, key/capability lifecycle, checksums, provenance, and change history.
- **Deploy / health / observability / rollback / validation:** local-only hold; observe transition/denial/receipt integrity, revoke capabilities and restore the trusted checkpoint on failure, then verify canonical history was not remotely altered.

## aevespers2/AionUi

- **Objective / user outcome / MVP / priority:** classify mirror/fork/derivative identity and reproduce inherited AionUi 1.7.0 before feature work.
- **Architecture / acceptance / non-goals:** Architect/user approve product and distribution identity; require divergence/provenance, notices, platform support, clean npm install, lint/format/test, platform smoke, accessibility, credential/storage/network review. No unapproved rebrand or unsigned public binary.
- **Release / version / changelog / artifacts:** preserve inherited 1.7.0; local changes require differentiated prerelease, changelog, license/notices, SBOM, build/test logs, platform artifacts, checksums, and provenance.
- **Deploy / health / observability / rollback / validation:** distribution blocked; health covers startup/build/platform/accessibility, diagnostics exclude secrets, and rollback returns to the reproduced upstream baseline before packaging revalidation.

## aevespers2/datarepo-temporal-invariants

- **Objective / user outcome / MVP / priority:** contain and explain tracked `.forensics/last_run_epoch.txt` drift before fork or overlay work resumes.
- **Architecture / acceptance / non-goals:** Architect/Inspector must identify the writer/root cause, move mutable state out of tree, prove atomic locking/worktree isolation, and test benign and adversarial hypotheses. Do not infer malicious intent without evidence.
- **Release / version / changelog / artifacts:** publication fail-closed; require marker values/hashes, logs, worktrees, hooks, refs, process/scheduler evidence, lock tests, security report, incident changelog, and provenance.
- **Deploy / health / observability / rollback / validation:** disable live-worktree writers on regression, observe marker/ref/process changes, restore last clean state without deleting evidence, and verify no unexplained mutation remains.

## aevespers2/Bridge

- **Objective / user outcome / MVP / priority:** reproduce one deterministic request-to-evidence baseline before broad ingestion, graph, monitoring, UI, or optical-network expansion.
- **Architecture / acceptance / non-goals:** Architect owns baseline acceptance; require positive/negative/timeout/retry/idempotency/ordering fixtures, visible failures, source hashes, and reproducible publication. Open Issues #4–#21 are backlog/deferred unless explicitly admitted to MVP.
- **Release / version / changelog / artifacts:** blocked `0.1.0-alpha.1`; require exact-head tests, contracts, security, provenance, source/checksum/report artifacts, health evidence, and accepted-interface changelog.
- **Deploy / health / observability / rollback / validation:** no target approved; health requires deterministic ingestion/evidence and explicit PASS/FAIL/UNKNOWN, observe retries/order/provenance, restore last verified snapshot, and retain rejected-candidate evidence.

## aevespers2/qso-field.github.io

- **Objective / user outcome / MVP / priority:** publish a documentation-only, evidence-classified QSO ecosystem portal.
- **Architecture / acceptance / non-goals:** Architect reviews PR #19; require link, claim, contradiction, accessibility, security, privacy, license, provenance, and accepted-upstream evidence. No runtime, credentials, agent execution, financial product, or unsupported capability claim.
- **Release / version / changelog / artifacts:** blocked `0.1.0-docs.1`; require static bundle, link/accessibility/security/privacy/license reports, checksums, provenance, and changelog.
- **Deploy / health / observability / rollback / validation:** Pages publication blocked; monitor build/link/content-integrity failures, restore previous verified site on regression, and repeat navigation/accessibility/security smoke tests.

## aevespers2/QuantumStateObjects

- **Objective / user outcome / MVP / priority:** accept one runnable package/configuration and bounded runtime-primitives candidate before any four-QSO experiment; PR #7 final acceptance is P0.
- **Architecture / acceptance / non-goals:** current PR #7 head `291d7419bf29a3d979762c4655c05a2a672c6f82` passed run `29657511858`, but eight unresolved P2 findings and Issue #8 security adjudication block merge acceptance. No generated-code execution, credentials, network input, external write, upstream candidate consumption, or Atlas/Nova/Orion/Lyra running claim.
- **Release / version / changelog / artifacts:** blocked `0.1.0-alpha.1`; require separate repair and exact-head evidence for all eight findings, immutable Issue #8 evidence/disposition, hostile-input threat model, explicit merge approval, merged-head verification, negative/runtime/security reports, event/attribution/checkpoint samples, wheel/sdist/SBOM/checksums/provenance, accepted upstream contracts, rollback drill, and changelog.
- **Deploy / health / observability / rollback / validation:** no target approved; first target must be disposable, credential-free, network-disabled, bounded, and human-controlled. Observe lifecycle/hash/rejection/quarantine evidence; preserve failures, restore accepted checkpoint or clean environment, verify no external mutation, and repeat integrity/security/cleanup validation.

## aevespers2/QSO-DIGITALIS

- **Objective / user outcome / MVP / priority:** approve draft PR #2 only as a bounded Digital Consciousness Field documentation charter or retire/archive the repository.
- **Architecture / acceptance / non-goals:** require non-overlapping contracts, capability separation, trust/data/privacy/license/retention boundaries, verification, migration, rollback, and retirement decisions. No literal-consciousness claim, executable/raw transport, credentials, unrestricted memory, implicit trust, autonomous approval, or settlement authority.
- **Release / version / changelog / artifacts:** possible `0.0.1-charter.1` remains blocked; require approved charter, overlap map, security/privacy/license review, exact-head evidence, checksums, changelog, provenance, and downstream acceptance.
- **Deploy / health / observability / rollback / validation:** no materialization or runtime deployment; health is documentation consistency and integrity, with rollback to the prior charter state if boundaries or provenance regress.

## aevespers2/QSO-GENOMES

- **Objective / user outcome / MVP / priority:** reconcile, scope-contain, freeze, and independently accept exactly one Atlas/Nova/Orion/Lyra compatibility-set head; highest portfolio unblocker.
- **Architecture / acceptance / non-goals:** PR #2 is canonical and currently non-mergeable; PRs #3–#5 are excluded/deferred. Require mergeable immutable head, exact-head suite, resolved findings, explicit digest scopes, immutable oversight validation, exact four-genome set, negative fixtures, provenance-preserving reconciliation, and downstream acceptance. No executable behavior, credentials, payments, or governance automation in the compatibility set.
- **Release / version / changelog / artifacts:** blocked `0.1.0-alpha.1`; require schemas/genomes/protocol/migration/oversight artifacts, compatibility manifest, fixtures, reconciliation records, review map, CI/clean-checkout/downstream reports, checksums, changelog, and provenance.
- **Deploy / health / observability / rollback / validation:** no runtime deployment; health validates schema, identity, immutability, and exact hashes, observes drift/consumer compatibility, preserves every reviewed head, and rolls back digest/identity/immutability regression.

## aevespers2/QSO-SEEKER

- **Objective / user outcome / MVP / priority:** prove a read-only fail-closed path from untrusted public content to inert canonical and attribution records.
- **Architecture / acceptance / non-goals:** merged v1 contract at `c0867fc9062ab8539eeb783b456911123d0a91b0` has five unresolved post-merge findings and is not downstream-authoritative. PR #2 awaits P0 disposition; PRs #4–#6 and #8 remain expansion work. No crawling, private-source access, executable processing, scheduled collection, or runtime authority.
- **Release / version / changelog / artifacts:** blocked `0.1.0-alpha.1`; require corrected schemas/fixtures, CLI/PDF samples, exact- and merged-head adversarial/deterministic/capability/hidden-control/conformance reports, complete review disposition, source/license/privacy review, SBOM/checksums, changelog, provenance, and rollback bundle.
- **Deploy / health / observability / rollback / validation:** no live collection; health requires deterministic fail-closed path/URL/version/ID/source-kind/hash semantics, observes source/license/hash identities and rejections, disables network adapters on regression, and restores last accepted P0.

## aevespers2/QSO-PAYMENTS

- **Objective / user outcome / MVP / priority:** publish a documentation-only payment-intent and authorization boundary before simulation.
- **Architecture / acceptance / non-goals:** Architect/user approve terminology, jurisdiction assumptions, environment labels, privacy/license, and prohibited capabilities. No credentials, custody, signing, transfers, returns, certification, or executable payment path.
- **Release / version / changelog / artifacts:** no executable version; require charter, static artifact, link/HTML/accessibility/security/privacy reports, claim review, checksums, changelog, and provenance.
- **Deploy / health / observability / rollback / validation:** documentation only; health confirms no adapter or credential path is active, observes link/claim changes, and restores prior verified documentation if boundaries regress.

## aevespers2/QSO-FABRIC

- **Objective / user outcome / MVP / priority:** stabilize a reproducible, bounded, read-only, network-disabled four-QSO integration experiment only after accepted upstream contract consumption.
- **Architecture / acceptance / non-goals:** PRs #2–#4 and Issues #5–#12 remain deferred; generic harnesses, hard-coded roles, network probes, curricula, scaffolds, and sandbox receipts do not prove canonical execution. Require exact upstream versions/hashes, per-object ledgers, checkpoints/freezes, rollback, distinct results, and atomic promotion visibility. No autonomous learning, payments, sentience claim, production credential, or portfolio control plane.
- **Release / version / changelog / artifacts:** blocked `0.1.0-alpha.1`; require versioned event/ledger/freeze/report/memory contracts, accepted upstream inputs, fixture/adversarial matrices, exact-/merged-head reports, per-object evidence, rollback samples, atomic transaction activation evidence, SBOM/checksums, provenance, and changelog.
- **Deploy / health / observability / rollback / validation:** no durable run or promotion; health requires deterministic per-object evidence and complete verified transaction visibility, observes contract/hash identities and promotion decisions, restores accepted snapshot, and proves no unapproved persistence or network activity.

## aevespers2/QSO-STUDIO

- **Objective / user outcome / MVP / priority:** approve a product/UX charter and accurate documentation before building a human-review interface.
- **Architecture / acceptance / non-goals:** Architect/user approve users, workflows, platform, data, privacy, license, and authority; PR #1 remains roadmap-only. No runtime execution, credentials, unrestricted writes, autonomous approval, or payment control.
- **Release / version / changelog / artifacts:** blocked `0.0.1-charter.1`; require charter, diagrams, documentation artifact, integrity/link/accessibility/security reports, fixtures/contracts, checksums, changelog, and provenance.
- **Deploy / health / observability / rollback / validation:** no application target; health is documentation and fixture-workflow integrity, with restoration of the approved charter/docs baseline and repeated validation after failure.

## aevespers2/ALISTAIRE-

- **Objective / user outcome / MVP / priority:** resolve duplicate Alistaire repository identity and produce one evidence-bounded composition charter.
- **Architecture / acceptance / non-goals:** Architect designates canonical repository and migration/archive role; require explicit subsystem contracts, deterministic evaluation, bounded learning, stop controls, and truthful maturity labels. No AGI, consciousness, autonomy, or production-readiness claim.
- **Release / version / changelog / artifacts:** no version; require dual-repository inventory, migration/dependency map, diagrams, evaluation fixtures, privacy/security model, changelog, approval, and provenance.
- **Deploy / health / observability / rollback / validation:** no deployment; prevent duplicate release identity, observe migration decisions and retained history, and restore both repositories to pre-migration state if identity or provenance is lost.

## aevespers2/Alistaire-agi

- **Objective / user outcome / MVP / priority:** resolve duplication with `ALISTAIRE-` and choose one authoritative product location; broad documentation is not implementation evidence.
- **Architecture / acceptance / non-goals:** Architect classifies substantive versus placeholder content and assigns one bounded first Builder task. No runtime, AGI, autonomous tools, persistence, or speculative capability completion.
- **Release / version / changelog / artifacts:** no candidate; require inventory, migration record, charter, dependency map, license/security/privacy decisions, evidence classification, changelog, and provenance.
- **Deploy / health / observability / rollback / validation:** no package, CI, or target; health is identity/content integrity, preserve history, and undo migrations that create ambiguity or data loss.

## aevespers2/Misc

- **Objective / user outcome / MVP / priority:** contain and classify the XYZ defensive firmware-assessment prototype, then migrate it to an approved owner or retire it; portfolio P4.
- **Architecture / acceptance / non-goals:** Architect chooses destination or retirement; require representative/adversarial hardware evidence and explicit limitations. No unauthorized assessment, flashing, disruptive defaults, sensitive data, certification, ATO, or automatic publication.
- **Release / version / changelog / artifacts:** metadata `0.3.0` remains unaccepted; require capability inventory, trusted baselines, hardware matrix, safe dry-run evidence, false-positive/negative analysis, SBOM/checksums, CI, legal/license review, changelog, and provenance.
- **Deploy / health / observability / rollback / validation:** no publication or field deployment; observe hardware/firmware identity and safe dry-run results, restore known firmware/configuration, and verify device integrity after rollback.

## Review log

- **2026-07-18 13:01 PDT:** recorded QuantumStateObjects PR #7 exact head `291d7419bf29a3d979762c4655c05a2a672c6f82`, successful exact-head run `29657511858`, 150 passing tests on Python 3.11/3.13, retained wheel/checksum/head-SHA/JUnit evidence, and artifact digests `b0b302…14388` and `930f14…a6d49`.
- **2026-07-18 13:01 PDT:** recorded resolution of the interruption-reason thread and three newly filed findings, increasing unresolved PR #7 acceptance blockers from five to eight; left QuantumStateObjects default-branch lifecycle files unchanged.
- **2026-07-18 13:01 PDT:** classified QSO-GENOMES PR #5 as a deferred expansion stacked on the canonical candidate rather than a compatibility-set acceptance dependency; portfolio priority did not change.
- **2026-07-18 13:01 PDT:** reviewed all 16 default-branch heads, open issues, active pull requests, and central lifecycle files; no release, deployment, rollback, or approval transition was found.