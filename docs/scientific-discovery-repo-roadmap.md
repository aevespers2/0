# Scientific Discovery Repository Roadmap

## Purpose

This roadmap translates recent scientific-research themes into concrete,
open-source repository tracks that fit Autonomous vNext's constrained,
auditable builder-agent model. It prioritizes modular Python-first tooling,
clear benchmark contracts, provenance capture, and human-in-the-loop safety for
high-impact scientific domains.

## Recommended First Focus: ClimateSheafFM

ClimateSheafFM is the best first project to refine because it is immediately
useful, lower-risk than therapeutic design, and naturally aligned with this
repository's existing sheaf consistency, tensor memory, uncertainty, and
federation primitives.

### Why Start Here

- It targets synthetic and retrospective research benchmarks for rainfall,
  precipitation, atmospheric rivers, and other extreme-event scenarios.
- It can be built around public reanalysis and satellite datasets before any
  sensitive or proprietary data is required.
- It supports reproducible benchmarks and visible progress through notebooks,
  metrics, and maps.
- It provides a safe proving ground for combining foundation time-series models,
  sheaf constraints, topological features, and uncertainty reporting.

## Project Definition

ClimateSheafFM is a modular research package for physically constrained,
interpretable spatiotemporal weather and climate benchmarking. The initial scope
is synthetic and retrospective rainfall and extreme-precipitation evaluation,
with research extension points for drought, heat stress, renewable-energy data,
and crop-resilience studies. It is not an operational forecasting or emergency-
response system.

### Core Modules

1. Data adapters for public climate products such as ERA5-style reanalysis,
   satellite precipitation products, station observations, and regional masks.
2. Foundation-model adapters that expose time-series embeddings through a common
   interface without hard-coding a single upstream model.
3. Sheaf refinement layers that enforce local consistency across grid cells,
   watersheds, storm corridors, lag windows, or sensor networks.
4. Topological feature extractors for threshold-light detection of atmospheric
   rivers, blocking patterns, and persistent precipitation structures.
5. Uncertainty and calibration reports for predictive intervals under benchmark
   conditions, regional bias, and event-level reliability.
6. Benchmark runners that produce reproducible metrics, artifacts, and audit
   records for each experiment.

## Minimal Viable Repository

The MVP should avoid overpromising quantum acceleration or self-driving lab
features. Instead, it should establish a dependable baseline that other tracks
can reuse.

### Milestone 1: Scaffolding

- Create a typed Python package with data, model, sheaf, topology, evaluation,
  and visualization subpackages.
- Add synthetic toy datasets that mimic gridded rainfall and storm corridors.
- Provide an end-to-end notebook and CLI smoke test.
- Define an experiment manifest schema for dataset, model, metric, and artifact
  provenance.

### Milestone 2: Sheaf-Constrained Baseline

- Implement a simple graph/sheaf Laplacian refinement layer over grid cells.
- Compare naive persistence, classical statistical baselines, and a lightweight
  neural model with and without sheaf refinement.
- Emit calibration and event-detection metrics into a machine-readable report.

### Milestone 3: Foundation-Model Adapter

- Add an adapter interface for external time-series foundation models.
- Keep the default implementation dependency-light by using synthetic embeddings
  or optional extras.
- Document how to plug in TimesFM-style or transformer-based forecasters without
  making them mandatory runtime dependencies.

### Milestone 4: Extreme-Event Workflow

- Add atmospheric-river-style corridor detection on toy and public sample data.
- Include topological summaries, connected-component tracks, and event-level
  verification metrics.
- Publish a small benchmark card describing data assumptions, limitations, and
  expected outputs.

## Safety And Governance

Climate tools can influence public planning decisions, so the repository should
make uncertainty and limitations visible from the start.

- Label outputs as research-only benchmark results unless independently validated.
- State that outputs are not intended for emergency response, public planning, or
  operational forecasting.
- Track dataset lineage, preprocessing choices, and model configuration.
- Include regional performance slices to expose bias or failure modes.
- Require benchmark reports for changes that alter model behavior.
- Keep destructive or remote actions outside automated workflows by default.

## Future Extensions

After the ClimateSheafFM baseline is stable, the same repository patterns can
support additional scientific tracks:

- PhaseSpaceQML for optional quantum or quantum-inspired scientific-computing
  experiments.
- OpenPrimeForge as a higher-governance therapeutic-design track with stricter
  safety, ethics, and validation gates.
- SciIterate as a cross-domain closed-loop experimentation layer that consumes
  benchmark reports and proposes auditable next experiments.

## Immediate Next Step

Create a small `climatesheaffm` package skeleton with synthetic rainfall data,
a sheaf-refinement baseline, and a reproducible benchmark command. This turns
the concept into a testable artifact while preserving the repository's emphasis
on bounded, reversible, evidence-backed work.
