from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.watch_safari_dispatch_send import run_osascript, safari_probe_script


def input_nudge_script() -> str:
    return """
(() => {
  const textarea = document.querySelector('textarea');
  if (!textarea) return JSON.stringify({strategy: 'input_events', applied: false, reason: 'textarea_not_found'});
  textarea.focus();
  textarea.dispatchEvent(new KeyboardEvent('keydown', {bubbles: true, key: ' '}));
  textarea.dispatchEvent(new InputEvent('beforeinput', {bubbles: true, inputType: 'insertText', data: ' '}));
  textarea.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertText', data: textarea.value}));
  textarea.dispatchEvent(new KeyboardEvent('keyup', {bubbles: true, key: ' '}));
  textarea.dispatchEvent(new Event('change', {bubbles: true}));
  return JSON.stringify({strategy: 'input_events', applied: true, value_length: textarea.value.length});
})()
"""


def exec_command_nudge_script() -> str:
    return """
(() => {
  const textarea = document.querySelector('textarea');
  if (!textarea) return JSON.stringify({strategy: 'exec_command', applied: false, reason: 'textarea_not_found'});
  textarea.focus();
  const before = textarea.value.length;
  const inserted = document.execCommand('insertText', false, ' ');
  const afterInsert = textarea.value.length;
  if (inserted) document.execCommand('delete', false, null);
  textarea.dispatchEvent(new Event('input', {bubbles: true}));
  return JSON.stringify({
    strategy: 'exec_command',
    applied: true,
    inserted,
    before,
    after_insert: afterInsert,
    after_delete: textarea.value.length
  });
})()
"""


def probe_sendable() -> dict[str, Any]:
    return run_osascript(safari_probe_script())


def run_nudges(args: argparse.Namespace) -> dict[str, Any]:
    before = probe_sendable()
    attempts: list[dict[str, Any]] = []
    for script in (input_nudge_script(), exec_command_nudge_script()):
        result = run_osascript(script)
        time.sleep(args.wait)
        probe = probe_sendable()
        attempts.append({"result": result, "probe": probe})
        if probe.get("send_button_enabled") and not probe.get("stop_answering_visible"):
            break
    after = attempts[-1]["probe"] if attempts else before
    return {
        "schema": "codex_safari_sendability_nudge.v1",
        "before": before,
        "attempts": attempts,
        "after": after,
        "sendable": bool(after.get("send_button_enabled")) and not bool(after.get("stop_answering_visible")),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Try bounded browser input nudges to enable Safari ChatGPT sendability.")
    parser.add_argument("--wait", type=float, default=0.5)
    parser.add_argument("--output", type=Path, default=Path("reports/safari_sendability_nudge_latest.json"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_nudges(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
