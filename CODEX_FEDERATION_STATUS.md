# Codex Federation Status

## Scope

This repository participates in the three-surface Codex coordination loop:

- Local Codex CLI on `/Users/ALISTAIRE`.
- Safari Codex cloud task: `Outline cybernetic autonomous entity`.
- macOS Codex desktop app.
- Codex mobile surface reachable from the Codex application sidebar.
- ChatGPT / Bridge planning surface.

The shared workstream is Autonomous vNext / cognitive-engine continuous integration and development.

## Safe Local Checkout

- Path: `/Users/ALISTAIRE/aevespers2-0`
- Primary remote: `origin` -> `git@github.com:aevespers2/0.git`
- Public redundancy remote: `georgetown` -> `git@github.com:GeorgeTownSabatical/0.git`
- Branch: `main`
- Latest verified commit before this status file: `8935fa5f6301b8adbf6a319d7208d7c470d83832`
- GitHub repo: `https://github.com/aevespers2/0`
- Public mirror: `https://github.com/GeorgeTownSabatical/0`
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
Use `scripts/enforce_federation_remote_write.py` to validate remote-write readiness in an
auditable, machine-checkable way.

## Role Split

- Local CLI: final implementation authority, verification, commits, and deployments.
- Safari/cloud Codex: PR-visible planning, diff review, and cloud-side status reporting.
- macOS desktop Codex: desktop UI observation, local context relay, and sidebar access to mobile.
- Codex mobile: daily user-facing routines, check-ins, completion follow-up, and escalation prompts.
- ChatGPT / Bridge: design and planning assistance, with advisory status only.

Fraud-pipeline work is prioritized when the target repo, APIs, credentials, and safety boundaries are explicit.

## Public Redundancy

The current public backup policy keeps this repository available through two public remotes:

```text
origin      git@github.com:aevespers2/0.git
georgetown  git@github.com:GeorgeTownSabatical/0.git
```

Both remotes were verified at commit:

```text
6faf33e551319b40fed4aa5c039071b7b438c291
```

The tracked public mirror manifest is:

```text
public_mirrors.json
```

The local mirror verifier is:

```bash
python3 scripts/verify_public_mirrors.py --pretty
```

## Federation Inbox

The repository-tracked inbox is:

```text
FederationInbox/
```

Surface directories:

```text
FederationInbox/local/
FederationInbox/safari/
FederationInbox/desktop/
FederationInbox/mobile/
FederationInbox/bridge/
```

Safari/cloud and advisory surfaces export status packets and patch proposals.
Local CLI validates patches and remains the authoritative GitHub writer.
Patch-only behavior is a surface constraint, not a blocker. Use `blocker` only
when a surface cannot produce a current status or patch proposal.

Patch exchange metadata lives under:

```text
patches/
```

Evaluate the inbox with:

```bash
python3 -m autonomous_vnext.federation_kernel --authoritative-head "$(git rev-parse HEAD)" --pretty
```

Write Local CLI status into the inbox with:

```bash
python3 scripts/write_local_federation_status.py
```

Install and enable the federation pre-push hook for automatic enforcement and
runtime cleanup auditing:

```bash
python3 scripts/setup_federation_git_hooks.py
python3 scripts/enforce_federation_remote_write.py --authoritative-head "$(git rev-parse HEAD)"
```

Write Safari, Desktop, Mobile, or Bridge status into the inbox with:

```bash
python3 scripts/write_federation_message.py \
  --agent safari_cloud \
  --type status \
  --cwd /workspace/0 \
  --branch work \
  --commit "$(git rev-parse HEAD)" \
  --blocker no_remote \
  --next-action "export patch proposal"
```

Export a patch bundle for Local CLI review with:

```bash
python3 scripts/write_patch_bundle.py \
  --agent safari_cloud \
  --commit "$(git rev-parse HEAD)" \
  --summary "Describe proposed change" \
  --file README.md
```

Verify proposed patch bundles without applying them with:

```bash
python3 scripts/verify_patch_proposals.py --authoritative-head "$(git rev-parse HEAD)" --pretty
```

Check or apply one verified patch proposal with:

```bash
python3 scripts/apply_verified_patch.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --source safari_cloud \
  --pretty
```

Use `--apply` only after Local CLI review and a clean worktree check.

Write a federation state report with:

```bash
python3 scripts/write_federation_state_report.py --authoritative-head "$(git rev-parse HEAD)" --print
```

Run Safari as patch-first producer:

```bash
python3 scripts/safari_patch_workflow.py \
  --summary "Describe proposed change" \
  --file README.md \
  --pretty
```

Emit mobile-facing check-in status:

```bash
python3 scripts/write_mobile_federation_status.py
```

Emit bridge signal for planning integration:

```bash
python3 scripts/emit_bridge_signal.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --pretty
```

Write dispatch packets for surfaces that owe status refreshes or unblock actions:

```bash
python3 scripts/write_federation_dispatch.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --print
```

Dispatch packets include a helper command, a self-contained `status_template`,
and copy-ready `handoff_text` so Safari/cloud can respond even when helper
scripts are unavailable in the cloud container.

Run the local federation routine to refresh local/desktop/mobile status, bridge
signal, state report, and dispatch in one pass:

```bash
python3 scripts/run_federation_routine.py --print
```

Record UI/browser/app contact attempts as relay evidence:

```bash
python3 scripts/record_federation_contact.py \
  --surface safari_cloud \
  --channel safari_chatgpt \
  --status staged \
  --dispatch FederationDispatch/safari/dispatch.json \
  --detail "handoff inserted into composer"
```

## Continuous Integration

The repository now has a shared CI entry point:

```text
.github/workflows/autonomous-vnext-ci.yml
```

It runs:

- `pytest -q` locally; CI installs pytest and runs it through the Python interpreter configured by `actions/setup-python`.
- `python3 -m autonomous_vnext.cognitive_runtime "ci federation coordination smoke" --output /tmp/cognitive_runtime_report.json` locally.
- `python3 scripts/emit_codex_federation_status.py --pretty` locally.

The machine-readable local coordination packet is:

```bash
python3 scripts/emit_codex_federation_status.py --pretty
```
