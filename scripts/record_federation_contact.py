from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONTACT_SCHEMA = "codex_federation_contact.v1"
VALID_STATUSES = ("observed", "staged", "sent", "acknowledged", "blocked", "failed")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_evidence(items: list[str]) -> dict[str, str]:
    evidence: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"evidence must be key=value: {item}")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"evidence key is empty: {item}")
        evidence[key] = value
    return evidence


def build_contact_event(args: argparse.Namespace) -> dict[str, Any]:
    if args.status not in VALID_STATUSES:
        raise ValueError(f"unsupported contact status: {args.status}")
    dispatch_payload = None
    if args.dispatch:
        dispatch_path = Path(args.dispatch)
        if dispatch_path.exists():
            dispatch_payload = json.loads(dispatch_path.read_text(encoding="utf-8"))
    return {
        "schema": CONTACT_SCHEMA,
        "generated_at": utc_now(),
        "surface": args.surface,
        "channel": args.channel,
        "status": args.status,
        "authoritative_head": args.authoritative_head,
        "dispatch_path": args.dispatch,
        "detail": args.detail,
        "evidence": parse_evidence(args.evidence),
        "dispatch": dispatch_payload,
    }


def write_contact_event(event: dict[str, Any], log_path: Path, latest_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    latest_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    latest_path.write_text(json.dumps(event, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record a federation surface-contact event.")
    parser.add_argument("--surface", required=True)
    parser.add_argument("--channel", required=True)
    parser.add_argument("--status", required=True, choices=VALID_STATUSES)
    parser.add_argument("--authoritative-head", default="")
    parser.add_argument("--dispatch", default="")
    parser.add_argument("--detail", required=True)
    parser.add_argument("--evidence", action="append", default=[], help="Evidence as key=value.")
    parser.add_argument("--log", type=Path, default=Path("reports/federation_contact_log.jsonl"))
    parser.add_argument("--latest", type=Path, default=Path("reports/federation_contact_latest.json"))
    parser.add_argument("--print", action="store_true", dest="print_event")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    event = build_contact_event(args)
    write_contact_event(event, args.log, args.latest)
    if args.print_event:
        print(json.dumps(event, indent=2, sort_keys=True))
    else:
        print(args.latest)


if __name__ == "__main__":
    main()
