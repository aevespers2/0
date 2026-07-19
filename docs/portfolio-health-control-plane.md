# Portfolio Health Control Plane

## Objective

Keep the `aevespers2` repository portfolio moving without allowing missing, pending, skipped, failed, stale, or non-exact-head evidence to be mistaken for release readiness.

## Implemented flow

1. **Sentinel** scans every accessible, non-archived owned repository every six hours from trusted `main` code.
2. The scanner retrieves bounded, paginated repository, pull-request, and issue sets.
3. Workflow failures are reported only when the failure remains the newest applicable state for the same workflow, head, and event; a later success supersedes an older failure without deleting history.
4. Every default-branch and open-PR head is checked directly. Missing, pending, skipped, cancelled, neutral, timed-out, action-required, and failed checks are not accepted as successful exact-head validation.
5. Pull-request mergeability is resolved through the authoritative per-PR endpoint with bounded retries for GitHub's temporary unknown state.
6. Blocking issues, stale release provenance, and release metadata contradictions are recorded.
7. **Flow Orchestrator** updates one central issue in Repository `0`; it closes the alert only after a later scan has zero findings and zero scan errors.
8. JSON, Markdown, exact scanner head, runtime version, exit status, and SHA-256 evidence are retained for 90 days.

## Candidate validation

Scanner changes run separately on the exact submitted PR head with read-only permissions. Candidate CI:

- pins GitHub Actions by immutable commit SHA;
- disables persisted checkout credentials;
- asserts the submitted head exactly;
- installs a pinned test runner;
- runs regression tests for superseded failures, exact-head status semantics, mergeability retries, and pagination;
- uploads JUnit, logs, versions, the exact head, and SHA-256 evidence.

Candidate success does not authorize the scheduled scanner to change until the PR is reviewed and merged.

## Authority boundaries

- Scheduled scanning may read portfolio state and update one central health issue.
- It may not merge pull requests, publish releases, rewrite history, change another repository, rerun failed jobs, weaken tests, issue credentials, or close an alert while scan errors remain.
- Cross-repository private access requires a least-privilege `PORTFOLIO_TOKEN`. Without it, inaccessible state is recorded as an error rather than treated as healthy.
- CI Healer, Provenance Steward, Dependency Curator, Incident Custodian, and Release Gatekeeper are bounded role definitions only; they do not have an implemented autonomous write path in this candidate.

## Finding semantics

| Finding | Meaning |
|---|---|
| `failed_ci` | The newest applicable workflow state for a workflow/head/event is unsuccessful |
| `default_head_ci_missing` | No check run is attached to the current default-branch head |
| `default_head_ci_pending` | At least one latest check on the default head is incomplete |
| `default_head_ci_failed` | At least one latest check on the default head is not successful |
| `pr_exact_head_ci_*` | The equivalent fail-closed state for an open PR's exact head |
| `non_mergeable_pr` | The authoritative PR endpoint reports merge conflicts |
| `unknown_mergeability` | Mergeability remains unknown after five bounded retries |
| `unverified_pr_not_draft` | A PR has unresolved exact-head validation but is not draft |
| `blocking_issue` | An open issue carries a security, incident, critical, P0, or blocker label |
| `stale_provenance` | `release.md` exact-head claims do not name the current default head |
| `metadata_contradiction` | Release documentation contradicts observable Actions state |

## Provenance rule

Release documents must distinguish:

- **reviewed baseline** — the immutable commit whose evidence was examined;
- **candidate head** — the commit proposed for release;
- **evidence run** — successful checks and retained artifacts attached to that exact head.

A document commit cannot certify itself merely by embedding its own current SHA. Evidence must be produced after the candidate exists and remain associated with that exact candidate.

## Release boundary

A blocked release is a valid safety result. This control plane reports current state and preserves the route to repair; it does not override repository-specific acceptance gates, review threads, branch protections, security approval, rollback evidence, or human release authority.
