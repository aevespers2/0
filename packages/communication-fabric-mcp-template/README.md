# Communication Fabric MCP Template

A public-ready advanced Model Context Protocol server template for a secure continuity layer between people, agents, devices, documents, memories, projects, evidence, codebases, and institutions.

## Design principles

- MCP servers expose tools, resources, and prompts; this template adds policy, consent, provenance, and continuity around those primitives.
- No tool runs merely because it exists. Every tool has identity, scope, sensitivity, consent, and audit metadata.
- Important external actions follow `observe → classify → retrieve → reason → propose → request consent → execute → audit → remember`.
- High-risk channels default to draft-only until a human approves the route.

## Core modules

- Identity Graph: people, organizations, devices, projects, documents, events, evidence, agents, and institutions.
- Continuity Memory: versioned facts, preferences, hypotheses, legal claims, technical artifacts, evidence, and allegations.
- Communication Router: drafts and routes emails, calendar invites, GitHub issues, research notes, packets, and agent tasks.
- Trust + Consent Kernel: scope checks, approval gates, revocation, and sensitivity classification.
- Audit + Provenance Ledger: append-only event records that can later be backed by a Merkle log.

## Storage upgrade path

Start in-memory for demos, then back the same interfaces with PostgreSQL, Kuzu/Neo4j, pgvector/Qdrant, S3/MinIO, Redis/NATS, and OpenTelemetry.
