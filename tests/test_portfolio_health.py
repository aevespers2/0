from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "portfolio_health.py"
SPEC = importlib.util.spec_from_file_location("portfolio_health", SCRIPT)
assert SPEC and SPEC.loader
health = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = health
SPEC.loader.exec_module(health)


def test_newer_success_supersedes_older_failure_for_same_workflow_head():
    runs = [
        {
            "id": 2,
            "workflow_id": 10,
            "head_sha": "abc",
            "event": "pull_request",
            "created_at": "2026-07-18T01:00:00Z",
            "status": "completed",
            "conclusion": "success",
        },
        {
            "id": 1,
            "workflow_id": 10,
            "head_sha": "abc",
            "event": "pull_request",
            "created_at": "2026-07-18T00:00:00Z",
            "status": "completed",
            "conclusion": "failure",
        },
    ]
    latest = health.latest_workflow_states(runs)
    assert len(latest) == 1
    assert latest[0]["conclusion"] == "success"


def test_workflow_states_remain_separate_across_heads():
    runs = [
        {
            "id": 2,
            "workflow_id": 10,
            "head_sha": "new",
            "event": "pull_request",
            "created_at": "2026-07-18T01:00:00Z",
            "status": "completed",
            "conclusion": "success",
        },
        {
            "id": 1,
            "workflow_id": 10,
            "head_sha": "old",
            "event": "pull_request",
            "created_at": "2026-07-18T00:00:00Z",
            "status": "completed",
            "conclusion": "failure",
        },
    ]
    latest = health.latest_workflow_states(runs)
    assert {(item["head_sha"], item["conclusion"]) for item in latest} == {
        ("new", "success"),
        ("old", "failure"),
    }


def test_exact_head_check_requires_at_least_one_check():
    assert health.exact_head_check_problem([]) == (
        "missing",
        "no check run is attached to the exact head",
    )


def test_exact_head_check_rejects_pending_and_skipped_states():
    pending = [{"id": 1, "name": "CI", "status": "in_progress", "conclusion": None}]
    assert health.exact_head_check_problem(pending)[0] == "pending"

    skipped = [{"id": 2, "name": "CI", "status": "completed", "conclusion": "skipped"}]
    problem = health.exact_head_check_problem(skipped)
    assert problem is not None
    assert problem[0] == "failed"
    assert "CI=skipped" in problem[1]


def test_exact_head_check_rejects_any_latest_failure():
    checks = [
        {"id": 3, "name": "Unit", "status": "completed", "conclusion": "success"},
        {"id": 4, "name": "Security", "status": "completed", "conclusion": "failure"},
    ]
    problem = health.exact_head_check_problem(checks)
    assert problem is not None
    assert problem[0] == "failed"
    assert "Security=failure" in problem[1]


def test_exact_head_check_accepts_only_completed_successes():
    checks = [
        {"id": 3, "name": "Unit", "status": "completed", "conclusion": "success"},
        {"id": 4, "name": "Security", "status": "completed", "conclusion": "success"},
    ]
    assert health.exact_head_check_problem(checks) is None


def test_mergeability_uses_authoritative_detail_and_bounded_retry():
    payloads = iter([{"mergeable": None}, {"mergeable": None}, {"mergeable": False}])
    calls = []
    sleeps = []

    def requester(path):
        calls.append(path)
        return next(payloads)

    result = health.resolve_mergeable(
        "aevespers2/example",
        7,
        requester=requester,
        sleeper=sleeps.append,
    )
    assert result is False
    assert calls == ["/repos/aevespers2/example/pulls/7"] * 3
    assert sleeps == [2.0, 2.0]


def test_mergeability_remains_unknown_after_five_attempts():
    calls = []
    result = health.resolve_mergeable(
        "aevespers2/example",
        7,
        requester=lambda path: calls.append(path) or {"mergeable": None},
        sleeper=lambda seconds: None,
    )
    assert result is None
    assert len(calls) == 5


def test_pagination_collects_until_short_page():
    pages = {
        1: list(range(100)),
        2: [100, 101],
    }

    def requester(path):
        page = int(path.rsplit("page=", 1)[1])
        return pages[page]

    assert health.paginated("/items?state=open", requester=requester) == list(range(102))


def test_pagination_rejects_non_list_payload():
    with pytest.raises(ValueError, match="did not return a list"):
        health.paginated("/items", requester=lambda path: {"items": []})
