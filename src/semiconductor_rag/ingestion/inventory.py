"""Deterministic corpus discovery and inventory."""

from pathlib import Path

DEFAULT_CATEGORIES = (
    "semiconductor_manufacturing",
    "transistor_device_technology",
    "memory",
    "advanced_packaging",
    "power_semiconductors",
    "photonics",
    "ai_advanced_semiconductor",
)


def list_patent_files(
    corpus_root: Path,
    categories: tuple[str, ...] = DEFAULT_CATEGORIES,
) -> list[Path]:
    """Return patent text files in deterministic category/path order."""
    files: list[Path] = []
    for category in categories:
        directory = corpus_root / category
        if directory.exists():
            files.extend(sorted(directory.glob("*.txt")))
    return files


def inventory(corpus_root: Path, categories: tuple[str, ...] = DEFAULT_CATEGORIES) -> dict[str, int]:
    """Return file counts by configured category."""
    files = list_patent_files(corpus_root, categories)
    return {
        category: sum(path.parent.name == category for path in files)
        for category in categories
    }
