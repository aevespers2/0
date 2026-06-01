from __future__ import annotations

from pathlib import Path

from autonomous_vnext.audit import AuditLogWriter
from autonomous_vnext.executor import ExecutionCheck, ExecutionResult, build_evidence_report, run_execution_checks
from autonomous_vnext.policy import PolicyEvaluator


def test_executor_records_pass_fail_and_blocked(tmp_path: Path) -> None:
    audit_path = tmp_path / "audit.jsonl"
    policy = PolicyEvaluator(allowed_command_prefixes=(("python3", "-c"),))
    results = run_execution_checks(
        [
            ExecutionCheck("step-001", "python3 -c 'print(123)'"),
            ExecutionCheck("step-002", "python3 -c 'raise SystemExit(2)'"),
            ExecutionCheck("step-003", "git push"),
        ],
        policy=policy,
        audit=AuditLogWriter(audit_path),
        mission_id="mission-001",
        cwd=tmp_path,
    )
    assert [result.status for result in results] == ["pass", "fail", "blocked"]
    assert len(audit_path.read_text(encoding="utf-8").splitlines()) == 3


def test_evidence_report_counts_statuses() -> None:
    results = [
        ExecutionResult("step-001", "cmd", "pass", 0, "", ""),
        ExecutionResult("step-002", "cmd", "blocked", None, "", ""),
        ExecutionResult("step-003", "cmd", "blocked", None, "", ""),
    ]
    report = build_evidence_report(results)
    assert report["status_counts"] == {"blocked": 2, "pass": 1}
