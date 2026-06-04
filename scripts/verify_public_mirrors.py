from __future__ import annotations

import argparse
import json
import subprocess
import time
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


def remote_head_with_retries(
    url: str,
    branch: str,
    cwd: Path,
    attempts: int = 3,
    delay: float = 0.5,
) -> tuple[str, str]:
    last_error = ""
    for attempt in range(max(1, attempts)):
        try:
            return remote_head(url, branch, cwd), ""
        except (subprocess.CalledProcessError, ValueError) as error:
            last_error = str(error)
            if attempt + 1 < attempts:
                time.sleep(delay)
    return "", last_error


def verify_manifest(
    path: Path,
    cwd: Path,
    attempts: int = 3,
    retry_delay: float = 0.5,
) -> dict[str, Any]:
    manifest = load_manifest(path)
    branch = str(manifest["branch"])
    expected = git(["rev-parse", "HEAD"], cwd)
    heads = []
    mismatches = []
    errors = []

    for mirror in manifest["mirrors"]:
        name = str(mirror["name"])
        url = str(mirror["url"])
        head, error = remote_head_with_retries(url, branch, cwd, attempts, retry_delay)
        heads.append(MirrorHead(name=name, url=url, branch=branch, head=head))
        if error:
            errors.append({"name": name, "url": url, "error": error})
            continue
        if head != expected:
            mismatches.append({"name": name, "url": url, "head": head, "expected": expected})

    return {
        "schema": "public_mirror_verification.v1",
        "expected_head": expected,
        "branch": branch,
        "synchronized": not mismatches and not errors,
        "mirrors": [head.__dict__ for head in heads],
        "mismatches": mismatches,
        "errors": errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify public mirror remotes match the local HEAD.")
    parser.add_argument("--manifest", type=Path, default=Path("public_mirrors.json"))
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=0.5)
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = verify_manifest(args.manifest, args.repo, args.attempts, args.retry_delay)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    if not result["synchronized"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
