from __future__ import annotations

import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from autonomous_vnext.audit import ActionRecord, AuditLogWriter
from autonomous_vnext.policy import PolicyEvaluator


@dataclass(frozen=True)
class ExecutionCheck:
    step_id: str
    command: str


@dataclass(frozen=True)
class ExecutionResult:
    step_id: str
    command: str
    status: str
    returncode: int | None
    stdout: str
    stderr: str


def run_execution_checks(
    checks: list[ExecutionCheck],
    policy: PolicyEvaluator,
    audit: AuditLogWriter,
    mission_id: str,
    cwd: Path,
) -> list[ExecutionResult]:
    results: list[ExecutionResult] = []
    for index, check in enumerate(checks, start=1):
        decision = policy.evaluate(check.command)
        if not decision.allowed:
            result = ExecutionResult(check.step_id, check.command, "blocked", None, "", decision.reason)
        else:
            completed = subprocess.run(
                check.command,
                cwd=cwd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            result = ExecutionResult(
                check.step_id,
                check.command,
                "pass" if completed.returncode == 0 else "fail",
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        results.append(result)
        audit.append(
            ActionRecord(
                action_id=f"act-{index:03d}",
                mission_id=mission_id,
                step_id=check.step_id,
                actor="autonomous_vnext",
                action_type="check",
                command=check.command,
                status=result.status,
                summary=f"{check.command}: {result.status}",
                details=asdict(result),
            )
        )
    return results


def build_evidence_report(results: list[ExecutionResult]) -> dict[str, object]:
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    return {
        "total": len(results),
        "status_counts": dict(sorted(counts.items())),
        "results": [asdict(result) for result in results],
    }
