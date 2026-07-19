import importlib.util
import json
from pathlib import Path

MODULE_PATH = Path("scripts/gods_control.py")
spec = importlib.util.spec_from_file_location("gods_control", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def sample_report() -> dict:
    return {
        "findings": [
            {"severity": "high", "repo": "aevespers2/QSO-STUDIO", "kind": "failed_ci", "summary": "Consent Capacity Lock failed", "url": "https://example.invalid/run"},
            {"severity": "medium", "repo": "aevespers2/QuantumStateObjects", "kind": "missing_exact_head_ci", "summary": "No exact-head docs build"},
        ],
        "errors": [],
    }


def test_prometheus_output_is_bounded(tmp_path: Path) -> None:
    output = tmp_path / "portfolio.prom"
    module.prometheus(sample_report(), output)
    text = output.read_text(encoding="utf-8")
    assert 'channel="Gods"' in text
    assert 'repository="aevespers2/QSO-STUDIO"' in text
    assert "example.invalid" not in text
    assert "qso_portfolio_release_ready{channel=\"Gods\"} 0" in text


def test_jira_dry_run_deduplicates_by_stable_label(monkeypatch) -> None:
    monkeypatch.setenv("JIRA_BASE_URL", "https://example.atlassian.net")
    monkeypatch.setenv("JIRA_PROJECT_KEY", "QSO")
    monkeypatch.setenv("JIRA_EMAIL", "owner@example.com")
    monkeypatch.setenv("JIRA_API_TOKEN", "not-used-in-dry-run")
    actions = module.jira_sync(sample_report(), dry_run=True)
    assert len(actions) == 2
    assert actions[0]["label"].startswith("gods-aevespers2-qso-studio-failed-ci")
    assert all(action["existing"] is False for action in actions)


def test_config_uses_gods_channel() -> None:
    data = json.loads(Path("integrations/gods/config.json").read_text(encoding="utf-8"))
    assert data["channel"] == "Gods"
    assert data["release_gate"]["automatic_merge"] is False
    assert data["prometheus"]["allow_commit_shas"] is False
