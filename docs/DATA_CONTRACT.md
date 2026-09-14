# Patent Data Contract

Phase 2 establishes the canonical document contract used before Delta persistence.

## Source

The current research corpus is a directory of UTF-8 `.txt` patent documents grouped by seven semiconductor categories. The notebook baseline treats these text files as authoritative rather than relying on stale metadata.

## Canonical document fields

| Field | Type | Rule |
|---|---|---|
| `document_id` | string | Required and unique; header first, filename fallback |
| `category` | string | Header first, parent directory fallback |
| `cpc_section` | string | Optional normalized header value |
| `source` | string | Header first, `BIGPATENT` fallback |
| `abstract` | string | Parsed section when present |
| `description` | string | Parsed description section when present |
| `claims` | string | Parsed claims section when present |
| `full_text` | string | Complete cleaned source document; authoritative retrieval text |
| `filename` | string | Original source filename |
| `file_path` | string | Source path for local lineage; not a production storage URI |
| `word_count` | integer | Count over cleaned source text |
| `character_count` | integer | Length of cleaned source text |

## Invariants

1. The corpus must contain at least one document.
2. Every document must have a non-empty `document_id`.
3. `document_id` must be unique within an ingestion batch.
4. Every document must have non-empty `full_text` before retrieval persistence.
5. Source text is cleaned deterministically; no LLM is involved in ingestion.

## Production mapping

The contract is deliberately independent of storage technology. Phase 2 validates it locally; a later Databricks phase will map it into Bronze/Silver Delta tables with explicit source lineage and ingestion timestamps.

## Compatibility note

The original research corpus contains documents where structured section extraction is incomplete. Therefore `full_text` is preserved independently of `abstract`, `description`, and `claims`. This prevents production ingestion from silently dropping usable patent text while section parsing evolves.
