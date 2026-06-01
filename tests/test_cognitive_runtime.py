from __future__ import annotations

import json

from autonomous_vnext.cognitive_runtime import report_to_dict, run_cognitive_cycle, write_report


def test_cognitive_cycle_produces_stable_report() -> None:
    report = run_cognitive_cycle("safe tensor evidence mission")

    assert report.backbone["rank"] == 6
    assert report.backbone["total_dimension"] == 1152
    assert report.mesh_consistent
    assert not report.mesh_conflicts
    assert report.goal_energy > 0
    assert report.retrieved_memory[0]["record_id"] in {
        "evidence_reporting",
        "mission_projection",
        "risk_governance",
        "tensor_backbone",
    }
    assert set(report.uncertainty) == {"beliefs", "environment", "goals", "risks"}


def test_cognitive_cycle_accepts_observation_override() -> None:
    report = run_cognitive_cycle(
        "risk mission",
        observations={
            "beliefs": (1.0, 0.0, 0.0, 0.0),
            "risks": (0.0, 1.0, 0.0),
            "environment": (0.0, 0.0, 1.0),
        },
    )

    assert report.state["risks"][1] > report.state["risks"][0]
    assert report.uncertainty["risks"]["confidence"] > 0.0


def test_write_report_round_trip(tmp_path) -> None:
    report = run_cognitive_cycle("mission evidence")
    output = tmp_path / "report.json"

    write_report(report, output)

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data == report_to_dict(report)
