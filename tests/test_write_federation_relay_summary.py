from __future__ import annotations

import json

from scripts.write_federation_relay_summary import (
    build_summary,
    contact_actionability_score,
    load_latest_contact_for_surface,
    next_action_for,
    select_actionable_contact,
    write_summary,
)


def write_json(path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_build_summary_combines_bridge_dispatch_and_contact(tmp_path) -> None:
    bridge = tmp_path / "bridge.json"
    dispatch = tmp_path / "dispatch.json"
    contact = tmp_path / "contact.json"
    write_json(
        bridge,
        {
            "authoritative_head": "abc123",
            "ready_for_remote_write": False,
            "required_packets": ["safari_cloud"],
            "missing_surfaces": ["safari_cloud"],
        },
    )
    write_json(
        dispatch,
        {
            "dispatch": {
                "agent": "safari_cloud",
                "expected_path": "FederationInbox/safari/status.json",
                "packet_type": "status",
            }
        },
    )
    write_json(
        contact,
        {
            "surface": "safari_cloud",
            "status": "blocked",
            "detail": "send unavailable",
            "evidence": {"stop_answering_visible": "true"},
        },
    )

    summary = build_summary(bridge, dispatch, contact)

    assert summary["schema"] == "codex_federation_relay_summary.v1"
    assert summary["authoritative_head"] == "abc123"
    assert summary["latest_contact_status"] == "blocked"
    assert "Wait for safari_cloud" in summary["next_action"]


def test_next_action_tracks_staged_and_sent_states() -> None:
    bridge = {"required_packets": ["safari_cloud"]}
    dispatch = {"agent": "safari_cloud", "expected_path": "FederationInbox/safari/status.json"}

    assert next_action_for(bridge, dispatch, {"status": "staged"}).startswith("Send staged handoff")
    assert next_action_for(bridge, dispatch, {"status": "sent"}).startswith("Await safari_cloud")
    assert next_action_for(bridge, dispatch, {"status": "acknowledged"}).startswith("Transcribe")
    assert next_action_for({"required_packets": []}, dispatch, {}).startswith("No required")


def test_next_action_for_observed_no_candidate_keeps_watch_path() -> None:
    bridge = {"required_packets": ["safari_cloud"]}
    dispatch = {"agent": "safari_cloud", "expected_path": "FederationInbox/safari/status.json"}
    contact = {"status": "observed", "evidence": {"candidate_found": "false"}}

    assert next_action_for(bridge, dispatch, contact).startswith("Continue watching safari_cloud")


def test_next_action_for_send_disabled_is_specific() -> None:
    bridge = {"required_packets": ["safari_cloud"]}
    dispatch = {"agent": "safari_cloud", "expected_path": "FederationInbox/safari/status.json"}
    contact = {
        "status": "blocked",
        "evidence": {
            "composer_contains_handoff": "true",
            "send_button_enabled": "false",
            "target_url": "https://chatgpt.com/c/example",
        },
    }

    action = next_action_for(bridge, dispatch, contact)

    assert action.startswith("Safari handoff is staged but send is disabled")
    assert "--clipboard" in action
    assert '--source-url "https://chatgpt.com/c/example"' in action
    assert "FederationInbox/safari/status.json" in action


def test_next_action_for_staged_disabled_uses_clipboard_recovery() -> None:
    bridge = {"required_packets": ["safari_cloud"]}
    dispatch = {"agent": "safari_cloud", "expected_path": "FederationInbox/safari/status.json"}
    contact = {
        "status": "staged",
        "evidence": {
            "composer_contains_handoff": "true",
            "send_button_disabled": "true",
            "url": "https://chatgpt.com/c/example",
        },
    }

    action = next_action_for(bridge, dispatch, contact)

    assert "--clipboard" in action
    assert '--source-url "https://chatgpt.com/c/example"' in action


def test_summary_uses_latest_contact_for_dispatch_surface(tmp_path) -> None:
    bridge = tmp_path / "bridge.json"
    dispatch = tmp_path / "dispatch.json"
    latest = tmp_path / "latest.json"
    log = tmp_path / "contact.jsonl"
    write_json(bridge, {"required_packets": ["safari_cloud"]})
    write_json(dispatch, {"dispatch": {"agent": "safari_cloud", "expected_path": "FederationInbox/safari/status.json"}})
    write_json(latest, {"surface": "desktop_app", "status": "blocked", "detail": "desktop no window"})
    log.write_text(
        json.dumps({"surface": "safari_cloud", "status": "staged", "detail": "safari staged"}) + "\n"
        + json.dumps({"surface": "desktop_app", "status": "blocked", "detail": "desktop no window"}) + "\n",
        encoding="utf-8",
    )

    summary = build_summary(bridge, dispatch, latest, log)

    assert summary["latest_contact_surface"] == "safari_cloud"
    assert summary["latest_contact_status"] == "staged"
    assert summary["latest_contact_detail"] == "safari staged"


def test_summary_prefers_surface_latest_file(tmp_path) -> None:
    bridge = tmp_path / "bridge.json"
    dispatch = tmp_path / "dispatch.json"
    latest = tmp_path / "latest.json"
    log = tmp_path / "contact.jsonl"
    surface_latest = tmp_path / "federation_contact_latest" / "safari_cloud.json"
    write_json(bridge, {"required_packets": ["safari_cloud"]})
    write_json(
        dispatch,
        {"dispatch": {"agent": "safari_cloud", "expected_path": "FederationInbox/safari/status.json"}},
    )
    write_json(latest, {"surface": "desktop_app", "status": "observed"})
    write_json(surface_latest, {"surface": "safari_cloud", "status": "blocked", "detail": "surface latest"})
    log.write_text(
        json.dumps({"surface": "safari_cloud", "status": "staged", "detail": "older log"}) + "\n",
        encoding="utf-8",
    )

    summary = build_summary(bridge, dispatch, latest, log)

    assert summary["latest_contact_status"] == "blocked"
    assert summary["latest_contact_detail"] == "surface latest"


def test_summary_prefers_current_head_send_disabled_contact_over_later_ack_probe(tmp_path) -> None:
    bridge = tmp_path / "bridge.json"
    dispatch = tmp_path / "dispatch.json"
    latest = tmp_path / "latest.json"
    log = tmp_path / "contact.jsonl"
    surface_latest = tmp_path / "federation_contact_latest" / "safari_cloud.json"
    write_json(
        bridge,
        {
            "authoritative_head": "head1",
            "required_packets": ["safari_cloud"],
            "missing_surfaces": ["safari_cloud"],
        },
    )
    write_json(
        dispatch,
        {
            "authoritative_head": "head1",
            "dispatch": {"agent": "safari_cloud", "expected_path": "FederationInbox/safari/status.json"},
        },
    )
    write_json(
        surface_latest,
        {
            "surface": "safari_cloud",
            "authoritative_head": "head1",
            "status": "observed",
            "detail": "no candidate",
            "evidence": {"candidate_found": "false"},
        },
    )
    write_json(latest, {"surface": "safari_cloud", "status": "observed"})
    log.write_text(
        json.dumps(
            {
                "surface": "safari_cloud",
                "authoritative_head": "old",
                "status": "blocked",
                "detail": "old disabled",
                "evidence": {"composer_contains_handoff": "true", "send_button_enabled": "false"},
            }
        )
        + "\n"
        + json.dumps(
            {
                "surface": "safari_cloud",
                "authoritative_head": "head1",
                "status": "blocked",
                "detail": "send disabled",
                "evidence": {"composer_contains_handoff": "true", "send_button_enabled": "false"},
            }
        )
        + "\n",
        encoding="utf-8",
    )

    summary = build_summary(bridge, dispatch, latest, log)

    assert summary["latest_contact_status"] == "blocked"
    assert summary["latest_contact_detail"] == "send disabled"
    assert summary["next_action"].startswith("Safari handoff is staged but send is disabled")
    assert "--clipboard" in summary["next_action"]


def test_select_actionable_contact_filters_by_authoritative_head() -> None:
    old = {
        "authoritative_head": "old",
        "status": "blocked",
        "evidence": {"composer_contains_handoff": "true", "send_button_enabled": "false"},
    }
    current = {"authoritative_head": "head1", "status": "observed", "evidence": {"candidate_found": "false"}}

    assert contact_actionability_score(old) > contact_actionability_score(current)
    assert select_actionable_contact([old, current], "head1") == current


def test_load_latest_contact_for_surface_ignores_bad_log_lines(tmp_path) -> None:
    latest = tmp_path / "latest.json"
    log = tmp_path / "contact.jsonl"
    write_json(latest, {"surface": "desktop_app", "status": "observed"})
    log.write_text(
        "not-json\n"
        + json.dumps({"surface": "safari_cloud", "status": "blocked"}) + "\n",
        encoding="utf-8",
    )

    contact = load_latest_contact_for_surface(latest, log, "safari_cloud")

    assert contact["status"] == "blocked"


def test_write_summary_creates_output(tmp_path) -> None:
    output = tmp_path / "reports" / "summary.json"

    write_summary({"schema": "example"}, output)

    assert json.loads(output.read_text(encoding="utf-8"))["schema"] == "example"
