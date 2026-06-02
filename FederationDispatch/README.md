# Federation Dispatch

This directory holds local_cli-generated routing instructions for Codex surfaces.

Dispatch packets are not status packets. They tell a surface which packet the
kernel currently needs, without pretending that local_cli can speak as that
surface.

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
