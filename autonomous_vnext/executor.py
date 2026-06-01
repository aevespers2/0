from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Iterable

from autonomous_vnext.core import AuditLogWriter, PolicyEvaluator, utc_now_iso


@dataclass(frozen=True)
class ExecutionCheck:
    name: str
    command: str


@dataclass(frozen=True)
class ExecutionResult:
    name: str
    command: str
    returncode: int
    passed: bool
    stdout: str
    stderr: str


DEFAULT_CHECKS: tuple[ExecutionCheck, ...] = (
    ExecutionCheck(name="tests", command="pytest -q"),
)


def run_execution_checks(
    checks: Iterable[ExecutionCheck],
    *,
    policy: PolicyEvaluator,
    logger: AuditLogWriter,
) -> list[ExecutionResult]:
    """Run test/lint/security hooks under policy control and audit every step."""
    results: list[ExecutionResult] = []

    for idx, check in enumerate(checks, start=1):
        policy.require_allowed(check.command)
        proc = subprocess.run(check.command, shell=True, capture_output=True, text=True)
        result = ExecutionResult(
            name=check.name,
            command=check.command,
            returncode=proc.returncode,
            passed=proc.returncode == 0,
            stdout=proc.stdout,
            stderr=proc.stderr,
        )
        results.append(result)

        logger.append(
            {
                "timestamp": utc_now_iso(),
                "actor": "executor",
                "step_id": f"exec-{idx}",
                "command_or_patch": check.command,
                "inputs": [check.name],
                "result": "pass" if result.passed else "fail",
                "evidence": [f"stdout:{len(result.stdout)}", f"stderr:{len(result.stderr)}"],
                "rollback": "N/A for read-only verification checks",
            }
        )

    return results


def build_evidence_report(results: Iterable[ExecutionResult]) -> dict[str, object]:
    result_list = list(results)
    total = len(result_list)
    passed = sum(1 for r in result_list if r.passed)
    failed = total - passed
    return {
        "summary": {
            "total_checks": total,
            "passed": passed,
            "failed": failed,
            "status": "pass" if failed == 0 else "fail",
        },
        "checks": [
            {
                "name": r.name,
                "command": r.command,
                "returncode": r.returncode,
                "passed": r.passed,
            }
            for r in result_list
        ],
    }
