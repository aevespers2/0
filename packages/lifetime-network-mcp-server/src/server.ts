import { createHash, randomUUID } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const __dirname = dirname(fileURLToPath(import.meta.url));
const insightsPath = join(__dirname, "..", "data", "platform_insights.json");
const sensitivities = ["public", "private", "legal", "medical", "financial", "credential", "biometric", "privileged", "sealed"] as const;
const entityTypes = ["person", "organization", "device", "project", "show", "movie", "clip", "schedule_event", "provider", "app_platform", "rights_window", "document", "message", "theory", "event", "memory", "evidence", "repository", "agent", "institution"] as const;

type Sensitivity = (typeof sensitivities)[number];
type EntityType = (typeof entityTypes)[number];

type Entity = { id: string; type: EntityType; label: string; summary: string; sensitivity: Sensitivity; source: string };
type Edge = { from: string; to: string; relation: string; source: string };
type AuditEvent = { eventId: string; timestamp: string; action: string; sensitivity: Sensitivity; decision: string; inputHash: string; provenance: string[] };

const graph: { entities: Entity[]; edges: Edge[] } = {
  entities: [
    { id: "org-lifetime", type: "organization", label: "Lifetime", summary: "Public television and digital entertainment brand; prototype has no official affiliation.", sensitivity: "public", source: "https://www.mylifetime.com/" },
    { id: "platform-lifetime-app", type: "app_platform", label: "Lifetime App", summary: "Publicly described app experience across mobile, tablet, connected-TV, casting, and smart-TV devices.", sensitivity: "public", source: "https://www.mylifetime.com/apps" },
    { id: "workflow-editorial-brief", type: "project", label: "Editorial brief workflow", summary: "Draft-only workflow for evidence-backed digital-platform communication.", sensitivity: "private", source: "local_design" } as Entity
  ],
  edges: [
    { from: "org-lifetime", to: "platform-lifetime-app", relation: "communicates_through", source: "public_platform_research" },
    { from: "workflow-editorial-brief", to: "org-lifetime", relation: "requires_consent_from", source: "local_policy" }
  ]
};

const auditLedger: AuditEvent[] = [];
const consentGrants = new Map<string, { scope: string; reason: string; expiresAt?: string }>();

function hashPayload(payload: unknown): string {
  return createHash("sha256").update(JSON.stringify(payload)).digest("hex");
}

function audit(action: string, sensitivity: Sensitivity, decision: string, payload: unknown, provenance: string[]): AuditEvent {
  const record = { eventId: randomUUID(), timestamp: new Date().toISOString(), action, sensitivity, decision, inputHash: hashPayload(payload), provenance };
  auditLedger.push(record);
  return record;
}

function consentRequired(sensitivity: Sensitivity): boolean {
  return sensitivity !== "public";
}

async function loadInsights() {
  return JSON.parse(await readFile(insightsPath, "utf8"));
}

const server = new McpServer({ name: "lifetime-network-communication-fabric-mcp", version: "0.2.0" });

server.resource("platform-insights", "lifetime://platform/insights", async () => ({
  contents: [{ uri: "lifetime://platform/insights", mimeType: "application/json", text: JSON.stringify(await loadInsights(), null, 2) }]
}));

server.resource("current-policy", "lifetime://policies/current", async () => ({
  contents: [{
    uri: "lifetime://policies/current",
    mimeType: "application/json",
    text: JSON.stringify({
      defaultExternalAction: "draft_only",
      sensitivities,
      consentRule: "External sends, provider/rights-sensitive actions, privileged data access, and public claims require explicit human approval.",
      entitlementRule: "Never bypass authentication, TV-provider verification, geofencing, rights windows, or content entitlements."
    }, null, 2)
  }]
}));

server.resource("recent-audit", "lifetime://audit/recent", async () => ({
  contents: [{ uri: "lifetime://audit/recent", mimeType: "application/json", text: JSON.stringify(auditLedger.slice(-50), null, 2) }]
}));

server.tool("search_lifetime_graph", {
  query: z.string(),
  entityType: z.enum(entityTypes).optional()
}, async ({ query, entityType }) => {
  const normalized = query.toLowerCase();
  const entities = graph.entities.filter((entity) => (!entityType || entity.type === entityType) && `${entity.label} ${entity.summary}`.toLowerCase().includes(normalized));
  const edgeSet = graph.edges.filter((edge) => entities.some((entity) => entity.id === edge.from || entity.id === edge.to));
  const record = audit("search_lifetime_graph", "private", "read", { query, entityType }, ["local_graph"]);
  return { content: [{ type: "text", text: JSON.stringify({ entities, edges: edgeSet, auditEvent: record.eventId }, null, 2) }] };
});

server.tool("summarize_relationship_network", {
  entityId: z.string(),
  includeEvidence: z.boolean().default(true)
}, async ({ entityId, includeEvidence }) => {
  const entity = graph.entities.find((item) => item.id === entityId);
  const edges = graph.edges.filter((edge) => edge.from === entityId || edge.to === entityId);
  const record = audit("summarize_relationship_network", entity?.sensitivity ?? "private", "drafted", { entityId, includeEvidence }, edges.map((edge) => edge.source));
  return { content: [{ type: "text", text: JSON.stringify({ entity, relationships: edges, evidenceRequired: includeEvidence, auditEvent: record.eventId }, null, 2) }] };
});

