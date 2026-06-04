from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from autonomous_vnext.federation_kernel import parse_message
from scripts.focus_safari_target import load_target
from scripts.record_federation_contact import build_contact_event, write_contact_event
from scripts.write_federation_message import output_path


EXPECTED_AGENT = "safari_cloud"
EXPECTED_SCHEMA = "codex_federation_message.v1"


def safari_messages_script() -> str:
    return """
(() => {
  const nodes = [...document.querySelectorAll('[data-message-author-role]')];
  const messages = nodes.map((node, index) => ({
    index,
    role: node.getAttribute('data-message-author-role') || '',
    text: node.innerText || node.textContent || ''
  })).filter(item => item.text.trim());
  const textarea = document.querySelector('textarea');
  return JSON.stringify({
    url: location.href,
    title: document.title,
    composer_length: textarea ? textarea.value.length : 0,
    message_count: messages.length,
    messages: messages.slice(-12)
  });
})()
"""


def run_osascript(javascript: str) -> dict[str, Any]:
    script = (
        'tell application "Safari"\n'
        f'  do JavaScript {json.dumps(javascript)} in current tab of front window\n'
        "end tell\n"
    )
    result = subprocess.run(
        ["osascript"],
        input=script,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return json.loads(result.stdout.strip())


def snapshot_from_text(text: str, *, url: str = "", title: str = "manual Safari packet input") -> dict[str, Any]:
    return {
        "url": url,
        "title": title,
        "composer_length": 0,
        "message_count": 1 if text.strip() else 0,
        "messages": [{"index": 0, "role": "assistant", "text": text}],
    }


def read_clipboard() -> str:
    result = subprocess.run(
        ["pbpaste"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def snapshot_from_source(args: argparse.Namespace) -> dict[str, Any]:
    sources = tuple(
        item
        for item in (
            bool(args.text_file),
            bool(args.stdin),
            bool(args.clipboard),
        )
        if item
    )
    if len(sources) > 1:
        raise ValueError("choose only one manual input source")
    if args.text_file:
        return snapshot_from_text(
            args.text_file.read_text(encoding="utf-8"),
            url=args.source_url,
            title=f"manual Safari packet input: {args.text_file}",
        )
    if args.stdin:
        return snapshot_from_text(sys.stdin.read(), url=args.source_url)
    if args.clipboard:
        return snapshot_from_text(
            read_clipboard(),
            url=args.source_url,
            title="manual Safari packet input: clipboard",
        )
    return run_osascript(safari_messages_script())


def iter_json_objects(text: str) -> tuple[dict[str, Any], ...]:
    objects: list[dict[str, Any]] = []
    stack = 0
    start: int | None = None
    in_string = False
    escaped = False

    for index, char in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            continue
        if char == "{":
            if stack == 0:
                start = index
            stack += 1
            continue
        if char == "}" and stack:
            stack -= 1
            if stack == 0 and start is not None:
                candidate = text[start : index + 1]
                try:
                    payload = json.loads(candidate)
                except json.JSONDecodeError:
                    start = None
                    continue
                if isinstance(payload, dict):
                    objects.append(payload)
                start = None
    return tuple(objects)


def valid_safari_message(payload: dict[str, Any], authoritative_head: str = "") -> bool:
    if payload.get("schema") != EXPECTED_SCHEMA:
        return False
    if payload.get("agent") != EXPECTED_AGENT:
        return False
    if payload.get("type") not in {"status", "blocker", "routine_checkin", "patch_proposal"}:
        return False
    if authoritative_head and payload.get("commit") != authoritative_head:
        return False
    return True


def extract_candidate(snapshot: dict[str, Any], authoritative_head: str = "") -> dict[str, Any] | None:
    messages = snapshot.get("messages", ())
    for message in reversed(messages):
        text = str(message.get("text", ""))
        for payload in reversed(iter_json_objects(text)):
            if valid_safari_message(payload, authoritative_head):
                return payload
    return None


def write_status_packet(payload: dict[str, Any], inbox: Path) -> Path:
    path = output_path(str(payload["agent"]), str(payload["type"]), inbox, "status.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    parse_message(path)
    return path


def expected_target_url(args: argparse.Namespace) -> str:
    url = str(getattr(args, "url", "") or "")
    if url:
        return url
    target_path = getattr(args, "target", None)
    if not target_path:
        return ""
    target = load_target(Path(target_path))
    return str(target.get("target_url", ""))


def target_url_matches(current_url: str, target_url: str) -> bool:
    if not target_url or not current_url:
        return True
    return current_url == target_url or current_url.startswith(target_url)


def record_ack(
    snapshot: dict[str, Any],
    args: argparse.Namespace,
    status: str,
    detail: str,
    candidate: dict[str, Any] | None,
    output_path_value: str = "",
) -> dict[str, Any]:
    target_url = expected_target_url(args)
    target_matched = target_url_matches(str(snapshot.get("url", "")), target_url)
    event_args = argparse.Namespace(
        surface=EXPECTED_AGENT,
        channel="safari_chatgpt",
        status=status,
        authoritative_head=args.authoritative_head,
        dispatch=str(args.dispatch),
        detail=detail,
        evidence=[
            f"title={snapshot.get('title', '')}",
            f"url={snapshot.get('url', '')}",
            f"message_count={snapshot.get('message_count', 0)}",
            f"candidate_found={str(candidate is not None).lower()}",
            f"candidate_type={candidate.get('type', '') if candidate else ''}",
            f"written_path={output_path_value}",
            f"target_url={target_url}",
            f"target_url_matched={str(target_matched).lower()}",
        ],
    )
    event = build_contact_event(event_args)
    write_contact_event(event, args.log, args.latest)
    return event


def run(args: argparse.Namespace) -> dict[str, Any]:
    snapshot = snapshot_from_source(args)
    target_url = expected_target_url(args)
    target_matched = target_url_matches(str(snapshot.get("url", "")), target_url)
    candidate = None if not target_matched else extract_candidate(snapshot, args.authoritative_head)
    written_path = ""
    if not target_matched:
        status = "failed"
        detail = f"Safari acknowledgment extraction is on wrong tab: expected {target_url}, saw {snapshot.get('url', '')}"
    elif candidate and args.write_status:
        written_path = str(write_status_packet(candidate, args.inbox))
        status = "acknowledged"
        detail = f"Safari visible response yielded a valid federation packet at {written_path}."
    elif candidate:
        status = "acknowledged"
        detail = "Safari visible response yielded a valid federation packet; --write-status was not requested."
    else:
        status = "observed"
        detail = "Safari visible conversation did not include a valid federation status packet."
    event = record_ack(snapshot, args, status, detail, candidate, written_path)
    return {
        "schema": "codex_safari_ack_extraction.v1",
        "candidate": candidate,
        "contact_event": event,
        "message_count": snapshot.get("message_count", 0),
        "written_path": written_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract explicit Safari federation acknowledgments from the visible ChatGPT tab.")
    parser.add_argument("--dispatch", type=Path, default=Path("FederationDispatch/safari/dispatch.json"))
    parser.add_argument("--authoritative-head", default="")
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument("--write-status", action="store_true")
    parser.add_argument("--text-file", type=Path, help="Read copied Safari response text from this file instead of live Safari.")
    parser.add_argument("--stdin", action="store_true", help="Read copied Safari response text from stdin instead of live Safari.")
    parser.add_argument("--clipboard", action="store_true", help="Read copied Safari response text from the macOS clipboard.")
    parser.add_argument("--source-url", default="", help="Optional Safari conversation URL for manual text input evidence.")
    parser.add_argument("--target", type=Path, default=Path("FederationRelay/safari_target.json"))
    parser.add_argument("--url", default="")
    parser.add_argument("--log", type=Path, default=Path("reports/federation_contact_log.jsonl"))
    parser.add_argument("--latest", type=Path, default=Path("reports/federation_contact_latest.json"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.authoritative_head and args.dispatch.exists():
        payload = json.loads(args.dispatch.read_text(encoding="utf-8"))
        args.authoritative_head = payload.get("authoritative_head", "")
    result = run(args)
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.latest)


if __name__ == "__main__":
    main()
