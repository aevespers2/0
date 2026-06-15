# Lifetime Network Television Platform Research

This research brief informs the tailored `lifetime-network-mcp-server` design. It uses public sources only and treats the resulting server as an unofficial prototype.

## Public platform observations

- A+E Global Media describes itself as a global media and entertainment portfolio, which means a credible MCP prototype should support portfolio-level coordination rather than a single-page demo.
- A+E Global Media Digital includes watch apps, games, FAST channels, AVOD, and SVOD products such as Crime 360, Lifetime Movie Club, and HISTORY Vault; the MCP design therefore needs digital-product, app, streaming, and cross-platform routing concepts.
- Lifetime's public site emphasizes full episodes, original movies, schedules, and online viewing, so a tailored server should model shows, movies, clips, schedules, platform availability, and editorial support workflows.
- Lifetime's app page lists mobile, tablet, connected-TV, casting, and smart-TV distribution, so the server should treat devices/platforms as first-class identity-graph nodes.
- Lifetime support says full-catalog access requires verification through a supported TV provider while some unlocked content is available without sign-in; the server must model access constraints and avoid bypassing entitlements.
- A+E producer technical requirements describe distribution across VOD, TV Everywhere, home video, download-to-own, and streaming outlets; the server should separate editorial, rights, delivery, QC, and evidence/asset provenance workflows.

## MCP and security observations

- MCP is a standard for connecting AI applications to external systems through tools, resources, prompts, and context, so the implementation should expose those primitives clearly.
- MCP tools allow models to interact with external systems and include unique names plus metadata schemas; every tool in this prototype therefore has typed inputs and explicit policy framing.
- Recent MCP security guidance and research emphasizes server trust, dynamic tool admission, prompt/tool injection, runtime monitoring, and the need for controls beyond static API wrappers. The design therefore defaults to draft-only behavior, consent gates, sensitivity classes, and append-only audit records.

## Tailored implications

The Lifetime-focused server should not be a numeric network catalog. It should be a communication fabric for Lifetime's television/digital ecosystem:

1. Identity graph nodes for people, editors, devices, shows, movies, clips, schedules, providers, apps, rights windows, evidence packets, repositories, and agents.
2. Continuity memory that distinguishes verified public facts, editorial assumptions, hypotheses, rights-sensitive notes, and unverified allegations.
3. Communication routing that drafts emails, editorial briefs, app-store issue reports, calendar invites, GitHub issues, legal/rights packets, and internal agent tasks without sending anything automatically.
4. Trust and consent controls for public/private/legal/financial/credential/privileged/sealed information.
5. Provenance records for source URLs, files, hashes, approvals, and final human decisions.

## Source links

- https://www.aenetworks.com/
- https://aenetworks.com/who-we-are/
- https://www.mylifetime.com/
- https://www.mylifetime.com/apps
- https://support.mylifetime.com/hc/en-us/articles/1500004781782-I-don-t-have-a-TV-package-Can-I-subscribe-directly-to-Lifetime
- https://producersuite.aenetworks.com/docs/ProductionDeliveryTechnicalRequirements.pdf
- https://modelcontextprotocol.io/docs/getting-started/intro
- https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- https://arxiv.org/html/2511.20920v1
