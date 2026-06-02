# Changelog

## 2026-06-02

### Added
- Added `scripts/enforce_federation_remote_write.py` to hard-fail remote-write when federation state is not ready.
- Added federation runtime pruning with machine-actionable status: `scripts/prune_federation_runtime.py`.
- Added stale packet detection for status/patch messages based on authoritative head and explicit blockers.
- Added `next_required_packets` output from `autonomous_vnext.federation_kernel` for direct recovery routing.
- Added archive behavior for stale runtime cleanup under `state/federation_runtime_archive`.
- Added test coverage for prune behavior in `tests/test_prune_federation_runtime.py`.
- Added desktop-safe status contract emitter (`scripts/write_desktop_federation_status.py`) with wrong-checkout blocker detection.
- Added tracked `.githooks/pre-push` with federation write gate and cleanup audit, plus hook installer script.

### Updated
- Federation assessment now separates `stale_surfaces` and `explicitly_blocked_surfaces` in kernel/state report paths.
- Documentation updates in `FederationInbox/README.md` and root `README.md` for the new cleanup flow.
- Local remote-write readiness now includes `next_required_packets` and explicit `readiness_blockers` in federation state reports.
