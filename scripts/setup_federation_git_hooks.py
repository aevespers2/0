from __future__ import annotations

import argparse
import subprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install repository-level federation git hooks."
    )
    parser.add_argument(
        "--hooks-path",
        default=".githooks",
        help="Path to the federation hook directory.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    subprocess.run(
        ["git", "config", "--local", "core.hooksPath", args.hooks_path],
        check=True,
    )
    print(f"Configured local git hook path: {args.hooks_path}")
    print(f"Enabled hooks: {args.hooks_path}/pre-push")


if __name__ == "__main__":
    main()
