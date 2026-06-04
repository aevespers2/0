from __future__ import annotations

import json

from scripts.write_federation_contact_report import build_report, contact_path, write_report


def write_json(path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_build_report_marks_missing_and_stale_contacts(tmp_path) -> None:
    latest_dir = tmp_path / "latest"
    write_json(
        contact_path(latest_dir, "safari_cloud"),
        {
            "surface": "safari_cloud",
            "status": "observed",
            "authoritative_head": "head-1",
            "channel": "safari_chatgpt",
            "detail": "observed",
            "evidence": {"candidate_found": "false"},
        },
    )
    write_json(
        contact_path(latest_dir, "desktop_app"),
        {
            "surface": "desktop_app",
            "status": "observed",
            "authoritative_head": "old",
        },
    )

    report = build_report(latest_dir, "head-1", ("safari_cloud", "desktop_app", "mobile"))

    assert report["schema"] == "codex_federation_contact_report.v1"
    assert report["all_contacts_fresh"] is False
    assert report["missing_surfaces"] == ("mobile",)
    assert report["stale_surfaces"] == ("desktop_app",)
    assert report["surfaces"][0]["fresh"] is True
    assert report["surfaces"][0]["actionable_status"] == "observed"


def test_build_report_preserves_actionable_current_head_contact_from_log(tmp_path) -> None:
    latest_dir = tmp_path / "latest"
    log = tmp_path / "contact.jsonl"
    write_json(
        contact_path(latest_dir, "safari_cloud"),
        {
            "surface": "safari_cloud",
            "status": "observed",
            "authoritative_head": "head-1",
            "detail": "no candidate",
            "evidence": {"candidate_found": "false"},
        },
    )
    log.write_text(
        json.dumps(
            {
                "surface": "safari_cloud",
                "status": "blocked",
                "authoritative_head": "head-1",
                "detail": "send disabled",
                "evidence": {
                    "composer_contains_handoff": "true",
                    "send_button_enabled": "false",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )

    report = build_report(latest_dir, "head-1", ("safari_cloud",), log)

    surface = report["surfaces"][0]
    assert surface["status"] == "observed"
    assert surface["actionable_status"] == "blocked"
    assert surface["actionable_detail"] == "send disabled"


def test_write_report_creates_output(tmp_path) -> None:
    output = tmp_path / "reports" / "contact.json"

    write_report({"schema": "example"}, output)

    assert json.loads(output.read_text(encoding="utf-8"))["schema"] == "example"
