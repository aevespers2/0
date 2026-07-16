# Repository 0 → Repository 1 Communication Flow

Repository 0 is the myelination layer. It routes tasks, assembles candidate work, and emits signed proposals and state-path observations. It does not decide canonical truth.

## Outbound Objects

Repository 0 may emit three object types:

1. **VTX proposal** — requests a specific operation or partition transition.
2. **Patch bundle** — contains candidate changes and a deterministic manifest.
3. **State-path event** — records how an agent, operator, tool, repository, branch, and artifact were traversed during the work.

## Muse Task Flow

```text
Operator intent
    |
    v
Muse task planner in Repository 0
    |
    +--> candidate patch/artifact
    +--> path observations
    +--> VTX proposal
             |
             v
Repository 1 verification gateway
             |
       +-----+-----+
       |           |
    reject      accept
       |           |
 quarantine    reviewed/canonical transition
                   |
                   v
             optional GitHub publication
```

## Path Observation Requirements

For each meaningful hop, Repository 0 records:

- actor identity;
- source and target repository;
- source and target partition;
- branch or state identifier;
- operation requested;
- payload digest;
- VTX envelope identifier;
- timestamp;
- local reason for choosing the route;
- expected next hop.

Repository 0 may calculate a preliminary peculiarity score, but Repository 1 performs the authoritative anomaly evaluation because Repository 0 must not grade its own behavior conclusively.

## Expected Muse Route

A normal Muse change should follow:

```text
0:working
  -> 0:proposal
  -> 1:quarantine
  -> 1:reviewed
  -> 1:canonical
  -> GitHub:proposal branch or approved publication target
  -> 1:audit receipt
```

Examples of unusual routes include:

- Muse attempting to address Repository 1 directly;
- skipping quarantine or review;
- changing repositories repeatedly without a task reason;
- publishing before an approval receipt exists;
- payload digest changes between hops;
- selecting a branch outside the allowed prefix;
- invoking a capability not present in the task envelope.

## Visual Graft

Repository 0 can render a live task path locally, while Repository 1 stores the signed durable history. A visualizer may graft the current in-progress route onto the canonical historical graph, clearly distinguishing:

- observed but unverified events;
- verified events;
- rejected or quarantined paths;
- corrective branches;
- canonical transitions;
- external publication and reconciliation receipts.

The visualization is a projection. Signed events and receipts remain authoritative.
