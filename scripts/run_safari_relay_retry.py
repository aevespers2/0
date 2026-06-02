from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import time
from typing import Any


def run_command(command: list[str], cwd: Path) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def parse_json_stdout(result: dict[str, Any]) -> dict[str, Any]:
    if result["returncode"] != 0 or not result["stdout"]:
        return {}
    try:
        return json.loads(result["stdout"])
    except json.JSONDecodeError:
        return {}


def run_attempt(args: argparse.Namespace, attempt: int) -> dict[str, Any]:
    routine = run_command(["python3", "scripts/run_federation_routine.py", "--print"], args.repo)
    stage = run_command(["python3", "scripts/stage_safari_dispatch.py", "--print"], args.repo)
    watch_command = [
        "python3",
        "scripts/watch_safari_dispatch_send.py",
        "--timeout",
        str(args.watch_timeout),
        "--interval",
        str(args.watch_interval),
        "--print",
    ]
    if args.send:
        watch_command.append("--send")
    watch = run_command(watch_command, args.repo)
    relay_summary = run_command(["python3", "scripts/write_federation_relay_summary.py", "--print"], args.repo)
    watch_payload = parse_json_stdout(watch)
    contact = watch_payload.get("contact_event", {})
    return {
        "attempt": attempt,
        "routine": routine,
        "stage": stage,
        "watch": watch,
        "relay_summary": relay_summary,
        "contact_status": contact.get("status", ""),
        "contact_detail": contact.get("detail", ""),
        "send_result": watch_payload.get("send_result"),
    }


def run_retry(args: argparse.Namespace) -> dict[str, Any]:
    attempts = []
    for index in range(1, args.attempts + 1):
        attempt = run_attempt(args, index)
        attempts.append(attempt)
        if attempt["contact_status"] in {"sent", "acknowledged"}:
            break
        if index < args.attempts:
            time.sleep(args.interval)
    return {
        "schema": "codex_safari_relay_retry.v1",
        "attempt_count": len(attempts),
        "send_requested": args.send,
        "final_status": attempts[-1]["contact_status"] if attempts else "",
        "final_detail": attempts[-1]["contact_detail"] if attempts else "",
        "attempts": attempts,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run bounded Safari relay retry attempts.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--interval", type=float, default=5.0)
    parser.add_argument("--watch-timeout", type=float, default=5.0)
    parser.add_argument("--watch-interval", type=float, default=1.0)
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("reports/safari_relay_retry_latest.json"))
    parser.add_argument("--print", action="store_true", dest="print_result")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_retry(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.print_result:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
