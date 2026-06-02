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
