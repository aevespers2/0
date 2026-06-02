# Codex Federation Status

## Scope

This repository participates in the three-surface Codex coordination loop:

- Local Codex CLI on `/Users/ALISTAIRE`.
- Safari Codex cloud task: `Outline cybernetic autonomous entity`.
- macOS Codex desktop app.

The shared workstream is Autonomous vNext / cognitive-engine continuous integration and development.

## Safe Local Checkout

- Path: `/Users/ALISTAIRE/aevespers2-0`
- Remote: `git@github.com:aevespers2/0.git`
- Branch: `main`
- Latest verified commit before this status file: `8935fa5f6301b8adbf6a319d7208d7c470d83832`
- GitHub repo: `https://github.com/aevespers2/0`
- Local GitHub account: `GeorgeTownSabatical`
- Permission observed with GitHub CLI: `WRITE`

## Verified Checks

Latest local verification:

```text
pytest -q
28 passed in 0.21s
```

```text
python3 -m autonomous_vnext.cognitive_runtime "federated codex coordination evidence mission"
reports/cognitive_runtime_report.json
```

The runtime report remained unchanged in the worktree after the smoke run.

## Cloud Task State

The Safari cloud task has reported ephemeral container behavior:

- `/workspace/0` on branch `work`.
- Clean working tree.
- Latest visible cloud commit has varied by container (`37bef3f`, `8d899ca`, and related local-only SHAs).
- One container added HTTPS `origin` and failed push with `CONNECT tunnel failed, response 403`.
- A retry container did not retain `origin`.

Cloud-side push should not be treated as authoritative until the task reports a stable remote and a successful push.

## Desktop App State

The macOS Codex desktop app reports local GitHub authentication, but its visible chat resolved the active checkout to `/Users/ALISTAIRE/Documents`.

Do not push from `/Users/ALISTAIRE/Documents`.

The safe repo path for desktop/local GitHub work is:

```text
/Users/ALISTAIRE/aevespers2-0
```

## Coordination Rule

All agents should report exact status before remote writes:

```bash
pwd
git status --branch --short
git remote -v
git log --oneline -n 1
```

Remote writes are allowed only from an explicit safe repository path.
