# Developer onboarding

## Prerequisites

The repository currently includes Python, Node/TypeScript, Bash, Git-hook, documentation, and infrastructure-planning surfaces. A complete environment review must inventory each active manifest, lockfile, workflow, local hook, and generated-output path before claiming reproducibility.

Recommended baseline:

- Git with a clean worktree and protected remotes;
- Python 3 with an isolated virtual environment;
- Node.js 20 or the version selected by the active package metadata;
- npm for both TypeScript packages where applicable;
- Bash for repository scripts and the optional pre-push gate;
- Terraform only for reviewing or planning the Clan scaffold, never automatic apply;
- no production credentials in local configuration or test fixtures.

## Initial checkout

```bash
git clone https://github.com/aevespers2/0.git
cd 0
git status --short --branch
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
```

Install project and documentation dependencies only through the currently reviewed manifests. Record the exact Python, pip, Node, npm, and operating-system versions used.

## Core validation

```bash
pytest -q
python3 -m autonomous_vnext.cognitive_runtime "safe tensor evidence mission"
python3 scripts/check_comment_style.py
python -m pip install --requirement requirements-docs.txt
mkdocs build --strict
```

Run package-specific Node checks from their own package directories and record any absent or conflicting lockfiles rather than silently generating new dependency state.

## Repository map

| Path | Purpose |
|---|---|
| `autonomous_vnext/` | core mission, policy, execution, cognition, evidence, and federation primitives |
| `tests/` | Python and cross-surface validation fixtures |
| `scripts/` | federation, evidence, health, policy, and operator utilities |
| `FederationInbox/` | tracked status and proposal intake |
| `FederationDispatch/` | per-surface routing output |
| `FederationRelay/` | contact and handoff evidence |
| `FederationPatches/` | patch-first proposal exchange |
| `docs/` | Pages site and design/operations guidance |
| `integrations/` | Gods, Clan, and external-integration descriptions and scaffolds |
| `punchlists/` | incomplete review, hardening, and acceptance work |
| `.github/workflows/` | CI, policy, validation, and candidate automation |

## Change workflow

1. Read `taskchain.md`, `release.md`, `changelog.md`, and the relevant punch list.
2. Confirm the highest-priority unblocked objective.
3. Create a dedicated branch from the exact current base.
4. Write a task contract naming files, constraints, tests, evidence, stop conditions, and rollback.
5. Make the smallest coherent change.
6. Run focused checks, then the complete applicable suite.
7. Build documentation strictly when architecture, behavior, contracts, setup, or release posture changes.
8. Record the exact head and evidence digests.
9. Open a draft pull request until all gates and contradictions are resolved.
10. Do not merge, release, deploy, or widen credentials merely because candidate CI passes.

## Documentation discipline

Update documentation in the same candidate when a change affects:

- component or data-flow architecture;
- contract fields or compatibility;
- authority and trust boundaries;
- setup, commands, supported runtimes, or generated outputs;
- privacy or security behavior;
- operational recovery or rollback;
- release eligibility or exclusions.

Use evidence-qualified verbs: implemented, configured, observed, tested, proposed, validated, approved, released, and deployed are distinct states.

## Stop conditions

Stop and record the blocker when:

- the requested change conflicts with the current task chain;
- ownership or cross-repository contract semantics are unresolved;
- a credential, remote, or protected branch is required but not explicitly granted;
- current source differs from the reviewed baseline;
- tests expose unrelated failures that cannot be isolated;
- a generated artifact would overwrite canonical source;
- rollback or incident ownership is unclear.

## Pull-request review packet

A strong candidate includes:

- scope and explicit non-goals;
- exact base and head commits;
- changed-file and contract summary;
- validation commands and complete results;
- workflow run and retained artifact references;
- architecture and release-document updates;
- security and privacy implications;
- rollback procedure;
- unresolved contradictions and required owner decisions.
