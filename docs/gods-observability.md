# Gods Observability Channel

`Gods` is the portfolio operations channel for synchronized Pre-Review Tasks and release-readiness telemetry.

## Jira

The scheduled control plane converts medium-or-higher repository-health findings into deduplicated Jira tasks. Configure these repository secrets:

- `JIRA_BASE_URL`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`
- `JIRA_PROJECT_KEY`

Optional repository variable: `JIRA_ISSUE_TYPE` (default: `Task`). Jira synchronization is skipped when credentials are absent and never runs on pull-request code.

## Prometheus

The exporter writes OpenMetrics-compatible text to `artifacts/gods/portfolio.prom`. Configure `PROMETHEUS_PUSHGATEWAY_URL` to push the metrics after a trusted scheduled scan; otherwise the metrics remain a retained workflow artifact suitable for a textfile collector.

Exported metrics include findings by severity and repository, scan errors, and computed release readiness. Commit SHAs, issue numbers, report text, URLs, secrets, and repository contents are excluded.

## Release boundary

The integration does not merge, approve, publish, deploy, or close Pre-Review Tasks. Release readiness remains false when high-severity findings or scan errors exist, and all candidate changes require exact-head CI before review.
