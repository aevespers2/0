from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from typing import Any


DEFAULT_SURFACES = ("safari_cloud", "desktop_app")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def git_head(repo: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def contact_path(latest_dir: Path, surface: str) -> Path:
    return latest_dir / f"{surface}.json"


def summarize_surface(surface: str, latest_dir: Path, authoritative_head: str) -> dict[str, Any]:
    path = contact_path(latest_dir, surface)
    contact = load_json(path)
    head = str(contact.get("authoritative_head", ""))
    status = str(contact.get("status", "missing" if not contact else ""))
    return {
        "surface": surface,
        "path": str(path),
        "present": bool(contact),
        "status": status,
        "channel": contact.get("channel", ""),
        "detail": contact.get("detail", ""),
        "authoritative_head": head,
        "fresh": bool(contact) and head == authoritative_head,
        "evidence": contact.get("evidence", {}),
    }


def build_report(
    latest_dir: Path,
    authoritative_head: str,
    surfaces: tuple[str, ...] = DEFAULT_SURFACES,
) -> dict[str, Any]:
    surface_reports = tuple(
        summarize_surface(surface, latest_dir, authoritative_head) for surface in surfaces
    )
    missing = tuple(item["surface"] for item in surface_reports if not item["present"])
    stale = tuple(item["surface"] for item in surface_reports if item["present"] and not item["fresh"])
    return {
        "schema": "codex_federation_contact_report.v1",
        "authoritative_head": authoritative_head,
        "surface_count": len(surface_reports),
        "missing_surfaces": missing,
        "stale_surfaces": stale,
        "all_contacts_fresh": not missing and not stale,
        "surfaces": surface_reports,
    }


def write_report(report: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a compact per-surface federation contact report.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--latest-dir", type=Path, default=Path("reports/federation_contact_latest"))
    parser.add_argument("--authoritative-head", default="")
    parser.add_argument("--surface", action="append", default=[])
    parser.add_argument("--output", type=Path, default=Path("reports/federation_contact_report.json"))
    parser.add_argument("--print", action="store_true", dest="print_report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    head = args.authoritative_head or git_head(args.repo)
    surfaces = tuple(args.surface) if args.surface else DEFAULT_SURFACES
    report = build_report(args.latest_dir, head, surfaces)
    write_report(report, args.output)
    if args.print_report:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(args.output)


if __name__ == "__main__":
    main()
