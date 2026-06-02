# 0

Autonomous vNext Phase-0 scaffolding for a constrained, auditable builder-agent.

## What Is Here

- [AUTONOMOUS_VNEXT.md](AUTONOMOUS_VNEXT.md): architecture, guardrails, risk rubric, and build checklist.
- [mission_contract.schema.json](mission_contract.schema.json): mission intake contract.
- [action_record.schema.json](action_record.schema.json): append-only execution/audit event contract.
- [public_mirrors.json](public_mirrors.json): public dual-redundancy mirror manifest.
- [FederationInbox/](FederationInbox): repository-tracked status and patch-proposal inbox for Codex surfaces.
- [FederationDispatch/](FederationDispatch): local_cli-generated per-surface routing instructions.
- [FederationRelay/](FederationRelay): UI/browser/app contact evidence for surface handoffs.
- [FederationPatches/](FederationPatches): patch exchange area for advisory/cloud proposals.
- [autonomous_vnext/policy.py](autonomous_vnext/policy.py): deny-by-default policy evaluator.
- [autonomous_vnext/audit.py](autonomous_vnext/audit.py): append-only JSONL audit writer.
- [autonomous_vnext/planner.py](autonomous_vnext/planner.py): minimal candidate planning and risk scoring.
- [autonomous_vnext/executor.py](autonomous_vnext/executor.py): policy-gated execution checks and evidence reports.
- [autonomous_vnext/itensor_adapter.py](autonomous_vnext/itensor_adapter.py): optional ITensor-backed plan scoring adapter.
- [autonomous_vnext/cognitive_hilbert.py](autonomous_vnext/cognitive_hilbert.py): tensor-product Hilbert backbone model.
- [autonomous_vnext/cognitive_state.py](autonomous_vnext/cognitive_state.py): subsystem state representation over the Hilbert backbone.
- [autonomous_vnext/attention_operator.py](autonomous_vnext/attention_operator.py): subsystem attention operators.
- [autonomous_vnext/belief_evolution.py](autonomous_vnext/belief_evolution.py): observation-driven cognitive update operators.
- [autonomous_vnext/sheaf_consistency.py](autonomous_vnext/sheaf_consistency.py): local belief patch consistency checks.
- [autonomous_vnext/tensor_memory.py](autonomous_vnext/tensor_memory.py): vector/tensor memory search primitives.
- [autonomous_vnext/multiagent_tensor_mesh.py](autonomous_vnext/multiagent_tensor_mesh.py): coupled multi-agent state mesh.
- [autonomous_vnext/mission_projection.py](autonomous_vnext/mission_projection.py): objective projection into goal subspace.
- [autonomous_vnext/goal_hamiltonian.py](autonomous_vnext/goal_hamiltonian.py): goal energy scoring.
- [autonomous_vnext/uncertainty_operator.py](autonomous_vnext/uncertainty_operator.py): entropy/confidence reporting.
- [autonomous_vnext/cognitive_runtime.py](autonomous_vnext/cognitive_runtime.py): deterministic end-to-end cognitive cycle runner.
- [autonomous_vnext/experience_memory.py](autonomous_vnext/experience_memory.py): append-only cognitive experience memory.
- [autonomous_vnext/federation.py](autonomous_vnext/federation.py): cross-surface Codex synchronization, role assignment, and recurring routine primitives.
- [autonomous_vnext/federation_kernel.py](autonomous_vnext/federation_kernel.py): inbox reader, patch proposal validator, and coordination report generator.
- [autonomous_vnext/self_model.py](autonomous_vnext/self_model.py): explicit capability/limitation/confidence model.
- [autonomous_vnext/reflection.py](autonomous_vnext/reflection.py): expected-vs-observed reflection updates.

## Test

```bash
pytest -q
```

The ITensor integration is dependency-gated. Tests mock availability, so the core suite does not require ITensor bindings to be installed.

GitHub Actions runs the same suite plus a cognitive-runtime smoke check in
[`.github/workflows/autonomous-vnext-ci.yml`](.github/workflows/autonomous-vnext-ci.yml).

## Run A Cognitive Cycle

```bash
python3 -m autonomous_vnext.cognitive_runtime "safe tensor evidence mission"
```

The default report is written to `reports/cognitive_runtime_report.json`.

To persist the cycle as experience memory:

```bash
python3 -m autonomous_vnext.cognitive_runtime \
  "safe tensor evidence mission" \
  --persist-experience \
  --memory state/experience_memory.jsonl
```

## Codex Federation Status

For local CLI, Safari/cloud Codex, and macOS desktop Codex coordination, emit the
shared status packet before remote writes:

