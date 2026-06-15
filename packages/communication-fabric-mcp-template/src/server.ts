import { createHash, randomUUID } from "node:crypto";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const sensitivityLevels = ["public", "private", "legal", "medical", "financial", "credential", "biometric", "privileged", "sealed"] as const;
const actionModes = ["draft_only", "requires_approval", "allow_autonomous"] as const;

type Sensitivity = (typeof sensitivityLevels)[number];
type ActionMode = (typeof actionModes)[number];

type AuditEvent = {
  eventId: string;
  timestamp: string;
  actor: string;
  action: string;
  mode: ActionMode;
  sensitivity: Sensitivity;
  inputHash: string;
  decision: "drafted" | "approved" | "denied" | "registered";
  provenance: string[];
};

const auditLedger: AuditEvent[] = [];
const consentGrants = new Map<string, { scope: string; expiresAt?: string }>();

function hashPayload(payload: unknown): string {
  return createHash("sha256").update(JSON.stringify(payload)).digest("hex");
}

function audit(event: Omit<AuditEvent, "eventId" | "timestamp">): AuditEvent {
  const record: AuditEvent = { eventId: randomUUID(), timestamp: new Date().toISOString(), ...event };
  auditLedger.push(record);
  return record;
}

function decideMode(sensitivity: Sensitivity, requestedMode: ActionMode): ActionMode {
  if (["legal", "medical", "financial", "credential", "biometric", "privileged", "sealed"].includes(sensitivity)) {
    return "requires_approval";
  }
  return requestedMode;
}

const server = new McpServer({ name: "communication-fabric-mcp-template", version: "0.2.0" });

server.resource("current-policy", "fabric://policies/current", async () => ({
  contents: [{
    uri: "fabric://policies/current",
    mimeType: "application/json",
    text: JSON.stringify({
      defaultMode: "draft_only",
      sensitivityLevels,
      rule: "No external send, publish, purchase, destructive action, or privileged data access without explicit consent and audit evidence."
    }, null, 2)
  }]
}));

server.resource("audit-ledger", "fabric://audit/recent", async () => ({
  contents: [{ uri: "fabric://audit/recent", mimeType: "application/json", text: JSON.stringify(auditLedger.slice(-25), null, 2) }]
}));

server.tool("request_user_consent", {
  scope: z.string(),
  reason: z.string(),
  expiresAt: z.string().optional()
}, async ({ scope, reason, expiresAt }) => {
  const consentId = randomUUID();
  consentGrants.set(consentId, { scope, expiresAt });
  const record = audit({ actor: "human", action: `consent:${scope}`, mode: "requires_approval", sensitivity: "private", inputHash: hashPayload({ scope, reason, expiresAt }), decision: "approved", provenance: [reason] });
  return { content: [{ type: "text", text: JSON.stringify({ consentId, scope, expiresAt, auditEvent: record.eventId }, null, 2) }] };
});

server.tool("draft_communication", {
  recipient: z.string(),
  channel: z.enum(["email", "calendar_invite", "github_issue", "legal_packet", "research_note", "agent_task", "sms_bridge", "local_notification", "institutional_submission"]),
  purpose: z.string(),
  sourceCitations: z.array(z.string()).default([]),
  sensitivity: z.enum(sensitivityLevels).default("private"),
  requestedMode: z.enum(actionModes).default("draft_only")
}, async ({ recipient, channel, purpose, sourceCitations, sensitivity, requestedMode }) => {
  const mode = decideMode(sensitivity, requestedMode);
  const record = audit({ actor: "agent", action: `draft_communication:${channel}`, mode, sensitivity, inputHash: hashPayload({ recipient, channel, purpose, sourceCitations }), decision: "drafted", provenance: sourceCitations });
  return { content: [{ type: "text", text: JSON.stringify({ recipient, channel, mode, subject: `Follow-up: ${purpose.slice(0, 64)}`, body: `Draft only. Purpose: ${purpose}\n\nSources:\n${sourceCitations.join("\n") || "No sources attached yet."}`, approvalRequired: mode !== "allow_autonomous", auditEvent: record.eventId }, null, 2) }] };
});

server.tool("hash_and_register_file", {
  fileName: z.string(),
  content: z.string(),
  sensitivity: z.enum(sensitivityLevels).default("private"),
  source: z.string().default("user_supplied")
}, async ({ fileName, content, sensitivity, source }) => {
  const digest = hashPayload({ fileName, content });
  const record = audit({ actor: "agent", action: "hash_and_register_file", mode: "draft_only", sensitivity, inputHash: digest, decision: "registered", provenance: [source] });
  return { content: [{ type: "text", text: JSON.stringify({ fileName, sha256: digest, sensitivity, source, auditEvent: record.eventId }, null, 2) }] };
});

server.prompt("secure_message_drafter", {
  recipient: z.string(),
  purpose: z.string(),
  sensitivity: z.enum(sensitivityLevels).default("private")
}, ({ recipient, purpose, sensitivity }) => ({
  messages: [{ role: "user", content: { type: "text", text: `Draft a ${sensitivity} message to ${recipient} for this purpose: ${purpose}. Do not send it. Include required approvals, citations, and attachments.` } }]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
