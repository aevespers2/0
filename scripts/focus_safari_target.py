from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from typing import Any


def load_target(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "codex_safari_target.v1":
        raise ValueError("unsupported Safari target schema")
    return payload


def focus_script(target_url: str, open_if_missing: bool) -> str:
    return f"""
(() => {{
  const targetUrl = {json.dumps(target_url)};
  const openIfMissing = {json.dumps(open_if_missing)};
  const safari = Application('Safari');
  safari.activate();
  const windows = safari.windows();
  for (let windowIndex = 0; windowIndex < windows.length; windowIndex += 1) {{
    const win = windows[windowIndex];
    const tabs = win.tabs();
    for (let tabIndex = 0; tabIndex < tabs.length; tabIndex += 1) {{
      const tab = tabs[tabIndex];
      let url = '';
      let title = '';
      try {{ url = String(tab.url()); }} catch (error) {{ url = ''; }}
      try {{ title = String(tab.name()); }} catch (error) {{ title = ''; }}
      if (url === targetUrl || url.startsWith(targetUrl)) {{
        win.currentTab = tab;
        win.index = 1;
        return JSON.stringify({{
          focused: true,
          opened: false,
          matched: true,
          window_index: windowIndex,
          tab_index: tabIndex,
          url,
          title
        }});
      }}
    }}
  }}
  if (openIfMissing && targetUrl) {{
    if (!windows.length) {{
      return JSON.stringify({{
        focused: false,
        opened: false,
        matched: false,
        window_index: -1,
        tab_index: -1,
        url: '',
        title: '',
        reason: 'safari_window_not_found'
      }});
    }}
    windows[0].currentTab.url = targetUrl;
    windows[0].index = 1;
    return JSON.stringify({{
      focused: true,
      opened: true,
      matched: false,
      window_index: 0,
      tab_index: -1,
      url: targetUrl,
      title: ''
    }});
  }}
  return JSON.stringify({{
    focused: false,
    opened: false,
    matched: false,
    window_index: -1,
    tab_index: -1,
    url: '',
    title: '',
    reason: 'target_tab_not_found'
  }});
}})()
"""


def run_osascript(javascript: str) -> dict[str, Any]:
    result = subprocess.run(
        ["osascript", "-l", "JavaScript", "-e", javascript],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = result.stdout.strip()
    return json.loads(output) if output else {}


def focus_target(args: argparse.Namespace) -> dict[str, Any]:
    target = load_target(args.target)
    target_url = args.url or str(target.get("target_url", ""))
    if not target_url:
        return {
            "schema": "codex_safari_target_focus.v1",
            "focused": False,
            "opened": False,
            "matched": False,
            "target_url": "",
            "reason": "target_url_missing",
        }
    try:
        result = run_osascript(focus_script(target_url, args.open_if_missing))
    except subprocess.CalledProcessError as error:
        return {
            "schema": "codex_safari_target_focus.v1",
            "focused": False,
            "opened": False,
            "matched": False,
            "target_url": target_url,
            "reason": "osascript_failed",
            "error": error.stderr.strip(),
        }
    return {
        "schema": "codex_safari_target_focus.v1",
        "target_url": target_url,
        **result,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Focus the configured Safari ChatGPT federation target tab.")
    parser.add_argument("--target", type=Path, default=Path("FederationRelay/safari_target.json"))
    parser.add_argument("--url", default="")
    parser.add_argument("--no-open-if-missing", action="store_false", dest="open_if_missing")
    parser.set_defaults(open_if_missing=True)
    parser.add_argument("--output", type=Path, default=Path("reports/safari_target_focus_latest.json"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = focus_target(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.output)
    if not result.get("focused"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
