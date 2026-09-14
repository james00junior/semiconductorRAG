# Production Roadmap

## Status

| Phase | Area | Status |
|---|---|---|
| 0 | Engineering foundation | In progress |
| 1 | Data platform | Planned |
| 2 | Production chunking | Planned |
| 3 | Embedding pipeline | Planned |
| 4 | Vector Search | Planned |
| 5 | Retrieval quality | Planned |
| 6 | RAG application | Planned |
| 7 | Evaluation | Planned |
| 8 | MLflow tracking | Planned |
| 9 | Databricks orchestration | Planned |
| 10 | Serving | Planned |
| 11 | Observability and security | Planned |
| 12 | Production release | Planned |

## Phase sequence

### Phase 0 — Engineering foundation

Repository structure, documentation, package configuration, tests, CI and development conventions.

### Phase 1 — Data platform

Build deterministic ingestion, Bronze/Silver Delta layers, validation and lineage.

### Phase 2 — Chunking

Extract notebook chunking logic into tested production code and version the strategy.

### Phase 3 — Embeddings

Build incremental embedding generation and persistence. Unchanged chunks must not be embedded again.

### Phase 4 — Vector Search

Create and validate the Databricks vector index from the retrieval-ready Delta data.

### Phase 5 — Retrieval quality

Establish semantic baseline, then evaluate hybrid retrieval and reranking only where metrics justify them.

### Phase 6 — RAG application

Separate retrieval, prompt construction, generation, evidence handling and citation logic.

### Phase 7 — Evaluation

Introduce a fixed benchmark and retrieval/generation quality gates.

### Phase 8 — MLflow

Track reproducible RAG experiments and quality/latency metrics.

### Phase 9 — Jobs

Orchestrate ingestion through evaluation with Databricks Workflows and Asset Bundles.

### Phase 10 — Serving

Expose a stable research endpoint and deploy it through the same controlled lifecycle used for other production resources.

### Phase 11 — Observability/security

Add operational telemetry, access controls, secret handling and auditability based on actual deployment requirements.

### Phase 12 — Production release

Promote validated artifacts through dev → staging → production with explicit release controls and post-deployment verification.

## Engineering gate

A phase cannot be marked complete because code exists. It is complete when implementation, tests, CI, documentation and deployment evidence satisfy that phase's acceptance criteria.
