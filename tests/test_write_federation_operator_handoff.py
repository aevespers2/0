from __future__ import annotations

import json

from scripts.write_federation_operator_handoff import build_handoff, build_text, write_outputs


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

    payload = build_handoff(dashboard, contact_report, relay_summary, dispatch)

    surfaces = {item["surface"]: item for item in payload["surfaces"]}
    assert payload["schema"] == "codex_federation_operator_handoff.v1"
    assert payload["mirrors_synchronized"] is True
    assert surfaces["local_cli"]["role"] == "authoritative_integrator"
    assert surfaces["safari_cloud"]["status"] == "blocked"
    assert surfaces["safari_cloud"]["required"] is True
    assert surfaces["safari_cloud"]["expected_path"] == "FederationInbox/safari/status.json"
    assert "--clipboard" in surfaces["safari_cloud"]["command"]
    assert surfaces["safari_cloud"]["next_action"] == "copy Safari packet"
    assert surfaces["desktop_app"]["detail"] == "no window"
    assert surfaces["mobile"]["command"].startswith("python3 scripts/write_mobile_federation_status.py")
    assert surfaces["chatgpt_bridge"]["role"] == "planning_and_dispatch_coordinator"


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
