from pathlib import Path

from semiconductor_rag.ingestion.pipeline import ingest_corpus


def test_ingest_corpus_is_deterministic_and_preserves_source_text(tmp_path: Path):
    category = tmp_path / "memory"
    category.mkdir()
    first = category / "patent_b.txt"
    second = category / "patent_a.txt"
    first.write_text("DOCUMENT ID: b\n\nMemory patent B", encoding="utf-8")
    second.write_text("DOCUMENT ID: a\n\nMemory patent A", encoding="utf-8")

    records = ingest_corpus(tmp_path, ("memory",))

    assert [record.document_id for record in records] == ["a", "b"]
    assert records[0].full_text == "DOCUMENT ID: a\n\nMemory patent A"
    assert records[1].full_text == "DOCUMENT ID: b\n\nMemory patent B"
