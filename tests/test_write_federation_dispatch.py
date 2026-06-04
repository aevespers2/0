from __future__ import annotations

import json

from scripts.write_federation_dispatch import build_dispatch, command_for, parallel_work_allocation, write_dispatch


def test_parallel_work_allocation_defines_surface_roles() -> None:
    payload = parallel_work_allocation("abc123")

    assert payload["schema"] == "codex_parallel_work_allocation.v1"
    assert payload["authoritative_head"] == "abc123"
    assert payload["surfaces"]["local_cli"]["role"] == "authoritative_integrator"
    assert payload["surfaces"]["safari_cloud"]["handoff_type"] == "patch_proposal"
    assert "patch_only_no_direct_push" in payload["surfaces"]["safari_cloud"]["constraints"]
    assert payload["surfaces"]["chatgpt_bridge"]["role"] == "planning_and_dispatch_coordinator"
    assert "local_cli remains" in payload["coordination_rule"]


def test_build_dispatch_translates_required_packets(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        "scripts.write_federation_dispatch.build_state_report",
        lambda repo, inbox, mirror_manifest, authoritative_head: {
            "ready_for_remote_write": False,
            "readiness_blockers": ("required federation packets pending",),
            "next_required_packets": (
                {
                    "agent": "safari_cloud",
                    "packet_type": "status_refresh",
                    "priority": "required",
                    "details": "status is stale",
                    "expected_path": "FederationInbox/safari/status.json",
                },
                {
                    "agent": "desktop_app",
                    "packet_type": "status_unblock",
                    "priority": "required",
                    "details": "wrong checkout",
                    "expected_path": "FederationInbox/desktop/status.json",
                },
            ),
        },
    )

    payload = build_dispatch(tmp_path, tmp_path / "FederationInbox", tmp_path / "public_mirrors.json", "abc123")

    assert payload["schema"] == "codex_federation_dispatch.v1"
    assert payload["parallel_work"]["schema"] == "codex_parallel_work_allocation.v1"
    assert payload["dispatch_count"] == 2
    assert payload["dispatches"][0]["surface_dir"] == "safari"
    assert payload["dispatches"][0]["status_template"]["agent"] == "safari_cloud"
    assert payload["dispatches"][0]["status_template"]["commit"] == "abc123"
    assert payload["dispatches"][0]["status_template"]["blocker"] == ""
    assert payload["dispatches"][0]["status_template"]["constraints"] == ["patch_only_no_direct_push"]
    assert "equivalent JSON packet" in payload["dispatches"][0]["handoff_text"]
    assert payload["dispatches"][1]["command"].startswith("python3 scripts/write_desktop_federation_status.py")


def test_write_dispatch_creates_aggregate_and_surface_packets(tmp_path) -> None:
    payload = {
        "schema": "codex_federation_dispatch.v1",
        "generated_at": "2026-06-02T00:00:00Z",
        "authoritative_head": "abc123",
        "parallel_work": parallel_work_allocation("abc123"),
        "ready_for_remote_write": False,
        "readiness_blockers": ("required federation packets pending",),
        "dispatch_count": 1,
        "dispatches": [
            {
                "agent": "mobile",
                "surface_dir": "mobile",
                "packet_type": "status_refresh",
                "priority": "required",
                "details": "refresh mobile",
                "expected_path": "FederationInbox/mobile/status.json",
                "command": "python3 scripts/write_mobile_federation_status.py",
                "status_template": {
                    "schema": "codex_federation_message.v1",
                    "agent": "mobile",
                    "type": "status",
                    "commit": "abc123",
                },
                "handoff_text": "Federation dispatch for mobile.",
            }
        ],
    }

    written = write_dispatch(payload, tmp_path / "FederationDispatch")

    assert "aggregate" in written
    aggregate = json.loads((tmp_path / "FederationDispatch" / "dispatch.json").read_text(encoding="utf-8"))
    surface = json.loads((tmp_path / "FederationDispatch" / "mobile" / "dispatch.json").read_text(encoding="utf-8"))
    assert aggregate["dispatch_count"] == 1
    assert aggregate["parallel_work"]["authoritative_head"] == "abc123"
    assert surface["schema"] == "codex_federation_surface_dispatch.v1"
    assert surface["parallel_work"]["surfaces"]["mobile"]["role"] == "user_facing_followup"
    assert surface["dispatch"]["agent"] == "mobile"


def test_command_for_known_surfaces() -> None:
    assert "write_local_federation_status.py" in command_for("local_cli", "FederationInbox/local/status.json")
    assert "write_federation_message.py" in command_for("safari_cloud", "FederationInbox/safari/status.json")
