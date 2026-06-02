from __future__ import annotations

import argparse
import json

import pytest

from scripts.write_federation_message import build_message, output_path, write_message


def args(**overrides):
    defaults = {
        "agent": "safari_cloud",
        "type": "status",
        "workstream": "Autonomous VNext",
        "cwd": "/workspace/0",
        "branch": "work",
        "commit": "abc123",
        "status_short": ["## work"],
        "remote": "",
        "blocker": "no_remote",
        "next_action": "export patch proposal",
        "repo": "aevespers2/0",
        "base": "",
        "summary": "",
        "file": [],
        "patch_path": "",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_build_status_message_for_safari() -> None:
    payload = build_message(args())

    assert payload["agent"] == "safari_cloud"
    assert payload["type"] == "status"
    assert payload["blocker"] == "no_remote"


def test_output_path_routes_agent_to_surface_directory(tmp_path) -> None:
    path = output_path("desktop_app", "status", tmp_path / "FederationInbox", None)

    assert path == tmp_path / "FederationInbox" / "desktop" / "status.json"


def test_write_message_validates_federation_schema(tmp_path) -> None:
    payload = build_message(args(agent="desktop_app", blocker="wrong_checkout"))
    path = tmp_path / "FederationInbox" / "desktop" / "status.json"

    write_message(payload, path)

    assert json.loads(path.read_text(encoding="utf-8"))["agent"] == "desktop_app"


def test_patch_proposal_forces_local_cli_authority() -> None:
    payload = build_message(
        args(
            type="patch_proposal",
            base="abc123",
            summary="propose inbox docs",
            file=["FederationInbox/README.md"],
            patch_path="patches/inbox-docs.patch",
        )
    )

    assert payload["patch"]["authority"] == "local_cli"
    assert payload["patch"]["source"] == "safari_cloud"


def test_local_cli_cannot_submit_patch_proposal() -> None:
    with pytest.raises(ValueError, match="local_cli should commit directly"):
        build_message(
            args(
                agent="local_cli",
                type="patch_proposal",
                base="abc123",
                summary="direct commit",
            )
        )
