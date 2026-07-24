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
        {"id": 2, "workflow_id": 10, "head_sha": "abc", "event": "pull_request",
         "created_at": "2026-07-18T01:00:00Z", "status": "completed", "conclusion": "success"},
        {"id": 1, "workflow_id": 10, "head_sha": "abc", "event": "pull_request",
         "created_at": "2026-07-18T00:00:00Z", "status": "completed", "conclusion": "failure"},
    ]
    latest = health.latest_workflow_states(runs)
    assert len(latest) == 1
    assert latest[0]["conclusion"] == "success"


def test_workflow_states_remain_separate_across_heads():
    runs = [
        {"id": 2, "workflow_id": 10, "head_sha": "new", "event": "pull_request",
         "created_at": "2026-07-18T01:00:00Z", "status": "completed", "conclusion": "success"},
        {"id": 1, "workflow_id": 10, "head_sha": "old", "event": "pull_request",
         "created_at": "2026-07-18T00:00:00Z", "status": "completed", "conclusion": "failure"},
    ]
    assert {(item["head_sha"], item["conclusion"]) for item in health.latest_workflow_states(runs)} == {
        ("new", "success"), ("old", "failure")
    }


def test_exact_head_check_requires_at_least_one_check():
    assert health.exact_head_check_problem([]) == (
        "missing", "no check run is attached to the exact head"
    )


def test_exact_head_check_rejects_pending_and_skipped_states():
    assert health.exact_head_check_problem(
        [{"id": 1, "name": "CI", "status": "in_progress", "conclusion": None}]
    )[0] == "pending"
    problem = health.exact_head_check_problem(
        [{"id": 2, "name": "CI", "status": "completed", "conclusion": "skipped"}]
    )
    assert problem and problem[0] == "failed" and "CI=skipped" in problem[1]


def test_exact_head_check_accepts_only_completed_successes():
    checks = [
        {"id": 3, "name": "Unit", "status": "completed", "conclusion": "success"},
        {"id": 4, "name": "Security", "status": "completed", "conclusion": "success"},
    ]
    assert health.exact_head_check_problem(checks) is None


def test_mergeability_uses_authoritative_detail_and_bounded_retry():
    payloads = iter([{"mergeable": None}, {"mergeable": None}, {"mergeable": False}])
    calls, sleeps = [], []
    result = health.resolve_mergeable(
        "aevespers2/example", 7,
        requester=lambda path: calls.append(path) or next(payloads),
        sleeper=sleeps.append,
    )
    assert result is False
    assert calls == ["/repos/aevespers2/example/pulls/7"] * 3
    assert sleeps == [2, 2]


def test_pagination_collects_until_short_page():
    page_values = {1: list(range(100)), 2: [100, 101]}
    def requester(path):
        return page_values[int(path.rsplit("page=", 1)[1])]
    assert health.paginated("/items?state=open", requester=requester) == list(range(102))


def test_paginated_key_collects_dictionary_pages():
    page_values = {1: {"workflow_runs": list(range(100))}, 2: {"workflow_runs": [100]}}
    def requester(path):
        return page_values[int(path.rsplit("page=", 1)[1])]
    assert health.paginated_key("/runs", "workflow_runs", requester=requester) == list(range(101))


def test_workflow_permissions_detect_write_all_and_pull_request_target_write():
    source = """on:
  pull_request_target:
permissions: write-all
jobs:
  x:
    permissions:
      contents: write
"""
    problems = dict(health.workflow_permission_problems(source))
    assert "unsafe_workflow_permissions" in problems
    assert "unsafe_pull_request_target_permissions" in problems


def test_workflow_permissions_accept_explicit_read_only():
    source = """on:
  pull_request:
permissions:
  contents: read
jobs: {}
"""
    assert health.workflow_permission_problems(source) == []


def test_automatic_privileged_workflow_is_flagged():
    source = """on:
  schedule:
    - cron: '0 0 * * *'
permissions:
  contents: write
"""
    assert "privileged_automatic_workflow" in dict(health.workflow_permission_problems(source))


def test_mutable_action_references_require_full_sha():
    source = """steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@0123456789abcdef0123456789abcdef01234567
  - uses: ./local-action
"""
    assert health.mutable_action_references(source) == ["actions/checkout@v4"]


