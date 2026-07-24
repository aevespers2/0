from __future__ import annotations

import base64
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "portfolio_health_entry", SCRIPTS / "portfolio_health_entry.py"
)
assert SPEC and SPEC.loader
entry = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(entry)


def encoded(value: bytes) -> str:
    return base64.b64encode(value).decode("ascii")


def test_decoder_accepts_github_wrapped_base64_content():
    raw = encoded(b"permissions:\n  contents: read\n")
    wrapped = "\n".join(raw[index:index + 8] for index in range(0, len(raw), 8)) + "\n"
    assert entry.text(
        "/repos/aevespers2/example/contents/.github/workflows/ci.yml",
        requester=lambda path: {"encoding": "base64", "content": wrapped},
    ) == "permissions:\n  contents: read\n"


def test_decoder_rejects_invalid_base64_after_whitespace_normalization():
    with pytest.raises(ValueError, match="invalid base64 UTF-8"):
        entry.text(
            "/repos/aevespers2/example/contents/README.md",
            requester=lambda path: {"encoding": "base64", "content": "YWJj$A==\n"},
        )


def test_decoder_rejects_non_utf8_content():
    with pytest.raises(ValueError, match="invalid base64 UTF-8"):
        entry.text(
            "/repos/aevespers2/example/contents/blob.bin",
            requester=lambda path: {"encoding": "base64", "content": encoded(b"\xff\xfe")},
        )


def test_decoder_rejects_unexpected_encoding():
    with pytest.raises(ValueError, match="unsupported content encoding"):
        entry.text(
            "/repos/aevespers2/example/contents/README.md",
            requester=lambda path: {"encoding": "utf-8", "content": "plain text"},
        )


def test_entrypoint_installs_corrected_decoder_on_scanner_module():
    assert entry.health.text is entry.text
