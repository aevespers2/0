# Repository Health Baseline

## Scope

This document records the bounded Phase 1 identity and runtime inventory for Repository `0`. It does not claim that the complete P0 health baseline, clean installation, test suite, security review, or release gate has passed.

- **Baseline source commit:** `7333f441138bdc0d596232581c52e5e1134cd142`
- **Builder branch:** `builder/repository-purpose-runtime-baseline-v1`
- **Repository:** `aevespers2/0`
- **Visibility:** public
- **Default branch:** `main`

## Purpose

Repository `0` contains Autonomous vNext Phase-0 scaffolding for a constrained, auditable builder-agent. The active product directive prioritizes a reproducible health baseline followed by one bounded local mission that is policy-gated, reversible, and fully evidenced. Existing implementation surfaces include mission and action schemas, deny-by-default policy evaluation, append-only audit records, deterministic planning and cognitive-runtime components, federation proposal validation, and local evidence generation.

The current MVP explicitly excludes credential discovery, silent pushes or deployment, destructive operations, unrestricted networking, production scientific claims, and cross-repository publication authority.

## Languages and repository formats

| Category | Evidence-backed role |
|---|---|
| Python | Primary implementation, scripts, CLI entry points, runtime smoke path, and tests. |
| JSON / JSON Schema | Mission and action contracts, mirror manifests, federation packets, reports, state, and evidence artifacts. |
| YAML | GitHub Actions workflow configuration. |
| Markdown | Product, architecture, release, punch-list, task-chain, and operator documentation. |

This is a source-level inventory, not a GitHub language-statistics claim.

## Package manager and dependency state

- The configured CI uses `python -m pip` to install `pip` and `pytest` directly.
- No `pyproject.toml`, `requirements.txt`, or `setup.py` exists at the baseline ref.
- The repository therefore has no discovered Python package manifest or lockfile in the checked root paths.
- The package is exercised from the source tree rather than installed as a declared distribution.
- `pytest` is currently unpinned in the workflow, and `pip` is upgraded from the mutable package index during each run.
- ITensor support is described as optional and dependency-gated; the core tests do not require ITensor bindings.

These observations are inventory findings. Dependency consistency, advisories, reproducible installation, and package-manifest remediation remain Phase 2 work.

## Runtime baseline

| Surface | Recorded runtime |
|---|---|
| GitHub Actions runner | `ubuntu-latest` |
| GitHub Actions Python | `3.11` |
| Test command | `python -m pytest -q` |
| Cognitive smoke command | `python -m autonomous_vnext.cognitive_runtime ...` |
| Documentation command form | `python3` |

Python 3.11 is the only explicitly pinned and therefore currently evidenced supported Python version. The documentation's generic `python3` form does not establish compatibility with other minor versions.

## Evidence inventory

| Source | Git blob SHA | What it establishes |
|---|---|---|
| `README.md` | `e7d19a0f707c8a748d987a9bdd6d78af32ae6263` | Repository purpose, implementation map, test command, optional ITensor boundary, and documented CLI usage. |
| `taskchain.md` | `50a8bed1aaa660e9df5756ab940c531590e4a205` | Active product directive, MVP scope, priority, success criteria, and non-goals. |
| `.github/workflows/autonomous-vnext-ci.yml` | `8bff5231345c03e08aa620674b5c1bc740babc35` | Ubuntu runner, Python 3.11, pip/pytest installation, test command, and smoke/validation entry points. |
| `autonomous_vnext/__init__.py` | `113c40b6a067952beadf95eff694dea7d96238c1` | Python package identity and implemented module surface. |
| `punchlist.md` | `e217f8d58a873d876c6a467461df851a51b2dce5` | P0 Phase 1 ordering and acceptance boundary. |

Root-path probes for `pyproject.toml`, `requirements.txt`, and `setup.py` returned `404 Not Found` at the baseline ref.

## Result and stop condition

**Result: PASS for Phase 1 item 1 only** — repository purpose, default branch, primary implementation languages/formats, package-manager behavior, and evidenced runtime version are now recorded.

Stop here. Do not treat this as completion of Phase 1 or P0. The next Builder item is the top-level directory and responsibility inventory, followed by manifest/build/workflow inventory in the order defined by `punchlist.md`.

## Rollback

Delete this document and revert the associated `punchlist.md` and `taskchain.md` entries. No runtime, schema, workflow, dependency, or production behavior is changed by this bounded documentation task.
