from __future__ import annotations

import json

from scripts.write_federation_operator_handoff import build_handoff, build_text, load_inbox_statuses, write_outputs


def test_build_handoff_summarizes_all_surface_roles() -> None:
    dashboard = {
        "authoritative_head": "abc123",
        "ready_for_remote_write": False,
        "mirrors_synchronized": True,
        "contact_evidence_fresh": True,
        "contact_surfaces": {"safari_cloud": "blocked", "desktop_app": "observed"},
        "required_packets": ["safari_cloud"],
        "readiness_blockers": ["required federation packets pending"],
        "relay_status": "blocked",
        "next_action": "copy Safari packet",
    }
    contact_report = {
        "surfaces": [
            {
                "surface": "safari_cloud",
                "status": "observed",
                "actionable_status": "blocked",
                "actionable_detail": "send disabled",
            },
            {
                "surface": "desktop_app",
                "status": "observed",
                "actionable_status": "observed",
                "actionable_detail": "no window",
            },
        ]
    }
    relay_summary = {
        "latest_contact_evidence": {
            "target_url": "https://chatgpt.com/c/example",
        }
    }
    dispatch = {
        "authoritative_head": "abc123",
        "parallel_work": {
            "coordination_rule": "local_cli remains authoritative",
            "merge_rule": "local_cli validates patches",
            "surfaces": {
                "local_cli": {"role": "authoritative_integrator", "handoff_type": "direct"},
                "safari_cloud": {
                    "role": "patch_first_parallel_builder",
                    "handoff_type": "patch_proposal",
                    "constraints": ["patch_only_no_direct_push"],
                    "must_report": ["status packet"],
                },
                "desktop_app": {"role": "local_context_observer", "handoff_type": "status"},
                "mobile": {"role": "user_facing_followup", "handoff_type": "routine_checkin"},
                "chatgpt_bridge": {"role": "planning_and_dispatch_coordinator", "handoff_type": "routine_checkin"},
            },
        },
        "dispatches": [
            {
                "agent": "safari_cloud",
                "expected_path": "FederationInbox/safari/status.json",
                "command": "python3 scripts/write_federation_message.py",
                "status_template": {"next_action": "refresh Safari status"},
            }
        ],
    }

    inbox_statuses = {
        "local_cli": {
            "type": "status",
            "commit": "abc123",
            "generated_at": "2026-06-04T00:00:00Z",
            "next_action": "keep integrating",
            "_path": "FederationInbox/local/status.json",
        },
        "mobile": {
            "type": "status",
            "commit": "abc123",
            "status_short": ["## main...origin/main"],
            "next_action": "collect priorities",
            "_path": "FederationInbox/mobile/status.json",
        },
        "chatgpt_bridge": {
            "type": "status",
            "commit": "old123",
            "blocker": "sandbox_write_boundary",
            "next_action": "relay bridge status",
            "_path": "FederationInbox/bridge/status.json",
        },
    }

    payload = build_handoff(dashboard, contact_report, relay_summary, dispatch, inbox_statuses)

    surfaces = {item["surface"]: item for item in payload["surfaces"]}
    assert payload["schema"] == "codex_federation_operator_handoff.v1"
    assert payload["mirrors_synchronized"] is True
    assert surfaces["local_cli"]["role"] == "authoritative_integrator"
    assert surfaces["local_cli"]["status"] == "reported"
    assert surfaces["local_cli"]["next_action"] == "keep integrating"
    assert surfaces["local_cli"]["packet_commit"] == "abc123"
    assert surfaces["local_cli"]["packet_fresh"] is True
    assert surfaces["local_cli"]["packet_stale"] is False
    assert surfaces["local_cli"]["packet_expected_commit"] == "abc123"
    assert surfaces["safari_cloud"]["status"] == "blocked"
    assert surfaces["safari_cloud"]["required"] is True
    assert surfaces["safari_cloud"]["expected_path"] == "FederationInbox/safari/status.json"
    assert "--clipboard" in surfaces["safari_cloud"]["command"]
    assert surfaces["safari_cloud"]["next_action"] == "copy Safari packet"
    assert surfaces["desktop_app"]["detail"] == "no window"
    assert surfaces["mobile"]["status"] == "reported"
    assert surfaces["mobile"]["detail"] == "## main...origin/main"
    assert surfaces["mobile"]["expected_path"] == "FederationInbox/mobile/status.json"
    assert surfaces["mobile"]["packet_fresh"] is True
    assert surfaces["mobile"]["command"].startswith("python3 scripts/write_mobile_federation_status.py")
    assert surfaces["chatgpt_bridge"]["role"] == "planning_and_dispatch_coordinator"
    assert surfaces["chatgpt_bridge"]["status"] == "stale_blocked"
    assert surfaces["chatgpt_bridge"]["blocker"] == "sandbox_write_boundary"
    assert surfaces["chatgpt_bridge"]["packet_fresh"] is False
    assert surfaces["chatgpt_bridge"]["packet_stale"] is True
    assert "from packet commit old123 to authoritative head abc123" in surfaces["chatgpt_bridge"]["next_action"]
    assert "codex_federation_message.v1" in surfaces["chatgpt_bridge"]["next_action"]
    assert surfaces["chatgpt_bridge"]["packet_stale_reason"] == (
        "packet commit old123 differs from authoritative head abc123"
    )
    assert surfaces["chatgpt_bridge"]["command"] == (
        'python3 scripts/emit_bridge_signal.py --authoritative-head "abc123" --print'
    )


def test_build_text_lists_surface_actions() -> None:
    text = build_text(
        {
            "authoritative_head": "abc123",
            "ready_for_remote_write": False,
            "mirrors_synchronized": True,
            "next_action": "copy packet",
            "surfaces": [
                {
                    "surface": "safari_cloud",
                    "status": "blocked",
                    "role": "patch_first_parallel_builder",
                    "next_action": "copy packet",
                    "command": "python3 scripts/extract_safari_ack.py --clipboard",
                }
            ],
        }
    )

    assert "Federation Operator Handoff" in text
    assert "safari_cloud: blocked" in text
    assert "--clipboard" in text


def test_write_outputs_creates_json_and_text(tmp_path) -> None:
    json_output = tmp_path / "handoff.json"
    text_output = tmp_path / "handoff.txt"

    write_outputs({"schema": "example", "surfaces": []}, json_output, text_output)

    assert json.loads(json_output.read_text(encoding="utf-8"))["schema"] == "example"
    assert "Federation Operator Handoff" in text_output.read_text(encoding="utf-8")


def test_load_inbox_statuses_maps_surface_directories(tmp_path) -> None:
    inbox = tmp_path / "FederationInbox"
    bridge_status = inbox / "bridge" / "status.json"
    mobile_status = inbox / "mobile" / "status.json"
    bridge_status.parent.mkdir(parents=True)
    mobile_status.parent.mkdir(parents=True)
    bridge_status.write_text(json.dumps({"agent": "chatgpt_bridge", "type": "status"}), encoding="utf-8")
    mobile_status.write_text(json.dumps({"agent": "mobile", "type": "status"}), encoding="utf-8")

    statuses = load_inbox_statuses(inbox)

    assert statuses["chatgpt_bridge"]["agent"] == "chatgpt_bridge"
    assert statuses["chatgpt_bridge"]["_path"].endswith("FederationInbox/bridge/status.json")
    assert statuses["mobile"]["agent"] == "mobile"
