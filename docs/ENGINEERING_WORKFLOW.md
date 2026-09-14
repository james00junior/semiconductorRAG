# Semiconductor Patent Intelligence Platform — Engineering Workflow

## 1. Purpose

This document defines the engineering lifecycle for turning the current semiconductor patent RAG research notebook into a production-grade, Databricks-based patent intelligence platform.

The project follows the same discipline used for the Netcare ML platform:

```text
Understand baseline
      ↓
Create phase branch from updated main
      ↓
Implement a small, testable increment
      ↓
Run local tests and static checks
      ↓
Commit with a clear phase-level message
      ↓
Push branch
      ↓
Open Pull Request
      ↓
CI validates the branch
      ↓
Review / fix / re-run CI
      ↓
Merge to main
      ↓
Pull main locally
      ↓
Start the next phase from the new main
```

**Rule: no direct feature development on `main`.**

The objective is not to convert the notebook into a large application in one step. Each phase must leave the repository in a working state.

---

## 2. Current baseline

The current research baseline is a single clean notebook that consolidates the earlier patent RAG work:

```text
500 patent corpus
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

The baseline currently uses local filesystem patent text, `nomic-embed-text` for embeddings, and `qwen3:8b` through Ollama for generation. Chunking and retrieval parameters are explicitly configured in the notebook.

The baseline is a **research reference implementation**, not the production runtime.

We preserve its behavior with tests before replacing individual components.

---

## 3. Target production lifecycle

### Phase 0 — Engineering foundation

Goal: establish the repository and CI contract before changing the RAG logic.

Deliverables:

- engineering documentation
- README with architecture and roadmap
- Python package layout
- `pyproject.toml`
- deterministic development dependencies
- Ruff configuration
- Black configuration
- pytest configuration
- initial unit-test structure
- GitHub Actions CI
- `.gitignore`
- environment/configuration strategy

Exit criteria:

- repository installs cleanly
- tests execute
- linting executes
- formatting check executes
- CI runs on pull requests and pushes to `main`
- no secrets or local corpus paths are committed

### Phase 1 — Data platform foundation

Goal: make patent ingestion deterministic and auditable.

Pipeline:

```text
Source files / future source APIs
        ↓
Bronze raw patents
        ↓
validation
        ↓
Silver normalized patents
```

Required metadata:

- `document_id`
- `source`
- `source_uri` or source file
- `category`
- `cpc_section`
- `title` when available
- `abstract`
- `description`
- `claims`
- `content_hash`
- `ingested_at`
- parser/schema version

Data quality checks:

- duplicate document IDs
- duplicate content hashes
- missing required fields
- malformed documents
- unexpected categories
- record counts
- ingestion reproducibility

### Phase 2 — Production chunking

Goal: move chunking out of the notebook into tested package code.

Every chunk must be traceable to its source patent.

Minimum fields:

- `chunk_id`
- `document_id`
- `section`
- `chunk_index`
- `text`
- `token_count`
- `chunking_version`
- `content_hash`
- `created_at`

Chunking parameters are configuration, not hard-coded notebook state.

### Phase 3 — Embedding pipeline

Goal: create a repeatable batch embedding process.

The pipeline must support incremental processing:

```text
patent chunk
    ↓
content hash + embedding configuration
    ↓
already indexed?
   / \
 yes  no
  ↓     ↓
skip   embed
          ↓
       persist
```

Track at minimum:

- embedding model
- embedding dimension
- embedding model version
- chunking version
- corpus version
- content hash
- embedding timestamp

The first production implementation should avoid re-embedding unchanged chunks.

### Phase 4 — Vector search

Goal: replace local-only semantic retrieval with a managed production retrieval layer on Databricks.

Target pattern:

```text
Delta patent chunks
       ↓
embeddings
       ↓
Databricks Vector Search
       ↓
metadata filters + semantic retrieval
```

The vector index is treated as a deployable environment resource, not as an undocumented manual artifact.

### Phase 5 — Retrieval quality

Goal: make retrieval reliable before optimizing generation.

Production retrieval should evolve from pure vector search toward hybrid retrieval where justified:

```text
query
  ├── lexical retrieval
  └── vector retrieval
          ↓
       candidate fusion
          ↓
       optional reranking
          ↓
       final evidence set
```

Do not add a reranker until baseline retrieval metrics show a measurable reason to do so.

### Phase 6 — RAG application

Goal: separate retrieval, prompting, generation, and citation assembly.

Runtime flow:

```text
user question
      ↓
query normalization
      ↓
retrieval
      ↓
evidence selection
      ↓
LLM prompt
      ↓
generation
      ↓
citation / evidence validation
      ↓
answer
```

The LLM must not be treated as the source of patent facts. Retrieved evidence is the source of truth.

### Phase 7 — Evaluation

Goal: establish measurable quality gates.

Retrieval metrics:

- Recall@K
- Precision@K
- Hit Rate@K
- MRR
- NDCG

Generation metrics:

- faithfulness
- answer relevance
- context relevance
- citation correctness
- citation completeness

Operational metrics:

- retrieval latency
- generation latency
- end-to-end latency
- token usage
- failure rate

A fixed benchmark belongs in source control. Evaluation must run against known questions and expected evidence rather than relying on subjective notebook inspection.

### Phase 8 — MLflow experiment tracking

Every meaningful retrieval/generation experiment should record:

- corpus version
- chunking version
- chunk size
- overlap
- embedding model
- embedding version
- retrieval strategy
- candidate K
- final K
- reranker
- LLM
- temperature
- retrieval metrics
- generation metrics
- latency

The objective is reproducibility: another engineer must be able to identify why one RAG configuration performed differently from another.

### Phase 9 — Databricks Jobs / orchestration

Target DAG:

```text
                 ┌──────────────┐
                 │    ingest    │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   validate   │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │    chunk     │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │    embed     │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │ update index │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   evaluate   │
                 └──────────────┘
