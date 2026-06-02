from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from autonomous_vnext.federation_kernel import AUTHORIZED_WRITER, PATCH_SCHEMA, PatchProposal, parse_message


MESSAGE_SCHEMA = "codex_federation_message.v1"
SURFACE_TO_DIR = {
    "local_cli": "local",
    "safari_cloud": "safari",
    "desktop_app": "desktop",
    "mobile": "mobile",
    "chatgpt_bridge": "bridge",
}
MESSAGE_TYPES = ("status", "blocker", "routine_checkin", "patch_proposal")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_message(args: argparse.Namespace) -> dict[str, Any]:
    if args.agent not in SURFACE_TO_DIR:
        raise ValueError(f"unsupported agent: {args.agent}")
    if args.type not in MESSAGE_TYPES:
        raise ValueError(f"unsupported message type: {args.type}")

    payload: dict[str, Any] = {
        "schema": MESSAGE_SCHEMA,
        "agent": args.agent,
        "type": args.type,
        "workstream": args.workstream,
        "generated_at": utc_now(),
        "cwd": args.cwd,
        "branch": args.branch,
        "commit": args.commit,
        "status_short": tuple(args.status_short),
        "remote": args.remote,
        "blocker": args.blocker,
        "next_action": args.next_action,
    }
    capabilities = tuple(getattr(args, "capability", ()))
    constraints = tuple(getattr(args, "constraint", ()))
    if capabilities:
        payload["capabilities"] = capabilities
    if constraints:
        payload["constraints"] = constraints
    if args.type == "patch_proposal":
        patch = build_patch(args)
        errors = patch.validate()
        if errors:
            raise ValueError("; ".join(errors))
        payload["patch"] = {
            "schema": PATCH_SCHEMA,
            "source": patch.source,
            "repo": patch.repo,
            "base": patch.base,
            "type": patch.patch_type,
            "summary": patch.summary,
            "files": patch.files,
            "patch_path": patch.patch_path,
            "authority": patch.authority,
        }
    return payload


def build_patch(args: argparse.Namespace) -> PatchProposal:
    return PatchProposal(
        source=args.agent,
        repo=args.repo,
        base=args.base,
        patch_type="git_patch",
        summary=args.summary,
        files=tuple(args.file),
        authority=AUTHORIZED_WRITER,
        patch_path=args.patch_path,
    )


def output_path(agent: str, message_type: str, inbox: Path, name: str | None) -> Path:
    directory = inbox / SURFACE_TO_DIR[agent]
    filename = name or f"{message_type}.json"
    if not filename.endswith(".json"):
        filename += ".json"
    return directory / filename


def write_message(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    parse_message(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a Codex federation inbox message.")
    parser.add_argument("--agent", required=True, choices=tuple(SURFACE_TO_DIR))
    parser.add_argument("--type", required=True, choices=MESSAGE_TYPES)
    parser.add_argument("--workstream", default="Autonomous VNext")
    parser.add_argument("--cwd", default="")
    parser.add_argument("--branch", default="")
    parser.add_argument("--commit", required=True)
    parser.add_argument("--status-short", action="append", default=[])
    parser.add_argument("--remote", default="")
    parser.add_argument("--blocker", default="")
    parser.add_argument("--next-action", default="")
    parser.add_argument("--capability", action="append", default=[])
    parser.add_argument("--constraint", action="append", default=[])
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--name", help="Output filename, default is <type>.json.")
    parser.add_argument("--print", action="store_true", dest="print_payload")
    parser.add_argument("--repo", default="aevespers2/0", help="Patch proposal repository.")
    parser.add_argument("--base", default="", help="Patch proposal base commit.")
    parser.add_argument("--summary", default="", help="Patch proposal summary.")
    parser.add_argument("--file", action="append", default=[], help="Patch proposal touched file.")
    parser.add_argument("--patch-path", default="", help="Patch proposal patch file path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_message(args)
    path = output_path(args.agent, args.type, args.inbox, args.name)
    write_message(payload, path)
    if args.print_payload:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(path)


if __name__ == "__main__":
    main()
