# Federation Patches

This directory is the durable patch exchange lane for nonlocal Codex surfaces.

Local CLI remains the authoritative GitHub write agent. Safari, desktop,
mobile, and bridge surfaces should place git patch text under `inbox/` and emit
a matching `patch_proposal` message in `FederationInbox/<surface>/`.

Patch proposals must point at the authoritative base commit and are verified
with:

```bash
python3 scripts/verify_patch_proposals.py \
  --authoritative-head "$(git rev-parse HEAD)" \
  --pretty
```

Only Local CLI should apply verified proposals and push to the public mirrors.
