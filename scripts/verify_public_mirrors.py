from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MirrorHead:
    name: str
    url: str
    branch: str
    head: str


def git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def load_manifest(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "public_mirrors.v1":
        raise ValueError("unsupported mirror manifest schema")
    if not payload.get("branch"):
        raise ValueError("mirror manifest branch is required")
    if not payload.get("mirrors"):
        raise ValueError("mirror manifest must include mirrors")
    return payload


def remote_head(url: str, branch: str, cwd: Path) -> str:
    output = git(["ls-remote", url, f"refs/heads/{branch}"], cwd)
    if not output:
        raise ValueError(f"remote branch not found: {url} {branch}")
    return output.split()[0]


def verify_manifest(path: Path, cwd: Path) -> dict[str, Any]:
    manifest = load_manifest(path)
    branch = str(manifest["branch"])
    expected = git(["rev-parse", "HEAD"], cwd)
    heads = []
    mismatches = []

    for mirror in manifest["mirrors"]:
        name = str(mirror["name"])
        url = str(mirror["url"])
        head = remote_head(url, branch, cwd)
        heads.append(MirrorHead(name=name, url=url, branch=branch, head=head))
        if head != expected:
            mismatches.append({"name": name, "url": url, "head": head, "expected": expected})

    return {
        "schema": "public_mirror_verification.v1",
        "expected_head": expected,
        "branch": branch,
        "synchronized": not mismatches,
        "mirrors": [head.__dict__ for head in heads],
        "mismatches": mismatches,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify public mirror remotes match the local HEAD.")
    parser.add_argument("--manifest", type=Path, default=Path("public_mirrors.json"))
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = verify_manifest(args.manifest, args.repo)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    if not result["synchronized"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
