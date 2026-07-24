#!/usr/bin/env python3
"""Hardened entry point for the portfolio-health control plane."""
from __future__ import annotations

import sys
from typing import Any, Callable

import portfolio_health as health
from github_content import decode_github_text


def text(path: str, requester: Callable[[str], Any] = health.api) -> str | None:
    payload = health.content(path, requester)
    if payload is None:
        return None
    return decode_github_text(payload, path)


# Install the corrected decoder in the reviewed scanner module before any scan.
health.text = text


if __name__ == "__main__":
    sys.exit(health.main())
