# Scientific Repository Roadmap: 2026 Composable Discovery Stack

This roadmap turns the proposal set into an actionable portfolio of open-source
repositories for autonomous scientific discovery. The emphasis is composability:
each domain engine can stand alone, while shared orchestration, benchmarking,
and iterative-refinement layers let teams combine them into closed-loop research
systems.

## Portfolio Principles

- **Design--simulate--optimize loops:** every repository should expose an
  explicit loop from candidate generation to simulation, scoring, uncertainty,
  and next-candidate proposal.
- **Reproducible benchmarks first:** ship small permissively licensed benchmark
  datasets, schema documentation, and baseline notebooks before scaling to large
  datasets.
- **Composable engines:** domain packages should export stable Python APIs and
  CLI entry points so orchestration layers can drive them without bespoke glue.
- **Uncertainty-aware outputs:** predictions should report confidence intervals,
  calibration metadata, or ensemble variance rather than single-point scores.
- **Human-in-the-loop safety:** scientific recommendations should be framed as
  research candidates, not clinical, manufacturing, or deployment instructions.

## Refined Repository Concepts

### OpenPrimeForge

OpenPrimeForge should evolve from a static gene-editing toolkit into a
closed-loop prime-editing design system.

**Core modules**

- `openprimeforge.design`: pegRNA, nicking guide, editor, and template proposal
  objects.
- `openprimeforge.modalities`: support for template-jumping, split prime editor
  systems, and prime-assembly-style large-insertion workflows.
- `openprimeforge.population`: adapters for population-scale variant catalogs and
  cohort-aware target prioritization.
- `openprimeforge.reasoning`: iterative hypothesis-refinement engine that updates
  guide/editor/template choices from observed edit distributions.
- `openprimeforge.benchmarks`: loaders for clinical, indel, and prime-editing
  outcome datasets.

**Minimum viable milestone**

1. Define immutable candidate and outcome schemas.
2. Implement deterministic baseline pegRNA scoring.
3. Add a simulated edit-distribution predictor with calibrated uncertainty.
4. Provide a benchmark runner that emits JSON and Markdown reports.

### PhaseSpaceQML

PhaseSpaceQML should bridge fundamental phase-space quantum machine learning and
applied climate, materials, and quantum-biology workflows.

**Core modules**

- `phasespaceqml.layers`: differentiable phase-space feature maps and
  quantum-inspired kernels.
- `phasespaceqml.hybrids`: adapters for climate or materials emulators, including
  TimesFM-style time-series backbones and sheaf-constrained predictors.
- `phasespaceqml.materials2d`: notebooks and utilities for stacked 2D material
  quantum-effect discovery.
- `phasespaceqml.open_systems`: exploratory noisy open-system models for
  biological environments.
- `phasespaceqml.eval`: ablations comparing classical, hybrid, and
  quantum-inspired layers.

**Minimum viable milestone**

1. Implement a small differentiable phase-space layer.
2. Add a time-series emulator example using synthetic climate-like data.
3. Provide a 2D-material toy benchmark with reproducible seeds.
4. Publish notebooks that show when the hybrid layer helps or fails.

### SheafTimes / ClimateSheafFM

SheafTimes should extend the existing rainfall-sheaf lineage into a clean package
for foundation-model embeddings plus physical-consistency refinement.

**Core modules**

- `sheaf_times.embeddings`: adapters for TimesFM-like embeddings and other
  time-series foundation model representations.
- `sheaf_times.layers`: sheaf-Laplacian refinement blocks over stations, grid
  cells, watersheds, or atmospheric regions.
- `sheaf_times.search`: gradient-based or discrete structure search over
  connection weights, lag features, and graph topology.
- `sheaf_times.eval.pnw`: Pacific Northwest and Western US evaluation suites for
  atmospheric rivers, extreme precipitation, and backtesting.
- `sheaf_times.datasets`: tiny benchmark package with reanalysis features and
  satellite-derived labels.

**Minimum viable milestone**

1. Create a framework-neutral embedding interface.
2. Implement one sheaf refinement layer with unit tests on synthetic graphs.
3. Add an atmospheric-river binary classification notebook.
4. Report calibration, lead-time skill, and failure cases.

### SciIterate

SciIterate should become the orchestration hub that can drive every domain engine
through active learning and self-driving discovery loops.

**Core modules**

- `sciiterate.engines`: protocol definitions for domain engines such as gene
  editing, mRNA design, materials, climate, and quantum workflows.
- `sciiterate.loop`: active-learning state machine for propose, simulate,
  evaluate, refine, and archive steps.
- `sciiterate.policies`: budget, safety, provenance, and human-approval gates.
- `sciiterate.memory`: structured experiment memory with dataset/version hashes.
- `sciiterate.reports`: audit-friendly run cards, uncertainty summaries, and
  benchmark comparisons.

**Minimum viable milestone**

1. Define the engine protocol and JSON run record.
2. Implement a random-search baseline and an uncertainty-sampling strategy.
3. Add one mock engine and one real domain adapter.
4. Emit reproducible experiment cards suitable for pull-request review.

## New High-Value Repository Proposals

### 1. mRNAForge / OpenmRNAid-Next

mRNAForge should connect mRNA sequence design with delivery optimization rather
than treating coding sequence design and lipid nanoparticle formulation as
separate tasks.

**Repository goals**