def test_markdown_targets_resolve_and_ignore_external_and_parent_escape():
    source = """[Guide](docs/guide.md)
[Local](./local.md#part)
[Web](https://example.com)
[Anchor](#section)
[Escape](../outside.md)
"""
    assert health.markdown_targets(source, "README.md") == ["docs/guide.md", "local.md"]


def test_semantic_fingerprint_is_stable_and_sensitive():
    item = health.Finding("high", "a/b", "failed_ci", "x", "u", "id")
    assert health.semantic_fingerprint([item], []) == health.semantic_fingerprint([item], [])
    assert health.semantic_fingerprint([item], []) != health.semantic_fingerprint(
        [health.Finding("high", "a/b", "failed_ci", "y", "u", "id")], []
    )


def test_render_markdown_contains_machine_readable_fingerprint():
    report = {
        "portfolio_fingerprint": "sha256:" + "a" * 64,
        "finding_count": 0,
        "errors": [],
        "findings": [],
    }
    assert "<!-- portfolio_fingerprint=sha256:" in health.render_markdown(report)


def test_pagination_rejects_non_list_payload():
    with pytest.raises(ValueError, match="did not return a list"):
        health.paginated("/items", requester=lambda path: {"items": []})


def test_pr_head_workflow_scan_reports_only_changed_unsafe_sources(monkeypatch):
    path = ".github/workflows/ci.yml"
    baseline = """on:
  pull_request:
permissions:
  contents: read
jobs: {}
"""
    changed = """on:
  pull_request_target:
permissions: write-all
jobs:
  x:
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
"""
    content_requests = []
    text_requests = []
    monkeypatch.setattr(
        health,
        "content",
        lambda request_path: content_requests.append(request_path) or ([{"path": path}]
        if "/contents/.github/workflows?" in request_path
        else None),
    )
    monkeypatch.setattr(
        health,
        "text",
        lambda request_path: text_requests.append(request_path) or changed,
    )
    findings, sources = health.scan_workflows(
        "aevespers2/example",
        "a" * 40,
        "PR #7@aaaaaaaaaaaa",
        baseline_sources={path: baseline},
        source_repo="contributor/example",
    )
    assert sources == {path: changed}
    assert {finding.kind for finding in findings} == {
        "unsafe_workflow_permissions",
        "unsafe_pull_request_target_permissions",
        "mutable_action_reference",
    }
    assert all("a" * 40 in finding.identity for finding in findings)
    assert all("contributor/example" in finding.identity for finding in findings)
    assert all("github.com/contributor/example/blob/" in finding.url for finding in findings)
    assert content_requests == [
        "/repos/contributor/example/contents/.github/workflows?ref=" + "a" * 40
    ]
    assert text_requests == [
        "/repos/contributor/example/contents/.github/workflows/ci.yml?ref=" + "a" * 40
    ]

    monkeypatch.setattr(health, "text", lambda request_path: baseline)
    inherited, sources = health.scan_workflows(
        "aevespers2/example",
        "b" * 40,
        "PR #8@bbbbbbbbbbbb",
        baseline_sources={path: baseline},
        source_repo="contributor/example",
    )
    assert inherited == []
    assert sources == {path: baseline}


def test_artifact_check_uses_workflow_source_from_run_exact_head():
    path = ".github/workflows/pr-only.yml"
    run = {
        "id": 44,
        "workflow_id": 9,
        "head_sha": "p" * 40,
        "status": "completed",
        "conclusion": "success",
        "name": "PR-only validation",
        "html_url": "https://example.invalid/run/44",
    }
    calls = []
    def requester(request_path):
        calls.append(request_path)
        if request_path.endswith("/actions/workflows/9"):
            return {"path": path}
        if request_path.endswith("/actions/runs/44/artifacts?per_page=1"):
            return {"total_count": 0}
        raise AssertionError(request_path)

    findings = health.scan_artifacts(
        "aevespers2/example",
        {"p" * 40},
        [run],
        {
            "d" * 40: {},
            "p" * 40: {
                path: "steps:\n  - uses: actions/upload-artifact@" + "a" * 40
            },
        },
        requester=requester,
    )
    assert len(findings) == 1
    assert findings[0].kind == "missing_expected_artifact"
    assert calls == [
        "/repos/aevespers2/example/actions/workflows/9",
        "/repos/aevespers2/example/actions/runs/44/artifacts?per_page=1",
    ]
