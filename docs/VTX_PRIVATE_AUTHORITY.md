# VTX Private-Authority Architecture

## Status

Phase 0 design and reference implementation for making the private repository the canonical authority while treating GitHub as a constrained publication and automation endpoint.

## Trust Model

The authoritative repository, signing keys, policy state, and audit ledger remain outside GitHub. GitHub receives only explicitly authorized commits, releases, artifacts, or workflow requests. No inbound GitHub event has direct write authority over the canonical store.

## Data Flow

```text
Private Authoritative Store
        |
        v
VTX Envelope Builder
        |
        v
Policy + Signature + Freshness Verification
        |
        v
GitHub Adapter / Actions Gateway
        |
        v
GitHub repository, release, workflow, or webhook
        |
        v
Signed receipt returned to the private audit ledger
```

Inbound events follow the reverse path through a quarantine gateway:

```text
GitHub webhook -> signature check -> replay check -> normalization
-> VTX envelope -> policy evaluation -> quarantined proposal
```

## Security Invariants

1. GitHub is never the canonical source of truth.
2. Every outbound operation is represented by a signed VTX envelope.
3. Envelopes bind the operation to a repository state, destination, branch, artifact digest, policy identifier, nonce, and expiration time.
4. Tokens are narrowly scoped, short lived, and unavailable to untrusted build steps.
5. Every accepted or rejected operation produces an append-only audit record.
6. Inbound webhooks can create proposals but cannot mutate the authoritative store.
7. Replay detection is mandatory for both outbound envelopes and inbound webhook events.
8. Hashes are computed before transport and verified after transport.
9. Verification failure is fail-closed.
10. External automation returns a receipt that is reconciled against the original envelope.

## Phase 0 Components

- `vtx/envelope.py`: deterministic envelope model and canonical serialization.
- `vtx/policy.py`: deny-by-default operation policy.
- `vtx/verify.py`: digest, freshness, scope, and replay verification.
- `vtx_envelope.schema.json`: machine-readable contract.
- `tests/test_vtx.py`: reference security behavior.

## Planned Components

- Hardware-backed Ed25519 signing.
- Append-only Merkle audit ledger.
- GitHub App adapter with installation-token minimization.
- Webhook quarantine service.
- Signed GitHub Actions receipts.
- Offline bundle export and import.
- SBOM and provenance attachment.
- Threshold authorization for high-risk publication operations.

## Operational Rule

A GitHub push, release, workflow dispatch, issue mutation, or webhook-derived proposal is valid only when its VTX envelope is accepted by local policy and its resulting receipt is reconciled into the private audit ledger.
