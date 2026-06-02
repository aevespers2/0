from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.write_federation_state_report import (
    build_state_report,
    write_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Abort execution when federation state is not safe for remote writes."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--inbox", type=Path, default=Path("FederationInbox"))
    parser.add_argument(
        "--mirror-manifest", type=Path, default=Path("public_mirrors.json")
    )
    parser.add_argument("--authoritative-head", required=True)
    parser.add_argument(
        "--output", type=Path, default=Path("reports/federation_state_report.json")
    )
    parser.add_argument("--print", action="store_true", dest="print_report")
    return parser.parse_args()


def enforce_remote_write_readiness(args: argparse.Namespace) -> dict[str, object]:
    report = build_state_report(
        args.repo,
        args.inbox,
        args.mirror_manifest,
        args.authoritative_head,
    )
    write_report(report, args.output)
    if args.print_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(args.output)
    if not report["ready_for_remote_write"]:
        blockers = report.get("readiness_blockers", ())
        print("Remote-write gate blocked by: " + ", ".join(blockers), file=sys.stderr)
        raise SystemExit(1)
    return report


def main() -> None:
    args = parse_args()
    enforce_remote_write_readiness(args)


if __name__ == "__main__":
    main()
