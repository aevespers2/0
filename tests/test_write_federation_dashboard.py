from __future__ import annotations

import json

from scripts.write_federation_dashboard import (
    build_dashboard,
    contact_surfaces,
    effective_readiness_blockers,
    load_or_verify_mirrors,
    write_dashboard,
)


def test_build_dashboard_summarizes_operational_state() -> None:
    state = {
        "ready_for_remote_write": False,
        "readiness_blockers": ("required federation packets pending",),
    }
    relay = {
        "dispatch_agent": "safari_cloud",
        "latest_contact_status": "observed",
        "required_packets": ("safari_cloud",),
        "next_action": "Collect FederationInbox/safari/status.json.",
    }
    contact = {
        "all_contacts_fresh": True,
        "surfaces": (
            {"surface": "safari_cloud", "status": "observed"},
            {"surface": "desktop_app", "status": "observed"},
        ),
    }
    mirrors = {"synchronized": True}

    dashboard = build_dashboard(state, relay, contact, mirrors, "abc123")

    assert dashboard["schema"] == "codex_federation_dashboard.v1"
    assert dashboard["authoritative_head"] == "abc123"
    assert dashboard["mirrors_synchronized"] is True
    assert dashboard["contact_evidence_fresh"] is True
    assert dashboard["contact_surfaces"]["desktop_app"] == "observed"
    assert dashboard["required_packets"] == ("safari_cloud",)


def test_contact_surfaces_ignores_empty_surface_names() -> None:
    assert contact_surfaces({"surfaces": ({"surface": "", "status": "missing"},)}) == {}


def test_contact_surfaces_prefers_actionable_status() -> None:
    report = {
        "surfaces": (
            {"surface": "safari_cloud", "status": "observed", "actionable_status": "blocked"},
            {"surface": "desktop_app", "status": "observed", "actionable_status": ""},
        )
    }

    assert contact_surfaces(report) == {
        "safari_cloud": "blocked",
        "desktop_app": "observed",
    }


def test_effective_readiness_blockers_removes_synced_mirror_blocker() -> None:
    blockers = effective_readiness_blockers(
        {
            "readiness_blockers": (
                "public mirrors out of sync",
                "required federation packets pending",
            )
        },
        {"synchronized": True},
    )

    assert blockers == ("required federation packets pending",)


def test_load_or_verify_mirrors_uses_saved_report(tmp_path, monkeypatch) -> None:
    path = tmp_path / "mirror.json"
    path.write_text(json.dumps({"synchronized": True}), encoding="utf-8")
    monkeypatch.setattr(
        "scripts.write_federation_dashboard.verify_manifest",
        lambda manifest, repo: {"synchronized": False},
    )

    assert load_or_verify_mirrors(path, tmp_path, tmp_path / "manifest.json", False)["synchronized"] is True


def test_load_or_verify_mirrors_refreshes_when_requested(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        "scripts.write_federation_dashboard.verify_manifest",
        lambda manifest, repo: {"synchronized": True},
    )

    assert load_or_verify_mirrors(tmp_path / "missing.json", tmp_path, tmp_path / "manifest.json", True)["synchronized"] is True


def test_write_dashboard_creates_output(tmp_path) -> None:
    output = tmp_path / "reports" / "dashboard.json"

    write_dashboard({"schema": "example"}, output)

    assert json.loads(output.read_text(encoding="utf-8"))["schema"] == "example"
