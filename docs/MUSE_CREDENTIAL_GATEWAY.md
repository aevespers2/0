# Muse Credential Gateway

Muse never receives, reads, stores, prints, or transmits the raw GitHub credential. Repository 0 sends signed operation requests to a narrow credential gateway, which evaluates the request against a Repository 1-approved grant manifest and VTX capability.

## Boundary

```text
Muse
  | structured request; no token
  v
Repository 0 proposal builder
  | signed VTX envelope
  v
Credential gateway
  | policy lookup and token use
  v
GitHub
  | execution result
  v
Gateway receipt -> Repository 1 audit
```

## Gateway Rules

- The token exists only in the gateway's ephemeral secret environment.
- The token value is never serialized into an event, exception, command line, prompt, patch, receipt, or log.
- Repository 1 is hard-denied as a target regardless of token capabilities.
- Only `muse/proposal/` branches are permitted for Muse writes.
- The gateway accepts structured operations, not arbitrary shell commands or URLs.
- Each request requires a fresh signed VTX envelope and unique nonce.
- The payload hash must be computed before the gateway call and verified against the exact bytes sent to GitHub.
- Responses are normalized and secret-redacted before returning to Muse.
- All denials produce audit receipts without secret material.

## Allowed Initial Operations

- read repository metadata for `aevespers2/0`;
- read files needed for an assigned task;
- create `muse/proposal/<task-id>` branches;
- create or update files only on that task branch;
- open or update a pull request from that branch;
- read pull-request checks and review comments.

## Explicitly Disallowed

- direct writes to `main`;
- access to `aevespers2/1`;
- arbitrary GitHub API calls;
- workflow dispatch or workflow editing;
- release creation;
- secrets or environment access;
- repository settings or collaborator changes;
- deletion, force push, branch protection changes, or visibility changes;
- token introspection or retrieval.

## Failure Mode

When Repository 1 policy cannot be verified, the gateway fails closed. It does not fall back to GitHub token permissions, cached permissive policy, or Muse's own assessment.
