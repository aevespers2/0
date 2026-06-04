# Federation Dispatch

This directory holds local_cli-generated routing instructions for Codex surfaces.

Dispatch packets are not status packets. They tell a surface which packet the
kernel currently needs, without pretending that local_cli can speak as that
surface.

Each dispatch includes:

- `command`: the preferred local helper command.
- `status_template`: the equivalent packet to emit when the helper is unavailable.
- `handoff_text`: copy-ready instructions for Safari/Desktop/Mobile/Bridge context.
- `parallel_work`: the current cross-surface work allocation contract.

The `parallel_work` block lets surfaces plan and execute concurrently without
sharing uncontrolled write access. It assigns durable roles:

- `local_cli`: authoritative integrator, tests, commits, approved pushes.
- `safari_cloud`: patch-first parallel builder and reviewer.
- `desktop_app`: local context observer and UI/status relay.
- `mobile`: user-facing follow-up, approvals, and escalation summaries.
- `chatgpt_bridge`: planning, task decomposition, dispatch coordination, and
  status synthesis.

Parallel execution is allowed when work is bounded and reported through the
inbox. If two surfaces need the same file or runtime resource, the dispatch
owner is primary and the other surface becomes reviewer or patch proposer.

Patch-only Safari behavior is represented as a `constraints` value, not a
`blocker`. A blocker means the surface cannot participate in synchronization.

Default runtime outputs are ignored:

- `FederationDispatch/local/dispatch.json`
- `FederationDispatch/safari/dispatch.json`
- `FederationDispatch/desktop/dispatch.json`
- `FederationDispatch/mobile/dispatch.json`
- `FederationDispatch/bridge/dispatch.json`
- `FederationDispatch/dispatch.json`

Generate dispatch packets from current federation state:

```bash
python3 scripts/write_federation_dispatch.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --print
```
