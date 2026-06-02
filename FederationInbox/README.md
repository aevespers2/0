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
