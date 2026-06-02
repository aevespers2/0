from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.record_federation_contact import build_contact_event, write_contact_event


def desktop_probe_script(app_name: str) -> str:
    return f"""
(() => {{
  const appName = {json.dumps(app_name)};
  const systemEvents = Application('System Events');
  const processes = systemEvents.processes.whose({{name: appName}})();
  if (!processes.length) {{
    return JSON.stringify({{
      app_name: appName,
      process_running: false,
      window_count: 0,
      frontmost: false,
      window_titles: []
    }});
  }}
  const process = processes[0];
  const windows = process.windows();
  return JSON.stringify({{
    app_name: appName,
    process_running: true,
    window_count: windows.length,
    frontmost: Boolean(process.frontmost()),
    window_titles: windows.map(window => {{
      try {{
        return String(window.name());
      }} catch (error) {{
        return '';
      }}
    }}).filter(Boolean).slice(0, 10)
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
    return json.loads(result.stdout.strip())


def status_for_probe(probe: dict[str, Any], failed: bool = False) -> str:
    if failed:
        return "failed"
    if probe.get("process_running"):
        return "observed"
    return "blocked"


def detail_for_probe(probe: dict[str, Any], failed: bool = False) -> str:
    if failed:
        return "Desktop Codex app probe failed."
    if probe.get("process_running"):
        if int(probe.get("window_count", 0)) > 0:
            return "Desktop Codex app is running with an accessible window."
        return "Desktop Codex app process is running; no accessible window was reported."
    return "Desktop Codex app process was not found."


def record_probe(
    probe: dict[str, Any],
    args: argparse.Namespace,
    status: str,
    detail: str,
) -> dict[str, Any]:
    titles = ",".join(str(item) for item in probe.get("window_titles", ()))
    event_args = argparse.Namespace(
        surface="desktop_app",
        channel="macos_codex_app",
        status=status,
        authoritative_head=args.authoritative_head,
        dispatch=str(args.dispatch),
        detail=detail,
        evidence=[
            f"app_name={probe.get('app_name', args.app_name)}",
            f"process_running={str(probe.get('process_running', False)).lower()}",
            f"window_count={probe.get('window_count', 0)}",
            f"frontmost={str(probe.get('frontmost', False)).lower()}",
            f"window_titles={titles}",
            f"error={probe.get('error', '')}",
        ],
    )
    event = build_contact_event(event_args)
    write_contact_event(event, args.log, args.latest)
    return event


def run(args: argparse.Namespace) -> dict[str, Any]:
    failed = False
    try:
        probe = run_osascript(desktop_probe_script(args.app_name))
    except (subprocess.CalledProcessError, json.JSONDecodeError) as error:
        failed = True
        probe = {
            "app_name": args.app_name,
            "process_running": False,
            "window_count": 0,
            "frontmost": False,
            "window_titles": [],
            "error": str(error),
        }
    status = status_for_probe(probe, failed)
    detail = detail_for_probe(probe, failed)
    event = record_probe(probe, args, status, detail)
    return {
        "schema": "codex_desktop_app_probe.v1",
        "probe": probe,
        "contact_event": event,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe the macOS Codex desktop app and record federation contact evidence.")
    parser.add_argument("--app-name", default="Codex")
    parser.add_argument("--dispatch", type=Path, default=Path("FederationDispatch/desktop/dispatch.json"))
    parser.add_argument("--authoritative-head", default="")
    parser.add_argument("--log", type=Path, default=Path("reports/federation_contact_log.jsonl"))
    parser.add_argument("--latest", type=Path, default=Path("reports/federation_contact_latest.json"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.authoritative_head:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            args.authoritative_head = result.stdout.strip()
        except subprocess.CalledProcessError:
            args.authoritative_head = ""
    result = run(args)
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.latest)


if __name__ == "__main__":
    main()
