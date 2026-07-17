# Portfolio Health Control Plane

## Objective

Keep the `aevespers2` repository portfolio moving without allowing missing evidence, stale provenance, weak validators, unsafe mutable-state writers, or failing CI to be mistaken for release readiness.

## Operating flow

1. **Sentinel** scans every non-archived owned repository every six hours.
2. Findings are normalized by repository, severity, and invariant family.
3. **Flow Orchestrator** deduplicates findings into one central health issue rather than creating competing repair paths.
4. **CI Healer**, **Provenance Steward**, **Dependency Curator**, or **Incident Custodian** prepares the smallest reversible repair appropriate to the finding.
5. Candidate changes run exact-head CI with read-only permissions.
6. **Release Gatekeeper** evaluates release claims using trusted base-branch validation and immutable artifacts; it cannot approve a validator change using only that changed validator.
7. The central issue is updated while findings remain and closed automatically only after a later scan reports no significant findings.

## Schedules and triggers

| Control | Trigger | Cadence |
|---|---|---|
| Portfolio scan | GitHub Actions schedule and manual dispatch | Every six hours at minute 17 |
| Candidate scanner validation | Pull request path filter | Every relevant PR update |
| Dependency/runtime inventory | Agent policy | Weekly |
| CI repair | Failed workflow finding | Event-driven after scan |
| Provenance repair | Stale candidate or exact-head evidence | Event-driven after scan |
| Incident containment | Integrity or mutable-writer finding | Immediate fail-closed routing |
| Release gate | PR/release metadata change | Before readiness or publication claims |

## Authority boundaries

- Scheduled scanning checks out `main`, so portfolio decisions are made by trusted code rather than a submitted PR head.
- Candidate CI checks out the submitted PR SHA exactly, uses read-only permissions, and validates syntax plus the agent registry.
- The scanner may update one issue in Repository `0`; it does not merge, publish, rewrite release history, weaken tests, or silently repair other repositories.
- Cross-repository private access requires a least-privilege `PORTFOLIO_TOKEN` secret. Without it, the scanner covers accessible public state and records access failures instead of claiming complete coverage.
- Integrity incidents preserve evidence and block destructive cleanup until writer identity, invocation path, containment, repair, replay, and explicit closure are documented.

## Provenance rule

Release documents must distinguish:

- **reviewed baseline** — the immutable commit whose evidence was actually examined;
- **candidate head** — the commit proposed for release;
- **evidence run** — the workflow run and artifacts attached to that exact candidate.

A document commit cannot truthfully certify itself merely by embedding its own current SHA. Evidence must be generated after the candidate exists, or the embedded SHA must be labeled as the reviewed parent/baseline rather than the current head.

## Definition of flow

The system is flowing when findings are detected early, routed once, repaired through bounded branches, validated at the submitted head by read-only CI, independently gated from trusted code, and automatically cleared only after the portfolio returns to a verified healthy state. A blocked release remains a valid safety outcome; the control plane's purpose is to make the route from block to verified recovery explicit and fast, not to erase legitimate gates.
