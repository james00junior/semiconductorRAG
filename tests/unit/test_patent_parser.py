from pathlib import Path

from semiconductor_rag.ingestion.parser import clean_text, parse_patent


def test_clean_text_normalizes_whitespace_and_html():
    assert clean_text("A &amp; B\r\n\tC\n\n\nD") == "A & B\nC\n\nD"


def test_parse_patent_supports_document_id_and_sections(tmp_path: Path):
    path = tmp_path / "patent_abc123.txt"
    content = """DOCUMENT ID: abc123
CATEGORY: memory
CPC SECTION: G
SOURCE: TEST
ABSTRACT
A memory device.
DESCRIPTION
A detailed description.
CLAIMS
1. A memory device.
REFERENCES CITED
Reference text.
"""
    path.write_text(content, encoding="utf-8")

    record = parse_patent(path)

    assert record.document_id == "abc123"
    assert record.category == "memory"
    assert record.cpc_section == "G"
    assert record.source == "TEST"
    assert record.abstract == "A memory device."
    assert record.description == "A detailed description."
    assert record.claims == "1. A memory device."
    assert record.full_text == content.strip()


def test_parse_patent_falls_back_to_filename_and_category(tmp_path: Path):
    category = tmp_path / "photonics"
    category.mkdir()
    path = category / "patent_fallback01.txt"
    content = "A patent body without section headings."
    path.write_text(content, encoding="utf-8")

    record = parse_patent(path)

    assert record.document_id == "fallback01"
    assert record.category == "photonics"
    assert record.source == "BIGPATENT"
    assert record.full_text == content
