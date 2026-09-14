from pathlib import Path

import pytest

from semiconductor_rag.ingestion.models import PatentRecord
from semiconductor_rag.ingestion.pipeline import validate_records


def make_record(document_id: str, text: str = "patent text") -> PatentRecord:
    return PatentRecord(
        document_id=document_id,
        category="memory",
        cpc_section="G",
        source="TEST",
        abstract=text,
        description="",
        claims="",
        filename=f"patent_{document_id}.txt",
        file_path=f"/tmp/patent_{document_id}.txt",
        word_count=len(text.split()),
        character_count=len(text),
    )


def test_validate_records_accepts_unique_records():
    validate_records([make_record("a"), make_record("b")])


def test_validate_records_rejects_duplicates():
    with pytest.raises(ValueError, match="unique"):
        validate_records([make_record("a"), make_record("a")])


def test_validate_records_rejects_missing_retrieval_text():
    with pytest.raises(ValueError, match="retrieval text"):
        validate_records([make_record("a", text="")])


def test_validate_records_rejects_empty_corpus():
    with pytest.raises(ValueError, match="no patent records"):
        validate_records([])
