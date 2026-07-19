# Gods and Clan Pre-Review Tasks

## Gods — Jira and Prometheus

- [x] Define `Gods` as the Jira and Prometheus operations channel.
- [x] Add deduplicated Jira task synchronization for medium-or-higher repository findings.
- [x] Add bounded Prometheus exposition without commit SHAs, issue numbers, secrets, URLs, or repository contents.
- [x] Add focused unit tests for channel configuration, Jira dry-run behavior, and metrics output.
- [ ] Correct workflow secret-presence gating so scheduled Jira and Pushgateway steps execute only when configured.
- [ ] Pin all third-party Actions to reviewed immutable commit SHAs.
- [ ] Pass fresh exact-head CI and retain the workflow artifact.
- [ ] Configure Jira and Pushgateway secrets before trusted scheduled execution.

## Clan — Terraform

- [x] Set the clan flag to `ralbane`.
- [x] Define `Clan` as the Terraform tooling channel.
- [x] Require exact-head validation, plan-only defaults, provider lockfiles, state locking, and human approval for apply.
- [x] Add a Terraform Pre-Review Gate that fails when Terraform exists without `.terraform.lock.hcl`.
- [ ] Add Terraform CLI installation pinned to an approved version before executing `fmt`, `init -backend=false`, `validate`, and speculative `plan`.
- [ ] Add backend, drift, sensitive-output, and state-file exclusion tests.
- [ ] Pass fresh exact-head CI before formal review.

No item authorizes automatic merge, Terraform apply, release, publication, or deployment.
