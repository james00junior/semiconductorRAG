"""Parsing and normalization of the patent text corpus."""

import html
import re
from pathlib import Path

from .models import PatentRecord, record_from_path


def clean_text(text: str | None) -> str:
    """Normalize HTML entities, line endings and whitespace without changing words."""
    value = "" if text is None else str(text)
    value = html.unescape(value)
    value = value.replace("\x00", " ")
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n[ \t]+", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def header_value(text: str, field: str) -> str:
    """Extract a single-line ``FIELD: value`` header."""
    match = re.search(rf"(?im)^\s*{re.escape(field)}:\s*(.+?)\s*$", text)
    return match.group(1).strip() if match else ""


def section_value(text: str, starts: tuple[str, ...], ends: tuple[str, ...]) -> str:
    """Extract text between the first matching start and next matching end heading."""
    start = None
    for pattern in starts:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            start = match.end()
            break
    if start is None:
        return ""

    remaining = text[start:]
    positions = []
    for pattern in ends:
        match = re.search(pattern, remaining, re.IGNORECASE | re.MULTILINE)
        if match:
            positions.append(match.start())
    if positions:
        remaining = remaining[: min(positions)]
    return clean_text(remaining)


def parse_patent(path: Path) -> PatentRecord:
    """Parse one corpus text file into the canonical patent record."""
    raw = clean_text(path.read_text(encoding="utf-8", errors="replace"))

    document_id = (
        header_value(raw, "DOCUMENT ID")
        or header_value(raw, "DOCUMENT_ID")
        or path.stem.removeprefix("patent_")
    )
    category = header_value(raw, "CATEGORY") or path.parent.name
    cpc_section = header_value(raw, "CPC SECTION")
    source = header_value(raw, "SOURCE") or "BIGPATENT"

    abstract = section_value(
        raw,
        (r"^\s*ABSTRACT\s*=*\s*$",),
        (
            r"^\s*DETAILED DESCRIPTION\s*=*\s*$",
            r"^\s*DESCRIPTION\s*=*\s*$",
            r"^\s*CLAIMS\s*=*\s*$",
        ),
    )
    description = section_value(
        raw,
        (
            r"^\s*DETAILED DESCRIPTION\s*=*\s*$",
            r"^\s*DESCRIPTION\s*=*\s*$",
        ),
        (r"^\s*CLAIMS\s*=*\s*$", r"^\s*REFERENCES CITED\s*$"),
    )
    claims = section_value(
        raw,
        (r"^\s*CLAIMS\s*=*\s*$",),
        (r"^\s*REFERENCES CITED\s*$", r"^\s*REFERENCE\s*$"),
    )

    return record_from_path(
        path,
        document_id=document_id,
        category=category,
        cpc_section=cpc_section,
        source=source,
        abstract=abstract,
        description=description,
        claims=claims,
        word_count=len(re.findall(r"\b\w+\b", raw)),
        character_count=len(raw),
    )
