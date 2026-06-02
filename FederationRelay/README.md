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

Valid statuses:

- `observed`
- `staged`
- `sent`
- `acknowledged`
- `blocked`
- `failed`
