from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import probe_desktop_codex_app


def open_app(app_name: str) -> dict[str, Any]:
    result = subprocess.run(
        ["open", "-a", app_name],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def recover(args: argparse.Namespace) -> dict[str, Any]:
    before = probe_desktop_codex_app.run(args)
    open_result: dict[str, Any] = {}
    before_probe = before.get("probe", {})
    if args.force_open or not before_probe.get("process_running") or int(before_probe.get("window_count", 0)) == 0:
        open_result = open_app(args.app_name)
        time.sleep(args.wait)
    after = probe_desktop_codex_app.run(args)
    after_probe = after.get("probe", {})
    return {
        "schema": "codex_desktop_app_recovery.v1",
        "app_name": args.app_name,
        "opened": bool(open_result),
        "open_result": open_result,
        "before": before,
        "after": after,
        "recovered": bool(after_probe.get("process_running")) and int(after_probe.get("window_count", 0)) > 0,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recover the macOS Codex desktop app window and record federation evidence.")
    parser.add_argument("--app-name", default="Codex")
    parser.add_argument("--dispatch", type=Path, default=Path("FederationDispatch/desktop/dispatch.json"))
    parser.add_argument("--authoritative-head", default="")
    parser.add_argument("--wait", type=float, default=2.0)
    parser.add_argument("--force-open", action="store_true")
    parser.add_argument("--log", type=Path, default=Path("reports/federation_contact_log.jsonl"))
    parser.add_argument("--latest", type=Path, default=Path("reports/federation_contact_latest.json"))
    parser.add_argument("--output", type=Path, default=Path("reports/desktop_codex_recovery_latest.json"))
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
    result = recover(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
