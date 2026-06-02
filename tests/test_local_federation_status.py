from __future__ import annotations

import json

from scripts.write_local_federation_status import write_status


def test_write_status_creates_inbox_packet(tmp_path) -> None:
    output = tmp_path / "FederationInbox" / "local" / "status.json"
    payload = {
        "schema": "codex_federation_message.v1",
        "agent": "local_cli",
        "type": "status",
        "workstream": "Autonomous vNext",
        "cwd": "/repo",
        "branch": "main",
        "commit": "abc123",
        "status_short": ["## main"],
        "remote": "origin git@example:repo.git",
        "blocker": "",
        "next_action": "collect remote status",
    }

    write_status(payload, output)

    assert json.loads(output.read_text(encoding="utf-8"))["agent"] == "local_cli"
