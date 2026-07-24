from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "iris-verifier-contract.yml"


def _workflow() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_concurrency_is_bound_to_immutable_submitted_head() -> None:
    text = _workflow()
    assert "github.event.pull_request.head.sha || github.sha" in text
    assert "cancel-in-progress: false" in text
    assert "github.event.pull_request.number || github.ref }}\n  cancel-in-progress: true" not in text


def test_actions_and_test_dependency_are_immutable() -> None:
    text = _workflow()
    action_refs = re.findall(r"uses:\s+[^@\s]+@([^\s]+)", text)
    assert action_refs
    assert all(re.fullmatch(r"[0-9a-f]{40}", ref) for ref in action_refs)
    assert "pytest==8.4.2" in text
    assert "pip install --disable-pip-version-check pytest\n" not in text


def test_terminal_evidence_is_external_and_uploaded_on_failure() -> None:
    text = _workflow()
    assert "$RUNNER_TEMP/iris-verifier-contract-evidence" in text
    assert "if: always()" in text
    assert "name: Upload retained exact-head evidence" in text
    assert "if-no-files-found: error" in text
    assert "retention-days: 90" in text


def test_final_gate_fails_closed_after_evidence_upload() -> None:
    text = _workflow()
    upload_position = text.index("name: Upload retained exact-head evidence")
    gate_position = text.index("name: Fail closed on unsuccessful validation")
    assert upload_position < gate_position
    for marker in (
        "CHECKOUT_OUTCOME",
        "SOURCE_STATUS",
        "PYTHON_OUTCOME",
        "INSTALL_STATUS",
        "FIXTURE_STATUS",
        "TEST_STATUS",
        "HASH_STATUS",
        "UPLOAD_OUTCOME",
    ):
        assert marker in text
