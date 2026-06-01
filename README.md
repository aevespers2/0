# 0

Installs needed for various projects.

## Autonomous Agent Spec

This repository includes a concrete specification for an auditable autonomous engineering agent:

- [`AUTONOMOUS_VNEXT.md`](./AUTONOMOUS_VNEXT.md)

### What's new in the spec
- System architecture across mission, planning, execution, safety, collaboration, and learning.
- MVP data model with JSON examples.
- Risk scoring rubric and explicit approval gates.
- Phase-0 implementation checklist to start building immediately.

## Implemented now
- [`mission_contract.schema.json`](./mission_contract.schema.json)
- [`action_record.schema.json`](./action_record.schema.json)

## Runtime MVP primitives
- [`autonomous_vnext/core.py`](./autonomous_vnext/core.py)
- [`tests/test_core.py`](./tests/test_core.py)

## Test
- Run `pytest -q` from repo root.

## ITensor integration
- [`autonomous_vnext/itensor_adapter.py`](./autonomous_vnext/itensor_adapter.py) provides an ITensor-gated scoring adapter for plan ranking.
- Install Python ITensor bindings in your environment to enable runtime scoring.

- [`autonomous_vnext/cognitive_hilbert.py`](./autonomous_vnext/cognitive_hilbert.py) models high-dimensional cognitive Hilbert spaces with ITensor-gated runtime hooks.

- [`autonomous_vnext/executor.py`](./autonomous_vnext/executor.py) adds policy-gated execution checks plus evidence report generation.
- [`tests/test_executor.py`](./tests/test_executor.py) validates check execution, audit logging, and report output.
