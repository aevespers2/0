# Iris-derived local verifier contract

## Status and authority

This document defines a **non-operational, synthetic-test-only contract candidate** for issue #15. It does not authorize biometric collection, enrollment, authentication, capability issuance, device control, network access, cloud processing, storage of raw captures, or canonical identity decisions.

Repository `0` is limited to candidate local preprocessing, quality/liveness assessment, protected-template derivation, and non-authoritative match proposals. Repository `1` remains the candidate authority for enrollment disposition, revocation, replacement, recovery, and any later capability decision. A neutral contract steward is still required for shared schemas and conformance fixtures.

A matching protected identifier is evidence only. It is not identity proof, approval, enrollment, authentication, authorization, or canonical state.

## Bounded pipeline

The proposed conceptual pipeline is:

`authorized local capture → quality/liveness gate → segmentation and normalization → masked feature representation → error-tolerant reconstruction → domain-separated keyed derivation → revocable protected identifier → non-authoritative proposal`

Only the final derivation contract and synthetic conformance surface are implemented here. Capture, liveness, segmentation, normalization, feature extraction, fuzzy extraction, helper-data construction, device integration, and enrollment are intentionally absent.

## Derivation

The candidate output is:

`HMAC-SHA-256(key, domain || 0x00 || canonical(profile) || 0x00 || reconstructed_secret)`

The profile fixes the domain, extractor version, transform, key slot identifier, one-eye subject scope, helper-data size ceiling, memory-only raw-capture policy, and output algorithm. Canonical JSON uses UTF-8, lexicographically sorted keys, compact separators, and rejects duplicate keys and non-finite numbers.

Production key material must never be committed, embedded in fixtures, logged, uploaded as an artifact, or derived from biometric material. The committed vector generator uses clearly labeled deterministic **public synthetic bytes** solely to prove cross-runtime conformance. Those bytes are not production secrets and must never be accepted by a runtime profile.

Changing the key, domain, profile identifier, extractor version, or transform must produce a different protected identifier. Revocation and replacement remain external authority decisions.

## Record separation

The schema separates:

- derivation profiles;
- verification attempts;
- non-authoritative match proposals;
- revocation records;
- recovery references.

Capture records, liveness/quality assessments, normalized features, helper data, enrollment dispositions, corrections, and recovery checkpoints require independent identities and ownership even when later schemas are added. Verification attempts carry an explicit positive profile generation so stale or future generations cannot be inferred from a mutable profile name.

## Privacy invariants

The contract and tests fail closed on record fields that could carry:

- raw eye images;
- iris codes or unprotected feature vectors;
- reconstructed secrets;
- live biometric samples;
- HMAC keys or other key material.

No such material may enter Git, CI artifacts, logs, crash reports, telemetry, Pages, issues, or pull requests. Raw captures are memory-only by contract and must be deleted immediately after any separately authorized bounded processing. Left and right eyes remain separate subjects.

Only synthetic, non-biometric fixtures are permitted in this repository. Any real-data evaluation requires a separately approved private and offline protocol, named data controller, deletion proof, retention limit, access controls, incident procedure, and independent legal and privacy review.

## Fail-closed cases

A future implementation must reject at least:

- unknown or unsupported profiles;
- low-quality, occluded, or liveness-rejected captures;
- mirrored or wrong-eye inputs;
- wrong-device or wrong-enrollment-generation records;
- stale, replayed, duplicate, malformed, or corrupted attempts;
- changed or oversized helper data;
- revoked profiles, identifiers, or generations;
- non-canonical records, duplicate JSON keys, and non-finite values;
- missing evidence, missing authority, or ambiguous disposition.

The current code validates derivation profiles, deterministic keyed derivation, strict JSON, privacy-safe record shape, schema shape, synthetic golden vectors, and a bounded synthetic attempt-context screen. It does not claim coverage of capture, liveness, matching, biometric-performance, or operational state-management failures.

## Synthetic hostile-context corpus

`fixtures/iris-verifier/hostile-context-vectors.json` is a public synthetic corpus with byte SHA-256 `677a66f65bde813e122c6493b5421a06dadf867cfa029a05f3bc610564f50006`. It contains no capture, biometric template, reconstructed secret, helper-data bytes, production key, or live identity material.

The corpus fixes one baseline attempt and context, then requires deterministic outcomes for:

- a valid baseline;
- wrong-eye and wrong-device attempts;
- a stale profile generation;
- an already-seen attempt identifier;
- a changed helper-data digest;
- a revoked profile;
- an attempt against a replaced profile;
- an incomplete recovery state;
- a completed recovery using the explicit replacement profile and generation.

The screen validates exact record fields, normalized identifiers, lowercase SHA-256 digests, bounded age, profile generation, subject, eye, device, helper-data reference, replay state, revocation state, replacement state, and recovery state before a synthetic proposal may be considered. Acceptance remains evidence only and creates no enrollment, authentication, capability, device-control, or canonical-state authority.

## Evaluation requirements

Before any operational proposal, independently record and review:

- false-match and false-non-match rates;
- failure-to-enroll and failure-to-acquire rates;
- quality rejection rate and reconstruction margin;
- capture-to-capture stability;
- diversity, unlinkability, renewability, and cross-database correlation resistance;
- helper-data leakage assumptions;
- revocation and replacement success;
- demographic and environmental performance differences;
- device, dependency, and platform reproducibility.

Thresholds remain proposed until approved by independent technical, privacy, legal, and human authorities. Standards references are design inputs only and do not confer compliance.

## Repository `0` to Repository `1` boundary

Repository `0` may emit a non-authoritative proposal containing only normalized identifiers, digests, profile references, timestamps, quality/liveness disposition references, and evidence references. It must not emit raw captures, unprotected features, reconstructed secrets, helper-data bytes, or keys.

Repository `1` must independently validate identity namespaces, profile generation, revocation state, replay state, device/workspace binding, evidence completeness, and policy before recording any disposition. No Repository `0` match result can directly create enrollment, authentication, capability, or canonical identity state.

## Rotation, rollback, and recovery

Rotation creates a new profile generation with a new transform and/or key. Old profile generations and helper-data references must be explicitly revoked; they are never silently reactivated. Recovery references bind prior and replacement profiles to an independently owned checkpoint digest without copying biometric material.

Rollback of this candidate means closing the pull request or reverting its files. It does not require key rotation because no production key is introduced. If any prohibited material is ever found in repository history or artifacts, stop immediately, freeze publication, revoke affected credentials and profile generations, preserve incident evidence, and follow an approved removal and notification procedure without rewriting history unless separately authorized.

## Current deliverables

This candidate provides:

- `contracts/iris-derived-verifier-v0.schema.json`;
- `iris_verifier_contract` strict parsing, profile validation, privacy guard, canonicalization, keyed derivation, and synthetic attempt-context screening primitives;
- a synthetic fixture generator and committed golden vector;
- the hostile-context corpus for wrong-eye, wrong-device, stale, replayed, corrupted, revoked, replaced, and recovery cases;
- focused regression tests;
- a read-only exact-head workflow with retained checksummed evidence.

## Remaining blockers

Operational work remains blocked on approved capture hardware and profiles, liveness and quality algorithms, fuzzy-extractor design and leakage analysis, protected helper-data construction, independent implementations, performance evaluation, device identity, key custody, signer policy, durable revocation/replay state, atomic consume-and-record semantics, privacy and legal approval, incident ownership, recovery drills, and explicit human authorization.
