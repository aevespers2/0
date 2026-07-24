# Security and authority

## Security objective

Autonomous vNext should make bounded engineering safer and more reproducible while denying hidden or excessive authority. Security is enforced through explicit mission scope, least privilege, exact-head evidence, deterministic contracts, human-visible proposals, independent verification, revocation, and rollback.

## Protected assets

- repository source and protected branches;
- credentials, tokens, signing keys, and secret configuration;
- action records, audit logs, workflow artifacts, and provenance;
- canonical contracts, state, and migration history;
- release and deployment channels;
- infrastructure state and Terraform backends;
- private repository, issue, and portfolio metadata;
- local files, conversations, memory, and sensitive evidence;
- emergency-stop and capability-revocation controls.

## Authority matrix

| Action | Default | Required before permission |
|---|---|---|
| Read approved local/public source | allow within mission | source identity and data classification |
| Generate plans, docs, tests, and local reports | allow within scoped workspace | mission, path policy, output boundary, rollback |
| Modify source on an isolated branch | deny unless mission permits | scoped branch/path grant and clean rollback |
| Apply a federation patch | deny by default | authoritative baseline, verified patch, clean worktree, explicit apply action |
| Read private repositories or issues | deny by default | least-privilege credential, repository opt-in, audit, expiry |
| Write issues or pull requests | deny by default | operation allowlist, idempotency, human-visible result, revocation |
| Merge or write protected branches | deny | repository-specific approval and branch protections |
| Publish package or release | deny | signing, provenance, evidence, rollback, explicit release approval |
| Deploy or Terraform apply | deny | approved plan, environment identity, human approval, recovery test |
| Change policy or capability issuer | deny | independent governance review and emergency-stop verification |

## Credential model

A secure credential gateway should:

- keep raw credentials outside agent context and repository files;
- issue short-lived, purpose-bound capabilities;
- bind repository, branch, path, operation, audience, and expiration;
- deny wildcard administration, secrets, workflow editing, deletion, and force push unless separately approved;
- produce redacted audit records;
- support immediate revocation and tested disablement;
- prevent a requester from approving its own capability expansion;
- distinguish read, proposal, merge, release, and deployment identities.

## Input and proposal threats

Treat repository content, issues, documents, model output, federation packets, and external APIs as untrusted inputs. Defenses include:

- schema validation and bounded sizes;
- canonical serialization and digest verification;
- stale-baseline, nonce, expiration, and replay checks;
- explicit destination and schema ownership;
- path normalization and traversal rejection;
- command allowlists and argument validation;
- output encoding and secret redaction;
- quarantine for unknown or conflicting contracts;
- independent verification before canonical adoption.

## Supply-chain controls

- pin workflow actions and document their source revisions;
- use lockfiles or record their absence as a release blocker;
- separate documentation dependencies from runtime installation where practical;
- generate SBOM and dependency records for release candidates;
- verify package provenance, signatures, and checksums;
- prevent build hooks from running during incident-safe evidence collection unless explicitly required and reviewed;
- retain exact environment and tool versions with validation artifacts.

## Network and external systems

Network access is not implied by a mission. Every external destination and method should be allowlisted. Remote Web APIs, Jira, GitHub, package registries, model providers, and infrastructure backends require independent authentication, transport security, rate limits, retries, timeouts, and data-classification review.

## Human approval boundary

Human approval remains mandatory for:

- credentials and capability expansion;
- merges to protected/canonical branches;
- releases, signing, publication, and deployment;
- Terraform apply or destructive infrastructure changes;
- financial or payment commitments;
- publication of sensitive or privacy-relevant evidence;
- emergency exceptions and incident reactivation;
- self-modification of the authority, policy, audit, or emergency-stop layer.

Narrow action classes may later be delegated only after their contracts, tests, evidence, incident behavior, and rollback have been accepted.

## Security evidence

A security-ready candidate includes:

- threat model and trust-boundary diagram;
- permission and capability matrix;
- secrets and workflow-permission scan;
- dependency and action provenance;
- negative tests for path, command, replay, stale state, malformed input, and excessive scope;
- credential issuance/revocation drill where applicable;
- incident and rollback exercise;
- exact-head workflow evidence and artifact hashes;
- explicit residual risks and owner approvals.
