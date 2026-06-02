# Federation Inbox

This directory is the repository-tracked coordination substrate for Codex surfaces.

Agents should write JSON messages into their own surface folder:

- `local/`
- `safari/`
- `desktop/`
- `mobile/`
- `bridge/`

Local CLI is the authoritative GitHub write agent. Other surfaces should submit
status packets, plans, and patch proposals here rather than pushing directly.

Use `patches/` for patch proposal metadata and optional patch text references.
Safari and advisory surfaces should emit patch proposals instead of direct pushes.

To remove stale/blocked runtime packets after relay:

```
python3 scripts/prune_federation_runtime.py --inbox FederationInbox --authoritative-head "$(git rev-parse HEAD)" --print
```

This is dry-run by default. Add `--delete` to move matching packets to
`state/federation_runtime_archive`, or `--delete --no-archive` to hard-delete.

Desktop should emit status through the safe-check helper so wrong checkouts are
explicitly blocked:

```bash
python3 scripts/write_desktop_federation_status.py \
  --safe-root /Users/ALISTAIRE/aevespers2-0
```

Mobile should emit user-facing routine packets for check-ins and completion follow-up:

```bash
python3 scripts/write_mobile_federation_status.py
```

Safari patch exports should use:

```bash
python3 scripts/safari_patch_workflow.py \
  --summary "Describe proposed change" \
  --file README.md \
  --pretty
```

When the kernel reports missing/stale packets, local_cli writes instructions to
`FederationDispatch/`:

```bash
python3 scripts/write_federation_dispatch.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --print
```
