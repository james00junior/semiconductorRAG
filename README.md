# Semiconductor Patent Intelligence Platform

A production-oriented RAG and analytics platform for semiconductor patent intelligence.

The project started as a research notebook over a 500-patent semiconductor corpus. It is now being engineered into a reproducible Databricks platform using the same incremental Git → test → CI → PR → merge → pull-main lifecycle used for production ML systems.

## What the platform is intended to do

The long-term system will answer evidence-backed questions about semiconductor technology and support deeper intelligence workflows such as:

- technical patent search and question answering
- patent similarity and related-document discovery
- technology clustering
- semiconductor technology trends
- assignee/company analysis
- emerging technology detection
- competitive intelligence
- patent whitespace analysis
- technical summaries with patent-level evidence

RAG is the first intelligence capability, not the final product.

## Current research baseline

The current notebook implements:

```text
500 patents
   ↓
audit
   ↓
parse / normalize
   ↓
chunk
   ↓
Ollama embeddings
   ↓
semantic retrieval
   ↓
grounded RAG answer
   ↓
evaluation
```

The baseline currently uses local patent text, `nomic-embed-text` for embeddings, and `qwen3:8b` through Ollama for generation. The notebook is retained as a research/reference surface while production logic is moved into tested Python modules.

## Target production architecture

```text
GitHub
  ↓
CI / tests / quality gates
  ↓
Databricks Asset Bundles
  ↓
Bronze Delta
  ↓
Silver Delta
  ↓
Gold patent chunks
  ↓
Embeddings
  ↓
Databricks Vector Search
  ↓
Hybrid retrieval / optional reranking
  ↓
Evidence selection
  ↓
LLM generation
  ↓
Evidence-backed API
```

The platform is designed around clear boundaries between data engineering, retrieval, generation, evaluation and serving.

## Production engineering lifecycle

We build this system incrementally. **No direct feature development on `main`.**

```text
git checkout main
git pull origin main
        ↓
create phase branch
        ↓
implement
        ↓
test locally
        ↓
lint + format
        ↓
commit
        ↓
push
        ↓
Pull Request
        ↓
CI
        ↓
review / fix
        ↓
merge main
        ↓
git checkout main
git pull origin main
        ↓
next phase
```

Each phase must leave the repository in a working state.

See the complete lifecycle in [`docs/ENGINEERING_WORKFLOW.md`](docs/ENGINEERING_WORKFLOW.md).

## Roadmap

| Phase | Capability | Status |
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
| 12 | Controlled production release | Planned |

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for phase-level acceptance criteria and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the target architecture.

## Repository direction

The repository will evolve toward:

```text
.github/
  workflows/

src/
  semiconductor_rag/
    ingestion/
    parsing/
    chunking/
    embeddings/
    retrieval/
    generation/
    evaluation/
    pipelines/

 tests/
   unit/
   integration/
   evaluation/

notebooks/

databricks/
  resources/
  sql/

configs/
eval/
docs/
```

Notebooks remain useful for experimentation and validation. Production pipelines, jobs and services live in version-controlled Python/configuration code.

## Data design

The production data model will use three logical Delta layers:

### Bronze — raw

Source-preserving patent records with ingestion metadata and content hashes.

### Silver — normalized

Canonical patent metadata and normalized text fields.

### Gold — retrieval-ready

Chunked patent content with source lineage, chunking version and embedding/index metadata.

Every answer should be traceable to the underlying patent record and configuration used to retrieve it.

## Reproducibility

The production system will explicitly version:

```text
corpus_version
parser_version
chunking_version
embedding_model
embedding_version
index_version
retrieval_version
prompt_version
llm_model
application_version
```

This makes experiments and production answers reproducible instead of tying behavior to an undocumented notebook state.

## Evaluation

Evaluation will cover both retrieval and generation.

Retrieval:

- Recall@K
- Precision@K
- Hit Rate@K
- MRR
- NDCG

Generation:

- faithfulness
- answer relevance
- context relevance
- citation correctness
- citation completeness

Operations:

- retrieval latency
- generation latency
- end-to-end latency
- token usage
- error rate

A fixed benchmark will be committed to the repository and used for regression testing.

## Environments

The intended deployment model is:

```text
dev → staging → prod
```

Data, jobs, indexes and serving resources are isolated by environment. Secrets are supplied through the deployment environment and are never committed to Git.

## Development philosophy

- Build small increments.
- Preserve working research behavior while replacing components.
- Test before optimizing.
- Prefer deterministic pipelines.
- Avoid re-embedding unchanged content.
- Prefer Databricks-native capabilities where they reduce operational complexity.
- Keep local Ollama useful for development.
- Do not add infrastructure without a concrete requirement.
- Never claim a production capability until it has been deployed and verified.

## Getting started

The production bootstrap is being built phase by phase. The existing notebook remains the baseline research entry point while Phase 0 establishes the engineering contract.

After cloning:

```bash
git clone https://github.com/james00junior/semiconductorRAG.git
cd semiconductorRAG
```

Follow the phase workflow in [`docs/ENGINEERING_WORKFLOW.md`](docs/ENGINEERING_WORKFLOW.md) rather than modifying `main` directly.

## Documentation

- [`Engineering Workflow`](docs/ENGINEERING_WORKFLOW.md) — complete Git, testing, CI/CD and production lifecycle
- [`Architecture`](docs/ARCHITECTURE.md) — target data, retrieval, RAG and intelligence architecture
- [`Roadmap`](docs/ROADMAP.md) — phased implementation plan and completion gates

## Project status

**Current stage: Phase 0 — engineering foundation.**

The immediate objective is to establish the package/test/CI foundation, then move the notebook's data and RAG logic into production-tested components one phase at a time.