- Unify UTR selection, CDS codon choice, uridine-content constraints,
  nucleoside-analog annotations, secondary-structure prediction, and
  immunogenicity scoring.
- Provide generative-model backends for transformer, diffusion, and simpler
  baseline samplers, with fine-tuning hooks for private experimental data.
- Integrate delivery-design features such as ionizable lipid descriptors,
  formulation parameters, and active-learning hooks for automated screening.
- Offer visualization inspired by existing mRNA optimization dashboards, while
  adding uncertainty and dataset-provenance panels.
- Ship benchmark schemas for optimized sequences, measured expression, stability,
  immune activation, and delivery outcomes.

**Suggested package layout**

```text
mrnaforge/
  design/          # candidate schemas and constraints
  sequence/        # codon, UTR, analog, and structure utilities
  models/          # transformer, diffusion, ensemble, and baseline wrappers
  delivery/        # LNP descriptors and formulation search spaces
  active_learning/ # proposal policies and closed-loop state
  viz/             # dashboard components and report renderers
  benchmarks/      # loaders, metrics, and reproducibility harness
```

**First three issues**

1. Define `MRNACandidate`, `DeliveryFormulation`, and `AssayOutcome` schemas.
2. Implement baseline codon optimization plus structure-aware scoring.
3. Build a toy active-learning loop that jointly proposes sequence and delivery
   candidates against a synthetic assay oracle.

### 2. PerovForge / SolarSheaf

PerovForge should move perovskite tooling from single-device simulation toward
closed-loop durability and self-healing materials discovery.

**Repository goals**

- Wrap or interoperate with drift-diffusion solvers, while adding ion migration,
  transfer-matrix optics, and self-healing additive abstractions.
- Model recovery trajectories after mechanical, thermal, moisture, or chemical
  stress.
- Add explainable-AI modules that link processing variables and
  photoluminescence-derived features to efficiency, degradation, and recovery.
- Explore sheaf-constrained or hybrid quantum/classical layers for multi-scale
  grain-boundary, interface, ion-dynamics, and mechanical-recovery structure.
- Provide both an interactive frontend and batch parameter-sweep interface.

**Suggested package layout**

```text
perovforge/
  physics/       # drift-diffusion, ion migration, and optics adapters
  healing/       # self-healing polymer/additive candidate models
  processing/    # processing, PL, and fabrication metadata schemas
  xai/           # interpretable models and attribution reports
  optimization/  # sweeps, Bayesian optimization, and generative search
  frontend/      # optional Vite/TypeScript simulator UI
  benchmarks/    # processing-performance-healing trajectories
```

**First three issues**

1. Define processing, device-stack, stress-test, and recovery-curve schemas.
2. Add a solver adapter interface with a deterministic toy drift-diffusion model.
3. Implement a batch sweep that ranks additive candidates by efficiency-retention
   and recovery metrics.

### 3. Ecosystem Accelerators

#### Awesome-Scientific-Repos-2026

A curated list should map the active ecosystem across gene editing, mRNA,
quantum/materials, climate, perovskites, self-healing materials, and
self-driving labs. It should include starter-kit recipes that compose multiple
repositories into end-to-end workflows.

#### SciReasoningHub

SciReasoningHub should provide a shared library of iterative-refinement modules
that can be imported by OpenPrimeForge, mRNAForge, PerovForge, SheafTimes, and
SciIterate.

**Shared primitives**

- Candidate perturbation and proposal kernels.
- Gradient-style structure refinement over graph, sheaf, lag, or formulation
  parameters.
- Hypothesis ledgers that track proposed mechanisms, supporting evidence,
  rejected alternatives, and next experiments.
- Calibration utilities for ensemble and bootstrap uncertainty.

## Recommended Build Order

1. **SciReasoningHub:** implement shared candidate, hypothesis, and uncertainty
   primitives once.
2. **SciIterate:** define the orchestration protocol and run-card format that all
   domain engines can satisfy.
3. **SheafTimes:** leverage the existing rainfall-sheaf direction and create an
   immediately testable climate benchmark.
4. **mRNAForge:** prototype schemas and a synthetic closed-loop sequence plus
   delivery benchmark.
5. **PerovForge:** add solver adapters and durability-focused benchmarks.
6. **OpenPrimeForge and PhaseSpaceQML:** deepen once the shared reasoning and
   orchestration APIs are stable.

## Cross-Repository Integration Pattern

Each domain repository should expose a small engine object that SciIterate can
call:

```python
class DiscoveryEngine:
    def propose(self, state, budget): ...
    def simulate(self, candidates): ...
    def score(self, candidates, observations): ...
    def refine(self, state, observations): ...
    def report(self, run): ...
```

This protocol keeps the ecosystem flexible: mRNAForge can optimize sequence and
LNP pairs, PerovForge can optimize device stacks and additives, SheafTimes can
search sheaf structures for weather extremes, and OpenPrimeForge can refine
pegRNA/editor/template combinations.

## Near-Term Deliverables

- A repository-template cookiecutter for domain engines.
- JSON schemas for candidate, observation, uncertainty, and run-card records.
- One synthetic benchmark per domain to make CI fast and deterministic.
- A small public roadmap board with labels for `schema`, `baseline`, `benchmark`,
  `dashboard`, `active-learning`, and `safety`.
- Documentation that distinguishes research ideation from validated clinical,
  manufacturing, or deployment guidance.
