#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

SOURCE_SUFFIXES = {".c", ".cc", ".cpp", ".cs", ".go", ".h", ".hpp", ".java", ".js", ".jsx", ".kt", ".kts", ".rs", ".swift", ".ts", ".tsx"}
SKIP_PARTS = {".git", ".terraform", "dist", "build", "node_modules", "vendor"}
TOKEN = "/" * 2


def has_comment_marker(line: str) -> bool:
    quote = ""
    escaped = False
    index = 0
    while index < len(line) - 1:
        char = line[index]
        if escaped:
            escaped = False
            index += 1
            continue
        if char == "\\" and quote:
            escaped = True
            index += 1
            continue
        if char in {"'", '"', "`"}:
            if not quote:
                quote = char
            elif quote == char:
                quote = ""
            index += 1
            continue
        if not quote and line[index:index + 2] == TOKEN:
            return True
        index += 1
    return False


def main() -> int:
    failures: list[str] = []
    for path in Path(".").rglob("*"):
        if not path.is_file() or path.suffix not in SOURCE_SUFFIXES:
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(lines, start=1):
            if has_comment_marker(line):
                failures.append(f"{path}:{number}")
    if failures:
        print("Prohibited comment style found:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
