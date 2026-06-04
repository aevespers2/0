from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.focus_safari_target import load_target
from scripts.record_federation_contact import build_contact_event, write_contact_event


def safari_probe_script() -> str:
    return """
(() => {
  const textarea = document.querySelector('textarea');
  const text = textarea ? textarea.value : '';
  const buttons = [...document.querySelectorAll('button')].map((button, index) => ({
    index,
    label: button.getAttribute('aria-label') || button.textContent.trim(),
    disabled: button.disabled,
    ariaDisabled: button.getAttribute('aria-disabled') || '',
    testid: button.getAttribute('data-testid') || '',
    id: button.id || ''
  })).filter(item => item.label || item.testid || item.id);
  const sendButton = buttons.find(item =>
    (
      item.testid === 'send-button' ||
      item.id === 'composer-submit-button' ||
      String(item.label).toLowerCase().includes('send')
    ) &&
    !String(item.label).toLowerCase().includes('stop')
  );
  const stopVisible = buttons.some(item =>
    String(item.label).toLowerCase().includes('stop answering') ||
    item.testid === 'stop-button'
  );
  return JSON.stringify({
    url: location.href,
    title: document.title,
    composer_contains_handoff: text.includes('Federation handoff from Local CLI'),
    textarea_length: text.length,
    send_button_visible: Boolean(sendButton),
    send_button_enabled: Boolean(sendButton) && !sendButton.disabled && sendButton.ariaDisabled !== 'true',
    send_button_disabled: sendButton ? Boolean(sendButton.disabled) : null,
    send_button_label: sendButton ? sendButton.label : '',
    send_button_id: sendButton ? sendButton.id : '',
    send_button_testid: sendButton ? sendButton.testid : '',
    send_button_aria_disabled: sendButton ? sendButton.ariaDisabled : '',
    send_button_index: sendButton ? sendButton.index : -1,
    stop_answering_visible: stopVisible,
    labels: buttons.map(item => item.label).filter(Boolean).slice(-20)
  });
})()
"""


def safari_click_send_script(button_index: int) -> str:
    return f"""
(() => {{
  const buttons = [...document.querySelectorAll('button')];
  const button = buttons[{button_index}];
  if (!button) return JSON.stringify({{clicked: false, reason: 'button_not_found'}});
  const label = button.getAttribute('aria-label') || button.textContent.trim();
  const testid = button.getAttribute('data-testid') || '';
  const id = button.id || '';
  const isSend = testid === 'send-button' ||
    id === 'composer-submit-button' ||
    String(label).toLowerCase().includes('send');
  if (!isSend || String(label).toLowerCase().includes('stop')) {{
    return JSON.stringify({{clicked: false, reason: 'button_not_send', label}});
  }}
  if (button.disabled || button.getAttribute('aria-disabled') === 'true') {{
    return JSON.stringify({{clicked: false, reason: 'button_disabled', label}});
  }}
  button.click();
  return JSON.stringify({{clicked: true, label}});
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


def wait_for_sendable(timeout_seconds: float, interval_seconds: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    probe = run_osascript(safari_probe_script())
    while time.monotonic() < deadline:
        if probe.get("send_button_enabled") and not probe.get("stop_answering_visible"):
            return probe
        time.sleep(interval_seconds)
        probe = run_osascript(safari_probe_script())
    return probe


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


def record_probe(
    probe: dict[str, Any],
    args: argparse.Namespace,
    status: str,
    detail: str,
) -> dict[str, Any]:
    target_url = expected_target_url(args)
    target_matched = target_url_matches(str(probe.get("url", "")), target_url)
    event_args = argparse.Namespace(
        surface="safari_cloud",
        channel="safari_chatgpt",
        status=status,
        authoritative_head=args.authoritative_head,
        dispatch=str(args.dispatch),
        detail=detail,
        evidence=[
            f"title={probe.get('title', '')}",
            f"url={probe.get('url', '')}",
            f"composer_contains_handoff={str(probe.get('composer_contains_handoff', False)).lower()}",
            f"send_button_visible={str(probe.get('send_button_visible', False)).lower()}",
            f"send_button_enabled={str(probe.get('send_button_enabled', False)).lower()}",
            f"send_button_disabled={str(probe.get('send_button_disabled', '')).lower()}",
            f"send_button_label={probe.get('send_button_label', '')}",
            f"send_button_id={probe.get('send_button_id', '')}",
            f"send_button_testid={probe.get('send_button_testid', '')}",
            f"send_button_aria_disabled={probe.get('send_button_aria_disabled', '')}",
            f"stop_answering_visible={str(probe.get('stop_answering_visible', False)).lower()}",
            f"target_url={target_url}",
            f"target_url_matched={str(target_matched).lower()}",
        ],
    )
    event = build_contact_event(event_args)
    write_contact_event(event, args.log, args.latest)
    return event


def watch(args: argparse.Namespace) -> dict[str, Any]:
    probe = wait_for_sendable(args.timeout, args.interval)
    sent = None
    target_url = expected_target_url(args)
    target_matched = target_url_matches(str(probe.get("url", "")), target_url)
    if not target_matched:
        status = "failed"
        detail = f"Safari watch is on wrong tab: expected {target_url}, saw {probe.get('url', '')}"
    elif probe.get("send_button_enabled") and not probe.get("stop_answering_visible") and args.send:
        sent = run_osascript(safari_click_send_script(int(probe["send_button_index"])))
        status = "sent" if sent.get("clicked") else "failed"
        detail = "Safari dispatch handoff sent." if sent.get("clicked") else f"Safari send failed: {sent.get('reason')}"
    elif probe.get("send_button_enabled") and not probe.get("stop_answering_visible"):
        status = "staged"
        detail = "Safari dispatch handoff is staged and sendable; --send was not requested."
    else:
        status = "blocked"
        detail = "Safari dispatch handoff is staged but send is unavailable."
    event = record_probe(probe, args, status, detail)
    return {"probe": probe, "send_result": sent, "contact_event": event}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wait for Safari dispatch handoff sendability.")
    parser.add_argument("--dispatch", type=Path, default=Path("FederationDispatch/safari/dispatch.json"))
    parser.add_argument("--authoritative-head", default="")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--send", action="store_true")
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
    result = watch(args)
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.latest)


if __name__ == "__main__":
    main()
