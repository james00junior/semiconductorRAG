# Semiconductor Patent Intelligence Platform — Architecture

## Objective

Evolve the current 500-document semiconductor patent RAG research baseline into a reproducible, testable and deployable intelligence platform on Databricks.

## Architecture

```text
                         ┌─────────────────────┐
                         │   Patent Sources    │
                         │ files / APIs / feeds│
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │     Ingestion       │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │   Bronze Delta      │
                         │      raw data       │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │ Validate + Normalize│
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │    Silver Delta     │
                         │ normalized patents  │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │      Chunking       │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │     Gold Delta      │
                         │    patent chunks    │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │     Embeddings      │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │  Vector Search      │
                         └──────────┬──────────┘
                                    ↓
                  ┌─────────────────┴──────────────────┐
                  ↓                                    ↓
          lexical retrieval                    vector retrieval
                  └─────────────────┬──────────────────┘
                                    ↓
                              candidate fusion
                                    ↓
                             optional reranker
                                    ↓
                              evidence set
                                    ↓
                         ┌─────────────────────┐
                         │    RAG Generator    │
                         │      LLM            │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │ Evidence-backed API │
                         └─────────────────────┘
```

## Data layers

### Bronze

Immutable or append-oriented raw source representation. Preserve enough information to reproduce parsing and diagnose source changes.

### Silver

Canonical patent records with normalized fields and quality metadata.

### Gold

Retrieval-ready chunks with lineage and embedding/index metadata.

## RAG boundary

The RAG application is deliberately separated into four responsibilities:

1. **Retrieval** — find relevant patent evidence.
2. **Selection** — choose the evidence supplied to the LLM.
3. **Generation** — formulate an answer using only supplied evidence.
4. **Citation** — identify the patent records supporting the answer.

This separation lets retrieval quality be evaluated independently from LLM quality.

## Future intelligence layer

The same patent corpus can later support a broader intelligence system:

```text
                    Patent Intelligence
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
       RAG QA         Similarity        Analytics
          │                │                │
          ↓                ↓                ↓
    evidence search    related patents   trends
    technical QA       clusters           assignees
    summaries          technology maps    whitespace
                                        competition
```

RAG is therefore one capability of the platform rather than the entire product.

## Architecture decision rules

- Prefer Delta/Unity Catalog for governed data persistence.
- Prefer Databricks-native vector search for the production retrieval layer.
- Keep model providers configurable rather than coupling application code to Ollama.
- Keep local Ollama useful for development and experimentation.
- Do not introduce a separate API gateway, Kubernetes cluster, feature store, graph database, or other infrastructure unless an actual requirement justifies it.
- Keep the production architecture observable and reproducible.