server.tool("classify_document_sensitivity", {
  title: z.string(),
  text: z.string(),
  source: z.string().default("user_supplied")
}, async ({ title, text, source }) => {
  const lowered = `${title} ${text}`.toLowerCase();
  const sensitivity: Sensitivity = lowered.includes("password") || lowered.includes("token") ? "credential" : lowered.includes("contract") || lowered.includes("rights") || lowered.includes("legal") ? "legal" : lowered.includes("budget") || lowered.includes("invoice") ? "financial" : lowered.includes("medical") ? "medical" : "private";
  const record = audit("classify_document_sensitivity", sensitivity, "classified", { title, text }, [source]);
  return { content: [{ type: "text", text: JSON.stringify({ title, sensitivity, consentRequired: consentRequired(sensitivity), auditEvent: record.eventId }, null, 2) }] };
});

server.tool("request_user_consent", {
  scope: z.string(),
  reason: z.string(),
  expiresAt: z.string().optional()
}, async ({ scope, reason, expiresAt }) => {
  const consentId = randomUUID();
  consentGrants.set(consentId, { scope, reason, expiresAt });
  const record = audit("request_user_consent", "private", "approved_by_user", { scope, reason, expiresAt }, [reason]);
  return { content: [{ type: "text", text: JSON.stringify({ consentId, scope, expiresAt, auditEvent: record.eventId }, null, 2) }] };
});

server.tool("draft_communication", {
  recipient: z.string(),
  channel: z.enum(["email", "calendar_invite", "github_issue", "legal_packet", "research_note", "agent_task", "sms_bridge", "local_notification", "institutional_submission", "app_feedback_packet"]),
  purpose: z.string(),
  sensitivity: z.enum(sensitivities).default("private"),
  sourceCitations: z.array(z.string()).default([]),
  consentId: z.string().optional()
}, async ({ recipient, channel, purpose, sensitivity, sourceCitations, consentId }) => {
  const approved = consentId ? consentGrants.has(consentId) : false;
  const mustApprove = consentRequired(sensitivity) || channel !== "research_note";
  const decision = mustApprove && !approved ? "draft_only_pending_approval" : "approved_draft_ready";
  const record = audit("draft_communication", sensitivity, decision, { recipient, channel, purpose, sourceCitations, consentId }, sourceCitations);
  return { content: [{ type: "text", text: JSON.stringify({ recipient, channel, subject: `Lifetime Network MCP follow-up: ${purpose.slice(0, 72)}`, body: `Draft only unless approved.\n\nPurpose: ${purpose}\n\nEvidence / sources:\n${sourceCitations.join("\n") || "Attach sources before sending."}`, requiresApproval: decision === "draft_only_pending_approval", auditEvent: record.eventId }, null, 2) }] };
});

server.tool("create_evidence_packet", {
  claim: z.string(),
  sources: z.array(z.string()).min(1),
  sensitivity: z.enum(sensitivities).default("private")
}, async ({ claim, sources, sensitivity }) => {
  const packetId = randomUUID();
  const record = audit("create_evidence_packet", sensitivity, "registered", { claim, sources }, sources);
  return { content: [{ type: "text", text: JSON.stringify({ packetId, claim, sources, sensitivity, sha256: hashPayload({ claim, sources }), auditEvent: record.eventId }, null, 2) }] };
});

server.tool("generate_project_timeline", {
  projectName: z.string(),
  events: z.array(z.object({ date: z.string(), description: z.string(), source: z.string().optional() }))
}, async ({ projectName, events }) => {
  const sorted = [...events].sort((a, b) => a.date.localeCompare(b.date));
  const record = audit("generate_project_timeline", "private", "drafted", { projectName, events }, sorted.flatMap((event) => event.source ? [event.source] : []));
  return { content: [{ type: "text", text: JSON.stringify({ projectName, timeline: sorted, auditEvent: record.eventId }, null, 2) }] };
});

server.prompt("secure_message_drafter", {
  recipient: z.string(),
  purpose: z.string()
}, ({ recipient, purpose }) => ({
  messages: [{ role: "user", content: { type: "text", text: `Draft a respectful, unofficial, evidence-backed message to ${recipient} about ${purpose}. Do not claim affiliation. Do not send. Include source links and approval checklist.` } }]
}));

server.prompt("agent_handoff_summary", {
  project: z.string(),
  nextAction: z.string()
}, ({ project, nextAction }) => ({
  messages: [{ role: "user", content: { type: "text", text: `Summarize current state for ${project}, including evidence packets, consent status, open risks, and next action: ${nextAction}.` } }]
}));

server.prompt("project_state_reconstructor", {
  project: z.string()
}, ({ project }) => ({
  messages: [{ role: "user", content: { type: "text", text: `Reconstruct the ${project} state from graph entities, continuity memories, audit events, and evidence packets. Separate verified facts from hypotheses.` } }]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
