from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import time
from typing import Any


def run_osascript(javascript: str) -> dict[str, Any]:
    script = (
        'tell application "Safari"\n'
        "  activate\n"
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
    output = result.stdout.strip()
    return json.loads(output) if output else {}


def composer_probe_script() -> str:
    return """
(() => {
  const selectors = [
    'textarea',
    '[contenteditable=true]',
    '[contenteditable=plaintext-only]',
    '[role=textbox]',
    '#prompt-textarea',
    '[data-testid=prompt-textarea]'
  ];
  const matches = selectors.map(selector => ({
    selector,
    count: document.querySelectorAll(selector).length
  }));
  const buttons = [...document.querySelectorAll('button')]
    .map(button => button.getAttribute('aria-label') || button.textContent.trim())
    .filter(Boolean)
    .slice(-20);
  const composer = selectors.some(selector => document.querySelector(selector));
  return JSON.stringify({
    url: location.href,
    title: document.title,
    ready_state: document.readyState,
    composer_found: composer,
    matches,
    buttons
  });
})()
"""


def reload_script() -> str:
    return "(() => { location.reload(); return JSON.stringify({reloaded: true, url: location.href}); })()"


def recover(args: argparse.Namespace) -> dict[str, Any]:
    before = run_osascript(composer_probe_script())
    reload_result: dict[str, Any] = {}
    if not before.get("composer_found") or args.force_reload:
        reload_result = run_osascript(reload_script())
        time.sleep(args.wait)
    after = run_osascript(composer_probe_script())
    return {
        "schema": "codex_safari_composer_recovery.v1",
        "before": before,
        "after": after,
        "reloaded": bool(reload_result),
        "reload": reload_result,
        "recovered": bool(after.get("composer_found")),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recover Safari ChatGPT composer visibility.")
    parser.add_argument("--wait", type=float, default=6.0)
    parser.add_argument("--force-reload", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("reports/safari_composer_recovery_latest.json"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = recover(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
