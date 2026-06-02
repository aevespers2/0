# Federation Relay

This directory documents surface-contact evidence for Codex federation.

Relay events are not status packets and do not satisfy federation readiness.
They record attempts to contact a surface through a UI, browser tab, desktop app,
or bridge channel.

Default runtime outputs are ignored:

- `reports/federation_contact_log.jsonl`
- `reports/federation_contact_latest.json`

Record a contact event:

```bash
python3 scripts/record_federation_contact.py \
  --surface safari_cloud \
  --channel safari_chatgpt \
  --status staged \
  --dispatch FederationDispatch/safari/dispatch.json \
  --detail "handoff inserted into composer; send unavailable while page is answering" \
  --evidence title="Cognitive OS Development" \
  --evidence composer_contains_handoff=true
```

Refresh Safari's staged handoff from the latest dispatch and record the contact
event:

```bash
python3 scripts/stage_safari_dispatch.py --print
```

Watch for the staged Safari handoff to become sendable:

```bash
python3 scripts/watch_safari_dispatch_send.py --timeout 30 --print
```

To click the send control once it appears, add `--send`.

Write a compact relay summary:

```bash
python3 scripts/write_federation_relay_summary.py --print
```

Run a bounded Safari relay retry loop:

```bash
python3 scripts/run_safari_relay_retry.py \
  --attempts 3 \
  --interval 5 \
  --watch-timeout 10 \
  --print
```

Add `--send` only when the staged handoff should be clicked once Safari exposes
a send control.

Extract an explicit Safari acknowledgment from the visible ChatGPT conversation:

```bash
python3 scripts/extract_safari_ack.py --print
```

This records contact evidence when no valid packet is present. If Safari has
emitted a valid `codex_federation_message.v1` packet and the packet should be
transcribed into the repository inbox, add `--write-status`.

Valid statuses:

- `observed`
- `staged`
- `sent`
- `acknowledged`
- `blocked`
- `failed`
