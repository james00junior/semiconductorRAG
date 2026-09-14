"""Document-level ingestion pipeline."""

from pathlib import Path

from .inventory import DEFAULT_CATEGORIES, list_patent_files
from .models import PatentRecord
from .parser import parse_patent


def ingest_corpus(
    corpus_root: Path,
    categories: tuple[str, ...] = DEFAULT_CATEGORIES,
) -> list[PatentRecord]:
    """Read and normalize every patent in deterministic order."""
    return [parse_patent(path) for path in list_patent_files(corpus_root, categories)]


def validate_records(records: list[PatentRecord]) -> None:
    """Enforce invariants required before persistence to a production data layer."""
    if not records:
        raise ValueError("Corpus contains no patent records")

    document_ids = [record.document_id for record in records]
    if any(not value for value in document_ids):
        raise ValueError("Every patent must have a document_id")
    if len(document_ids) != len(set(document_ids)):
        raise ValueError("document_id values must be unique")
    if any(not record.full_text for record in records):
        raise ValueError("Every patent must contain retrieval text")
