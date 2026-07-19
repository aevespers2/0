# Clan Terraform Tooling

The Terraform operations channel is `Clan`, and its clan flag is `ralbane`.

## Operating boundary

- Pull requests run formatting, validation, static checks, and speculative plans only.
- `terraform apply` requires explicit human approval against the exact reviewed head.
- Remote state, locking, provider lockfiles, drift detection, and retained plan artifacts are required.
- Repository commits must never contain Terraform state, plaintext secrets, provider credentials, or sensitive outputs.
- Force unlock, automatic apply, and unreviewed provider upgrades are prohibited.

## Channel separation

- `Gods`: Jira synchronization, Prometheus metrics, portfolio health, and release-readiness dispatch.
- `Clan`: Terraform formatting, validation, planning, drift review, state-backend checks, and approved infrastructure application.

Every Terraform finding becomes a Pre-Review Task before formal review, and no infrastructure candidate may advance without exact-head evidence.
