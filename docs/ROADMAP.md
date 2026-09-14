# Production Roadmap

## Status

| Phase | Area | Status |
|---|---|---|
| 0 | Engineering foundation | Frozen |
| 1 | Python package and CI foundation | Frozen |
| 2 | Patent ingestion and normalization | In progress |
| 3 | Production chunking | Planned |
| 4 | Embedding pipeline | Planned |
| 5 | Vector Search | Planned |
| 6 | Retrieval quality | Planned |
| 7 | RAG application | Planned |
| 8 | Evaluation | Planned |
| 9 | MLflow tracking | Planned |
| 10 | Databricks orchestration | Planned |
| 11 | Serving | Planned |
| 12 | Observability and security | Planned |
| 13 | Production release | Planned |

## Phase sequence

### Phase 0 — Engineering foundation

Repository structure, documentation, development conventions and initial production architecture.

### Phase 1 — Python package and CI foundation

Installable package, configuration, pinned development toolchain, unit tests and GitHub Actions quality gates.

### Phase 2 — Patent ingestion and normalization

Extract deterministic corpus inventory, parsing and validation from the research notebooks. Establish the canonical patent data contract while preserving the complete source text for lineage and retrieval compatibility.

### Phase 3 — Production chunking

Extract notebook chunking logic into tested production code and version the strategy. Chunk lineage must remain traceable to `document_id`.

### Phase 4 — Embeddings

Build incremental embedding generation and persistence. Unchanged chunks must not be embedded again.

### Phase 5 — Vector Search

Create and validate the Databricks vector index from retrieval-ready Delta data.

### Phase 6 — Retrieval quality

Establish a semantic baseline, then evaluate hybrid retrieval and reranking only where metrics justify them.

### Phase 7 — RAG application

Separate retrieval, prompt construction, generation, evidence handling and citation logic.

### Phase 8 — Evaluation

Introduce a fixed benchmark and retrieval/generation quality gates.

### Phase 9 — MLflow

Track reproducible RAG experiments and quality/latency metrics.

### Phase 10 — Databricks orchestration

Orchestrate ingestion through evaluation with Databricks Workflows and Asset Bundles, using a dedicated semiconductor production workspace and governed Unity Catalog resources.

### Phase 11 — Serving

Expose a stable research endpoint and deploy it through the same controlled lifecycle used for other production resources.

### Phase 12 — Observability/security

Add operational telemetry, access controls, secret handling and auditability based on actual deployment requirements.

### Phase 13 — Production release

Promote validated artifacts through dev → staging → production with explicit release controls and post-deployment verification.

## Engineering gate

A phase cannot be marked complete because code exists. It is complete when implementation, tests, CI, documentation and deployment evidence satisfy that phase's acceptance criteria.
