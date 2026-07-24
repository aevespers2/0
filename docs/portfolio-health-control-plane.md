# Portfolio Health Control Plane v3.1

## Purpose

This control plane inspects the owned `aevespers2` GitHub portfolio without allowing missing, queued, skipped, cancelled, stale, failed, or non-exact-head evidence to be represented as healthy or release-ready.

It is a bounded observation and repair-routing system. It does not merge pull requests, publish releases or Pages, deploy software, change credentials, rewrite history, apply infrastructure, or override repository-specific review and rollback gates.

## Current repair

Version 3 established dedicated portfolio credentials, public-only fallback coverage, stable finding identities, semantic deduplication, one canonical issue route, exact-head validation, and retained evidence. Review of the trusted scanner then found a remaining exact-head coverage defect: workflow security and artifact expectations were read only from the default branch. A workflow introduced or modified solely on an open pull-request head could therefore evade permission and mutable-Action checks, and a PR-only workflow that declared artifact upload could finish successfully without retained artifacts while the scanner consulted an unrelated default-branch workflow tree.

Version 3.1 closes that bounded defect:

1. the default workflow tree is read from the immutable default commit rather than a mutable branch name;
2. every unique open-PR head receives its own workflow-source inspection;
3. PR findings are bound to repository, PR, exact head, workflow path, and normalized failure kind;
4. workflow files byte-identical to the trusted default copy are not reported again for each PR;
5. artifact expectations are resolved from the workflow source at the exact run head;
6. new regressions exercise changed unsafe workflows, inherited safe workflows, mutable Action references, and missing artifacts from PR-only workflows;
7. no merge, release, publication, deployment, credential, or infrastructure authority is added.

## Inspection surface

For every accessible, non-archived owned repository, the scanner evaluates:

- current default-branch and open-PR heads;
- newest applicable workflow state per workflow, head, and event;
- missing, incomplete, skipped, cancelled, stale, timed-out, action-required, and failed exact-head checks;
- authoritative PR mergeability with bounded retries;
- security, incident, P0, critical, and blocker issues;
- top-level workflow permissions and privileged automatic triggers at the exact default and open-PR heads;
- mutable third-party Action references introduced or changed on open PRs;
- successful workflows that declare artifact upload at the run's exact head but retain no artifact;
- local Markdown links from `README.md`, `taskchain.md`, `punchlist.md`, `release.md`, and `changelog.md`;
- stale exact-head statements and observable workflow contradictions in `release.md`.

## Exact-state and deduplication rule

The current state is keyed by:

```text
repository
+ issue or pull-request identity
+ exact head
+ workflow run and event
+ normalized failure signature
+ resolution state
```

The sorted findings and scan errors are serialized deterministically and hashed. The generated Markdown begins with:

```text
<!-- portfolio_fingerprint=sha256:... -->
```

The scheduled workflow reads prior comments on issue #9. When the newest fingerprint equals the current fingerprint, it emits no new comment. A changed fingerprint produces one new evidence-bearing comment. The stable policy issue is never overwritten or automatically closed.

## Workflow safety

Candidate validation uses read-only permissions, immutable Action SHAs, exact-head checkout, disabled credential persistence, a pinned test dependency, deterministic source hashes, clean-tree verification, and a 90-day artifact.

The trusted scanner has only `contents: read` and `issues: write`. The write scope is limited to a fingerprint-deduplicated comment on issue #9. Reports and checksums are created under the runner temporary directory and retained for 90 days.

An absent or inaccessible repository, malformed API response, incomplete scan, or missing report is a scan error and fails the workflow closed. Findings themselves do not cause the scanner to conceal the report; they remain repair inputs.

## Repair lifecycle

```text
observe exact state
→ normalize finding identity
→ compare semantic fingerprint
→ preserve changed evidence
→ diagnose bounded root cause
→ prepare focused reversible branch
→ validate exact head
→ merge only when independently safe and permitted
→ rescan resulting state
```

Equivalent prose: the scanner observes and records current evidence first. Repair work is separate, focused, reversible, and revalidated after integration. Neither scanner success nor a clean fingerprint grants release or operational authority.

## FYSA-120 capability mapping

- **CAT-012:** `012-D` link checking and documentation testing; `012-E` docs-as-code and lifecycle synchronization.
- **CAT-017:** `017-C` derivation-chain recording; `017-D` version-substitution detection; `017-E` hashing, audit packaging, and correction propagation.
- **CAT-022:** `022-A` dependency pinning; `022-C` deterministic execution; `022-D` checksum validation; `022-E` artifact packaging.
- **CAT-031:** `031-A` threat-aware acceptance criteria; `031-D` integration and regression testing; `031-E` verified builds, change-impact analysis, and remediation.
- **CAT-040:** `040-A` system archaeology; `040-B` dependency mapping; `040-E` rollback planning and post-repair monitoring.
- **CAT-052:** `052-B` least privilege; `052-E` audit evidence and continuous assurance.
- **CAT-054:** `054-B` supply-chain hardening; `054-E` control validation.

The existing non-authoritative gap **`031-L — portfolio exact-state repair orchestration`** includes active-head enumeration, exact-head workflow-source inspection, failure-signature normalization, semantic deduplication, artifact-presence verification, stale-provenance reconciliation, and bounded repair resumption. It does not expand authorization.

## Acceptance criteria

The control plane is acceptable for `main` only when:

- all focused scanner regressions pass on the exact submitted head;
- workflow-security and artifact checks demonstrably use each default or PR run's immutable source head;
- all Actions are immutable and permissions remain least privilege;
- generated evidence remains outside the checkout and is retained;
- the repair PR is based on current `main`, mergeable, and free of unresolved high-risk review findings;
- issue #9 is the only automated notification route;
- an unchanged fingerprint demonstrably produces no duplicate comment;
- production, credentials, destructive history, release, publication, deployment, and infrastructure changes remain blocked.
