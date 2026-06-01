from __future__ import annotations

import json
from pathlib import Path

from autonomous_vnext.core import AuditLogWriter, PolicyEvaluator
from autonomous_vnext.executor import (
    ExecutionCheck,
    build_evidence_report,
    run_execution_checks,
)


def test_run_execution_checks_and_audit(tmp_path: Path) -> None:
    log_path = tmp_path / "audit.jsonl"
    logger = AuditLogWriter(log_path)
    policy = PolicyEvaluator(allow_commands={"python"})

    checks = [
        ExecutionCheck(name="smoke-pass", command="python -c \"print('ok')\""),
        ExecutionCheck(name="smoke-fail", command="python -c \"import sys; sys.exit(3)\""),
    ]

    results = run_execution_checks(checks, policy=policy, logger=logger)
    assert len(results) == 2
    assert results[0].passed is True
    assert results[1].passed is False

    log_lines = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(log_lines) == 2
    first = json.loads(log_lines[0])
    assert first["step_id"] == "exec-1"


def test_build_evidence_report(tmp_path: Path) -> None:
    checks = [
        ExecutionCheck(name="a", command="python -c 'print(1)'"),
    ]
    logger = AuditLogWriter(tmp_path / "audit.jsonl")
    policy = PolicyEvaluator(allow_commands={"python"})
    exec_results = run_execution_checks(checks, policy=policy, logger=logger)
    report = build_evidence_report(exec_results)
    assert report["summary"]["total_checks"] == 1
    assert report["summary"]["passed"] == 1
