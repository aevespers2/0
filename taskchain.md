# Task Chain

## Purpose
This file is the Architect-controlled execution chain for this repository. Builders must work from the highest-priority unblocked task and preserve evidence, tests, and rollback paths.

## Roles
- **Architect:** defines dependencies, acceptance criteria, sequencing, and architectural boundaries.
- **Builder:** implements one bounded task at a time, records verification, and reports blockers without silently changing scope.

## Workflow
1. Architect adds or reprioritizes tasks.
2. Builder claims the first unblocked `READY` task.
3. Builder changes status to `IN PROGRESS` and records the branch or commit.
4. Builder runs relevant tests and records evidence.
5. Architect reviews completion and unlocks dependent tasks.

## Task States
`PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Active Chain
| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0 | Repository health baseline | Architect | — | READY | Current workflows, tests, dependencies, and known defects are inventoried. |
| P1 | Define next bounded implementation task | Architect | Repository health baseline | PROPOSED | A Builder-ready task has explicit files, tests, constraints, and rollback guidance. |

## Builder Log
Record commit links, test commands, results, unresolved risks, and follow-up tasks here.
