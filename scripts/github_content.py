#!/usr/bin/env python3
"""Strict decoding helpers for GitHub Contents API responses."""
from __future__ import annotations

import base64
import binascii
from typing import Any


def decode_github_text(payload: Any, path: str) -> str:
    """Decode UTF-8 text returned by GitHub's Contents API.

    GitHub wraps base64 content across lines. Whitespace is removed before
    strict alphabet and padding validation so valid API responses are accepted
    while malformed payloads still fail closed.
    """
    if not isinstance(payload, dict) or not isinstance(payload.get("content"), str):
        raise ValueError(f"invalid content response for {path}")
    encoding = payload.get("encoding")
    if encoding not in (None, "base64"):
        raise ValueError(f"unsupported content encoding for {path}: {encoding}")

    compact = "".join(payload["content"].split())
    try:
        decoded = base64.b64decode(compact, validate=True)
        return decoded.decode("utf-8")
    except (binascii.Error, UnicodeDecodeError) as exc:
        raise ValueError(f"invalid base64 UTF-8 content response for {path}") from exc
