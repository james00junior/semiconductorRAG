"""Canonical document models for patent ingestion."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PatentRecord:
    """Normalized patent record produced from one source text file."""

    document_id: str
    category: str
    cpc_section: str
    source: str
    abstract: str
    description: str
    claims: str
    filename: str
    file_path: str
    word_count: int
    character_count: int

    @property
    def full_text(self) -> str:
        """Return the retrieval source text in deterministic section order."""
        sections = [self.abstract, self.description, self.claims]
        return "\n\n".join(section for section in sections if section).strip()


def record_from_path(path: Path, **values: object) -> PatentRecord:
    """Build a record while keeping filesystem metadata explicit."""
    return PatentRecord(
        filename=path.name,
        file_path=str(path),
        **values,
    )
