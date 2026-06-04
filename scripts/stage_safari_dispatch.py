from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.focus_safari_target import load_target
from scripts.record_federation_contact import build_contact_event, write_contact_event


def build_handoff_text(dispatch_payload: dict[str, Any]) -> str:
    dispatch = dispatch_payload["dispatch"]
    template = json.dumps(dispatch["status_template"], indent=2, sort_keys=True)
    return (
        "Federation handoff from Local CLI to Safari Codex\n\n"
        f"Current repo head: {dispatch_payload['authoritative_head']}\n"
        "Current live assessment: Safari status packet is missing; local_cli, "
        "desktop_app, and mobile have refreshed status.\n"
        f"Required action: {dispatch['packet_type']} -> {dispatch['expected_path']}\n"
        "Command if available:\n"
        f"{dispatch['command']}\n\n"
        "If helper scripts are unavailable, emit this equivalent JSON packet:\n"
        f"{template}\n\n"
        "Please report what you are currently working on, whether you have local "
        "diffs/patches to export, and whether any blocker prevents writing "
        "FederationInbox/safari/status.json. Do not push directly; export patch "
        "proposals for Local CLI review."
    )


def safari_probe_script(handoff_text: str) -> str:
    encoded = json.dumps(handoff_text)
    return f"""
(() => {{
  const text = {encoded};
  const textarea = document.querySelector('textarea');
  const editable = document.querySelector('[contenteditable=true]');
  const target = textarea || editable;
  if (!target) {{
    return JSON.stringify({{
      staged: false,
      reason: 'composer_not_found',
      url: location.href,
      title: document.title,
      labels: [...document.querySelectorAll('button')]
        .map(b => b.getAttribute('aria-label') || b.textContent.trim())
        .filter(Boolean)
        .slice(-20)
    }});
  }}
  if (textarea) {{
    textarea.focus();
    const setter = Object.getOwnPropertyDescriptor(
      window.HTMLTextAreaElement.prototype,
      'value'
    ).set;
    setter.call(textarea, text);
    textarea.dispatchEvent(new InputEvent('beforeinput', {{
      bubbles: true,
      inputType: 'insertText',
      data: text
    }}));
    textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
    textarea.dispatchEvent(new InputEvent('input', {{
      bubbles: true,
      inputType: 'insertText',
      data: text
    }}));
    textarea.dispatchEvent(new Event('change', {{ bubbles: true }}));
  }} else {{
    editable.focus();
    editable.textContent = text;
    editable.dispatchEvent(new InputEvent('input', {{
      bubbles: true,
      inputType: 'insertText',
      data: text
    }}));
  }}
  const labels = [...document.querySelectorAll('button')]
    .map(b => b.getAttribute('aria-label') || b.textContent.trim())
    .filter(Boolean);
  return JSON.stringify({{
    staged: true,
    reason: '',
    url: location.href,
    title: document.title,
    textarea_length: textarea ? textarea.value.length : 0,
    composer_contains_handoff: textarea
      ? textarea.value.includes('Federation handoff from Local CLI')
      : editable.textContent.includes('Federation handoff from Local CLI'),
    send_button_visible: labels.some(label => label.toLowerCase().includes('send')),
    send_button_enabled: [...document.querySelectorAll('button')].some(button => {{
      const label = button.getAttribute('aria-label') || button.textContent.trim();
      return label.toLowerCase().includes('send') &&
        !label.toLowerCase().includes('stop') &&
        !button.disabled &&
        button.getAttribute('aria-disabled') !== 'true';
    }}),
    stop_answering_visible: labels.some(label => label.toLowerCase().includes('stop answering')),
    labels: labels.slice(-20)
  }});
}})()
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
    if not target_url:
        return True
    return current_url == target_url or current_url.startswith(target_url)


def stage_dispatch(args: argparse.Namespace) -> dict[str, Any]:
    dispatch_payload = json.loads(args.dispatch.read_text(encoding="utf-8"))
    handoff_text = build_handoff_text(dispatch_payload)
    probe = run_osascript(safari_probe_script(handoff_text))
    target_url = expected_target_url(args)
    current_url = str(probe.get("url", ""))
    target_matched = target_url_matches(current_url, target_url)
    status = "staged" if probe.get("staged") and target_matched else "failed"
    if probe.get("staged") and not target_matched:
        detail = f"Safari handoff staged in wrong tab: expected {target_url}, saw {current_url}"
    elif probe.get("stop_answering_visible") and not probe.get("send_button_enabled"):
        detail = "handoff staged in Safari composer; send unavailable while page exposes Stop answering"
    elif probe.get("send_button_enabled"):
        detail = "handoff staged in Safari composer; send button enabled"
    elif probe.get("send_button_visible"):
        detail = "handoff staged in Safari composer; send button visible but disabled"
    else:
        detail = f"Safari handoff staging result: {probe.get('reason', 'unknown')}"
    event_args = argparse.Namespace(
        surface="safari_cloud",
        channel="safari_chatgpt",
        status=status,
        authoritative_head=dispatch_payload["authoritative_head"],
        dispatch=str(args.dispatch),
        detail=detail,
        evidence=[
            f"title={probe.get('title', '')}",
            f"url={probe.get('url', '')}",
            f"composer_contains_handoff={str(probe.get('composer_contains_handoff', False)).lower()}",
            f"send_button_visible={str(probe.get('send_button_visible', False)).lower()}",
            f"send_button_enabled={str(probe.get('send_button_enabled', False)).lower()}",
            f"stop_answering_visible={str(probe.get('stop_answering_visible', False)).lower()}",
            f"target_url={target_url}",
            f"target_url_matched={str(target_matched).lower()}",
        ],
    )
    event = build_contact_event(event_args)
    write_contact_event(event, args.log, args.latest)
    return {"probe": probe, "contact_event": event}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage the current Safari dispatch in the Safari ChatGPT composer.")
    parser.add_argument("--dispatch", type=Path, default=Path("FederationDispatch/safari/dispatch.json"))
    parser.add_argument("--target", type=Path, default=Path("FederationRelay/safari_target.json"))
    parser.add_argument("--url", default="")
    parser.add_argument("--log", type=Path, default=Path("reports/federation_contact_log.jsonl"))
    parser.add_argument("--latest", type=Path, default=Path("reports/federation_contact_latest.json"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = stage_dispatch(args)
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.latest)


if __name__ == "__main__":
    main()
