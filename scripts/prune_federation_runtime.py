from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MESSAGE_SCHEMA = "codex_federation_message.v1"
PATCH_SCHEMA = "codex_patch_proposal.v1"


@dataclass(frozen=True)
class RuntimePacket:
    path: Path
    agent: str
    message_type: str
    reason: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prune or archive ignored federation runtime packets.")
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--authoritative-head", default="", help="If provided, keep only fresh status/proposals at this head.")
    parser.add_argument("--all", action="store_true", help="Include all runtime packets, not just stale/blocking ones.")
    parser.add_argument("--include-local", action="store_true", help="Include FederationInbox/local in processing.")
    parser.add_argument("--no-archive", action="store_true", help="Delete matching packets instead of archiving.")
    parser.add_argument("--archive-dir", type=Path, default=Path("state/federation_runtime_archive"))
    parser.add_argument("--delete", action="store_true", help="Delete selected packets (or move to archive-dir if set).")
    parser.add_argument("--surfaces", default="", help="Comma-separated surface directories (default: safari,desktop,mobile,bridge).")
    parser.add_argument("--print", action="store_true", help="Print JSON report output.")
    return parser.parse_args()


def candidate_surfaces(include_local: bool) -> tuple[str, ...]:
    surfaces = ["safari", "desktop", "mobile", "bridge"]
    if include_local:
        surfaces.insert(0, "local")
    return tuple(surfaces)


def resolve_surfaces(arg: str, include_local: bool) -> tuple[str, ...]:
    if not arg.strip():
        return candidate_surfaces(include_local)
    return tuple(part.strip() for part in arg.split(",") if part.strip())


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_stale_status(payload: dict[str, Any], authoritative_head: str) -> bool:
    blocker = str(payload.get("blocker", "")).strip()
    commit = str(payload.get("commit", "")).strip()
    return bool(blocker) or (authoritative_head and commit and commit != authoritative_head)


def is_stale_patch(payload: dict[str, Any], authoritative_head: str) -> bool:
    if payload.get("schema") != MESSAGE_SCHEMA or payload.get("type") != "patch_proposal":
        return False
    patch = payload.get("patch", {})
    if payload.get("schema") != MESSAGE_SCHEMA:
        return False
    if patch.get("schema") != PATCH_SCHEMA:
        return True
    base = str(patch.get("base", "")).strip()
    return bool(base and authoritative_head and base != authoritative_head)


def iter_packets(inbox: Path, surfaces: tuple[str, ...]) -> list[Path]:
    packets = []
    for surface in surfaces:
        directory = inbox / surface
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.json")):
            if path.is_file():
                packets.append(path)
    return packets


def classify_packet(path: Path, authoritative_head: str, mode_all: bool) -> RuntimePacket | None:
    payload = load_json(path)
    if str(payload.get("schema")) != MESSAGE_SCHEMA:
        return None
    message_type = str(payload.get("type", ""))
    agent = str(payload.get("agent", path.parent.name))

    stale = False
    reason = ""
    if message_type in {"status", "blocker", "routine_checkin"}:
        stale = is_stale_status(payload, authoritative_head)
        if stale:
            reason = "stale_or_blocked_status"
    elif message_type == "patch_proposal":
        stale = is_stale_patch(payload, authoritative_head)
        if stale:
            reason = "stale_patch_base"
    else:
        stale = False

    if mode_all and not stale:
        reason = reason or "all_mode_selected"
    if mode_all or stale:
        return RuntimePacket(path=path, agent=agent, message_type=message_type, reason=reason)
    return None


def archive_packet(path: Path, archive_root: Path) -> Path:
    timestamp = utc_now().replace(":", "").replace("-", "")
    target_dir = archive_root / path.parent.name
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{timestamp}-{path.name}"
    return target


def run_prune(
    inbox: Path,
    authoritative_head: str,
    *,
    mode_all: bool,
    include_local: bool,
    surfaces_arg: str,
    delete: bool,
    archive_dir: Path | None,
) -> dict[str, Any]:
    surfaces = resolve_surfaces(surfaces_arg, include_local)
    packets = iter_packets(inbox, surfaces)
    selected: list[RuntimePacket] = []
    skipped: list[RuntimePacket] = []

    for path in packets:
        packet = classify_packet(path, authoritative_head, mode_all)
        if packet is None:
            skipped.append(RuntimePacket(path=path, agent=path.parent.name, message_type="", reason="ignored_by_filter"))
            continue
        selected.append(packet)

    actions = []
    deleted = 0
    archived = 0

    if delete:
        if mode_all or authoritative_head:
            for packet in selected:
                if archive_dir is None:
                    packet.path.unlink(missing_ok=True)
                    deleted += 1
                    actions.append(
                        {
                            "action": "deleted",
                            "source": str(packet.path),
                            "agent": packet.agent,
                            "type": packet.message_type,
                            "reason": packet.reason,
                        }
                    )
                else:
                    target = archive_packet(packet.path, archive_dir)
                    shutil.move(str(packet.path), str(target))
                    archived += 1
                    actions.append(
                        {
                            "action": "archived",
                            "source": str(packet.path),
                            "destination": str(target),
                            "agent": packet.agent,
                            "type": packet.message_type,
                            "reason": packet.reason,
                        }
                    )
        else:
            raise ValueError("stale-only mode requires --authoritative-head")

    return {
        "schema": "codex_federation_runtime_prune.v1",
        "generated_at": utc_now(),
        "authoritative_head": authoritative_head,
        "mode": "all" if mode_all else "stale_only",
        "inbox": str(inbox),
        "surfaces": list(surfaces),
        "matched": len(selected),
        "skipped": len(skipped),
        "deleted": deleted,
        "archived": archived,
        "actions": actions,
        "targets": [
            {
                "path": str(packet.path),
                "agent": packet.agent,
                "type": packet.message_type,
                "reason": packet.reason,
            }
            for packet in selected
        ],
    }


def main() -> None:
    args = parse_args()
    report = run_prune(
        inbox=args.inbox,
        authoritative_head=args.authoritative_head,
        mode_all=args.all,
        include_local=args.include_local,
        surfaces_arg=args.surfaces,
        delete=args.delete,
        archive_dir=None if (args.delete and args.no_archive) else args.archive_dir,
    )
    if args.print or not args.delete:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(json.dumps({"schema": report["schema"], "matched": report["matched"], "archived": report["archived"]}))


if __name__ == "__main__":
    main()
