from __future__ import annotations

import json

from scripts.emit_bridge_signal import collect_bridge_signal, write_signal


def test_collect_bridge_signal_builds_bridge_readout(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        "scripts.emit_bridge_signal.build_state_report",
        lambda repo, inbox, manifest, authoritative_head: {
            "schema": "codex_federation_state_report.v1",
            "kernel": {
                "assessment": {
                    "synchronized": False,
                    "blocked_surfaces": ["safari_cloud"],
                    "missing_surfaces": (),
                    "stale_surfaces": (),
                },
                "message_count": 4,
            },
            "patch_proposals": {"valid": True, "proposal_count": 1},
            "public_mirrors": {"synchronized": True},
            "ready_for_remote_write": False,
            "readiness_blockers": ("missing/blocked federation surfaces",),
            "next_required_packets": (
                {
                    "agent": "safari_cloud",
                    "packet_type": "status_refresh",
                    "priority": "required",
                    "details": "status must refresh",
                },
            ),
            "authoritative_writer": "local_cli",
        },
    )
    manifest = tmp_path / "public_mirrors.json"
    manifest.write_text(
        json.dumps(
            {
                "schema": "public_mirrors.v1",
                "branch": "main",
                "mirrors": [
                    {
                        "name": "origin",
                        "url": "git@github.com:aevespers2/0.git",
                        "web_url": "https://github.com/aevespers2/0",
                    },
                    {"name": "georgetown", "url": "git@github.com:GeorgeTownSabatical/0.git"},
                ]
            }
        ),
        encoding="utf-8",
    )

    payload = collect_bridge_signal(
        repo=tmp_path,
        inbox=tmp_path / "FederationInbox",
        mirror_manifest=manifest,
        authoritative_head="abc123",
    )

    assert payload["schema"] == "codex_bridge_signal.v1"
    assert payload["ready_for_remote_write"] is False
    assert payload["synchronized"] is False
    assert payload["public_mirror_synchronized"] is True
    assert "safari_cloud" in payload["blocked_surfaces"]
    assert payload["required_packets"] == ["safari_cloud"]
    assert payload["remote_targets"] == ["https://github.com/aevespers2/0", "git@github.com:GeorgeTownSabatical/0.git"]


def test_write_signal_writes_file(tmp_path) -> None:
    output = tmp_path / "reports" / "bridge.json"
    payload = {"schema": "codex_bridge_signal.v1", "generated_at": "2026-01-01T00:00:00Z"}

    write_signal(output, payload)

    assert json.loads(output.read_text(encoding="utf-8")) == payload
