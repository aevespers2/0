from __future__ import annotations

import sys

import pytest

from autonomous_vnext.cognitive_hilbert import build_cognitive_backbone, require_itensor_backbone
from autonomous_vnext.itensor_adapter import ITensorUnavailableError


def test_backbone_dimension_composition() -> None:
    backbone = build_cognitive_backbone([("intent", 2), ("context", 3), ("plan", 5)])
    assert backbone.rank == 3
    assert backbone.total_dimension == 30
    assert backbone.labels == ("intent", "context", "plan")


def test_backbone_rejects_invalid_dimension() -> None:
    with pytest.raises(ValueError):
        build_cognitive_backbone([("intent", 1)])


def test_itensor_backbone_gate_unavailable(monkeypatch) -> None:
    monkeypatch.setitem(sys.modules, "itensor", None)
    backbone = build_cognitive_backbone([("intent", 2)])
    with pytest.raises(ITensorUnavailableError):
        require_itensor_backbone(backbone)


def test_itensor_backbone_gate_mocked(monkeypatch) -> None:
    class FakeITensor:
        pass

    monkeypatch.setitem(sys.modules, "itensor", FakeITensor())
    backbone = build_cognitive_backbone([("intent", 2)])
    assert require_itensor_backbone(backbone) is backbone