```bash
python3 scripts/emit_codex_federation_status.py --pretty
```

Verify public mirror heads from a local checkout with both remotes reachable:

```bash
python3 scripts/verify_public_mirrors.py --pretty
```

Evaluate federation inbox messages with Local CLI as the authoritative writer:

```bash
python3 -m autonomous_vnext.federation_kernel \
  --authoritative-head "$(git rev-parse HEAD)" \
  --pretty
```

Write Local CLI's current status packet into the inbox:

```bash
python3 scripts/write_local_federation_status.py
```

Write a nonlocal surface status packet:

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

Prune stale/failing runtime packets once the state is reconciled:

```bash
python3 scripts/prune_federation_runtime.py \
  --inbox FederationInbox \
  --authoritative-head "$(git rev-parse HEAD)" \
  --print
```

Add `--delete` to move selected packets into `state/federation_runtime_archive`, or `--delete --no-archive` to hard-delete selected packets.

Export a working-tree diff as a patch bundle for Local CLI review:

```bash
python3 scripts/write_patch_bundle.py \
  --agent safari_cloud \
  --commit "$(git rev-parse HEAD)" \
  --summary "Describe proposed change" \
  --file README.md
```

Verify proposed patch bundles without applying them:

```bash
python3 scripts/verify_patch_proposals.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --pretty
```

Check or apply one verified patch proposal:

```bash
python3 scripts/apply_verified_patch.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --source safari_cloud \
  --pretty
```

Add `--apply` only after reviewing the patch and confirming the worktree is clean.

Write a durable federation state report:

```bash
python3 scripts/write_federation_state_report.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --print
```

Run Safari production as patch-first workflow:

```bash
python3 scripts/safari_patch_workflow.py \
  --summary "Describe proposed change" \
  --file README.md \
  --pretty
```

Emit a bridge-facing signal for external coordination and planning:

```bash
python3 scripts/emit_bridge_signal.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --pretty
```

Write per-surface dispatch packets from the current federation state:

```bash
python3 scripts/write_federation_dispatch.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --print
```

Run the local daily federation routine in one command:

```bash
python3 scripts/run_federation_routine.py --print
```

Record a browser/app contact attempt:

```bash
python3 scripts/record_federation_contact.py \
  --surface safari_cloud \
  --channel safari_chatgpt \
  --status staged \
  --detail "handoff inserted into composer"
```

Contact recording writes both the global latest event and a per-surface latest
event under `reports/federation_contact_latest/`.

Summarize Safari/Desktop relay-contact freshness:

```bash
python3 scripts/write_federation_contact_report.py --print
```

Write a compact federation dashboard:

```bash
python3 scripts/write_federation_dashboard.py --refresh-mirrors --print
```

Probe the macOS Codex desktop app and record live app evidence:

```bash
python3 scripts/probe_desktop_codex_app.py --print
```

Refresh and stage Safari's current dispatch in the Safari composer:

```bash
python3 scripts/stage_safari_dispatch.py --print
```

Watch Safari until the staged dispatch is sendable:

```bash
python3 scripts/watch_safari_dispatch_send.py --timeout 30 --print
```

Summarize current relay state:

```bash
python3 scripts/write_federation_relay_summary.py --print
```

Run bounded Safari relay retries:

```bash
python3 scripts/run_safari_relay_retry.py --attempts 3 --print
```

Run one full Safari sync cycle:

```bash
python3 scripts/run_safari_sync_cycle.py --print
```

This refreshes the routine, stages Safari dispatch, checks sendability, probes
for an explicit Safari acknowledgment, and rewrites the relay summary, contact
report, and dashboard.

Extract an explicit Safari status acknowledgment from the visible ChatGPT tab:

```bash
python3 scripts/extract_safari_ack.py --print
```

Add `--write-status` only when the visible Safari response contains a valid
`codex_federation_message.v1` packet that should be transcribed to
`FederationInbox/safari/status.json`.

Enforce remote-write readiness before push (this is the authoritative gate):

```bash
python3 scripts/enforce_federation_remote_write.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --print
```

Write a mobile surface check-in packet:

```bash
python3 scripts/write_mobile_federation_status.py \
  --repo /Users/ALISTAIRE/aevespers2-0 \
  --output FederationInbox/mobile/status.json
```

Install the local pre-push federation hooks (remote-write gate + runtime cleanup audit):

```bash
python3 scripts/setup_federation_git_hooks.py
```

Run status emission for desktop in a safe-check mode that blocks wrong checkouts:

```bash
python3 scripts/write_desktop_federation_status.py \
  --repo /Users/ALISTAIRE/aevespers2-0
```