```

Jobs should be defined as code using Databricks Asset Bundles.

### Phase 10 — Serving

Goal: expose the platform through a stable production interface.

The first serving contract should be deliberately small:

```text
POST /research

request:
  question
  optional filters
  optional top_k

response:
  answer
  evidence
  patent identifiers
  retrieval metadata
  evaluation / trace identifiers where appropriate
```

Serving is introduced only after retrieval and generation are independently testable.

### Phase 11 — Observability and security

Add only the controls required by the deployed architecture.

Minimum observability:

- request ID
- latency
- retrieval count
- model configuration
- errors
- job failures
- index freshness
- evaluation drift

Security controls should cover:

- secrets
- service principals / workload identity
- Unity Catalog permissions
- environment separation
- least privilege
- auditability

Do not introduce infrastructure that does not serve an actual production requirement.

### Phase 12 — Controlled production release

Production releases follow an explicit promotion process:

```text
developer branch
      ↓
PR
      ↓
CI
      ↓
merge main
      ↓
Deploy dev
      ↓
validate dev
      ↓
promote staging
      ↓
validate staging
      ↓
explicit production release
      ↓
post-deployment verification
```

Production promotion must be explicit. Do not invent canary traffic, rollback behavior, or infrastructure that has not actually been implemented and verified.

---

## 4. Git operating procedure

Before starting any phase:

```bash
git checkout main
git pull origin main
git checkout -b phase-X-short-name
```

During development:

```bash
pytest
ruff check .
black --check .
```

Then:

```bash
git status
git diff
git add .
git commit -m "Phase X: <clear change>"
git push -u origin phase-X-short-name
```

Open a PR against `main`.

After CI passes and the PR is reviewed/merged:

```bash
git checkout main
git pull origin main
git branch -d phase-X-short-name
```

Then start the next phase from the newly updated `main`.

### Commit rule

A commit should represent a coherent engineering increment. Avoid mixing unrelated refactors, infrastructure changes, model changes, and documentation into one opaque commit.

### PR rule

Every PR should state:

1. What changed.
2. Why it changed.
3. Tests/checks run.
4. What was deliberately not changed.
5. Any new infrastructure or configuration required.
6. The acceptance criteria for the phase.

---

## 5. Testing strategy

### Unit tests

Fast tests for:

- parser behavior
- text normalization
- section extraction
- chunking
- hashing
- configuration validation
- retrieval result formatting
- prompt construction
- citation assembly

### Integration tests

Validate boundaries between:

- ingestion and Delta
- embedding pipeline and vector index
- retrieval and generation
- Databricks Jobs and package entry points
- API and RAG service

### Evaluation tests

Evaluation tests answer a different question from unit tests: **does the system produce useful evidence and answers?**

A benchmark should include representative semiconductor questions such as:

- technology identification
- process/manufacturing methods
- memory architectures
- transistor/device structures
- advanced packaging
- power semiconductor technologies
- photonics
- AI accelerator semiconductor technologies

### Regression rule

A change that improves one benchmark category but materially damages another must be visible in CI/evaluation results before merging.

---

## 6. Environment strategy

Use three logical environments:

| Environment | Purpose |
|---|---|
| `dev` | active engineering and integration testing |
| `staging` | release candidate validation |
| `prod` | controlled production workload |

Keep data, vector indexes, jobs, and serving resources isolated by environment.

Configuration should select environment-specific resource names. Secrets must never be committed to Git.

---

## 7. Data and model versioning

The platform must be able to answer:

> Which corpus, parser, chunker, embedding model, index, and LLM configuration produced this answer?

Therefore the following versions should be explicit:

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

This is especially important for patent intelligence because the corpus changes over time.

---

## 8. Production data flow

```text
Patent sources
     ↓
Ingestion
     ↓
Bronze Delta
     ↓
Validation / normalization
     ↓
Silver Delta
     ↓
Chunking
     ↓
Gold patent chunks
     ↓
Embedding
     ↓
Vector Search
     ↓
Hybrid retrieval / reranking
     ↓
RAG generation
     ↓
Evidence-backed answer
     ↓
API / application
```

The same source data should also support non-RAG analytics later, including:

- patent similarity
- technology clustering
- assignee analysis
- temporal technology evolution
- emerging technology detection
- whitespace analysis
- competitive intelligence
- citation/network analysis

---

## 9. Definition of done

A phase is complete only when:

- implementation is committed to its phase branch
- unit/integration tests relevant to the phase pass
- lint/format checks pass
- CI passes
- documentation reflects the actual implementation
- the PR is reviewed
- the PR is merged to `main`
- `main` is pulled locally
- the next phase can start from a known-good state

A diagram or design document is not evidence that an infrastructure component exists. Production claims must be backed by an implemented and validated resource.

---

## 10. Guiding engineering principles

1. **Build incrementally.**
2. **Test before replacing working research logic.**
3. **Keep notebooks for exploration, not production orchestration.**
4. **Make data lineage explicit.**
5. **Make model and retrieval configuration reproducible.**
6. **Use Databricks-native services where they reduce operational burden.**
7. **Prefer the simplest architecture that satisfies the requirement.**
8. **Do not claim a production capability until it has been deployed and verified.**
9. **Every production change moves through Git, CI, review, and controlled deployment.**
10. **Optimize for evidence-backed answers, not merely fluent answers.**
