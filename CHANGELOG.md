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
- Added mobile status writer (`scripts/write_mobile_federation_status.py`) for user-facing routine packets.
- Added Safari patch-first production workflow (`scripts/safari_patch_workflow.py`) for deterministic patch bundle export.
- Added bridge signal emitter (`scripts/emit_bridge_signal.py`) for planning/coordination bridge handoff.
- Added regression coverage for mobile status writer, Safari patch workflow, and bridge signal output.
- Added `FederationDispatch/` plus `scripts/write_federation_dispatch.py` to turn kernel-required packets into per-surface routing instructions.
- Added `scripts/run_federation_routine.py` to refresh local/desktop/mobile status, bridge signal, state report, and dispatch in one command.
- Added self-contained `status_template` and `handoff_text` fields to dispatch packets for cloud/advisory surfaces.
- Preserved message `capabilities` and `constraints` through the federation kernel.
- Added `FederationRelay/` and `scripts/record_federation_contact.py` for UI/browser/app handoff evidence.
- Added `scripts/stage_safari_dispatch.py` to refresh Safari composer handoffs from the current dispatch and record relay evidence.
- Added `scripts/watch_safari_dispatch_send.py` to poll Safari sendability and optionally send staged dispatches.
- Added `scripts/write_federation_relay_summary.py` for compact relay-state readouts.
- Added `scripts/run_safari_relay_retry.py` for bounded Safari dispatch staging/watch retry loops.
- Added `scripts/extract_safari_ack.py` to parse visible Safari acknowledgments and optionally transcribe valid federation packets.
- Added `scripts/run_safari_sync_cycle.py` to refresh, stage, watch, extract, and summarize Safari federation state in one command.
- Added `scripts/probe_desktop_codex_app.py` to record live macOS Codex desktop app contact evidence.

### Updated
- Federation assessment now separates `stale_surfaces` and `explicitly_blocked_surfaces` in kernel/state report paths.
- Documentation updates in `FederationInbox/README.md` and root `README.md` for the new cleanup flow.
- Local remote-write readiness now includes `next_required_packets` and explicit `readiness_blockers` in federation state reports.
- Added explicit protocol guidance for Safari/mobile/bridge status cycles in `CODEX_FEDERATION_STATUS.md`.
- Documented dispatch generation and local federation routine execution across README/status docs.
- Documented dispatch fallback behavior for surfaces that cannot run local helper scripts.
- Clarified that `*-assignment.json` handoff files are ignored by the kernel and patch-only Safari behavior is a constraint, not a blocker.
- Documented relay/contact logging for Safari and Desktop handoff attempts.
- Documented Safari acknowledgment extraction as a relay step before collecting `FederationInbox/safari/status.json`.
- Relay summaries now preserve actionable next steps when Safari acknowledgment extraction observes no valid packet.
- Relay summaries now select the latest contact for the dispatched surface so Desktop probes do not overwrite Safari relay state.
- Contact recording now writes per-surface latest relay files under `reports/federation_contact_latest/`.
- Added `scripts/write_federation_contact_report.py` for Safari/Desktop relay-contact freshness audits.
- Added `scripts/write_federation_dashboard.py` for compact federation handoff summaries.
- Safari sync cycles now refresh the relay summary, contact report, and federation dashboard together.
