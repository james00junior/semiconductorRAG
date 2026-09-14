from pathlib import Path

from semiconductor_rag.ingestion.inventory import inventory, list_patent_files


def test_list_patent_files_is_deterministic(tmp_path: Path):
    (tmp_path / "memory").mkdir()
    (tmp_path / "memory" / "patent_b.txt").write_text("b", encoding="utf-8")
    (tmp_path / "memory" / "patent_a.txt").write_text("a", encoding="utf-8")

    files = list_patent_files(tmp_path, ("memory",))

    assert [path.name for path in files] == ["patent_a.txt", "patent_b.txt"]


def test_inventory_counts_configured_categories(tmp_path: Path):
    (tmp_path / "memory").mkdir()
    (tmp_path / "memory" / "patent_a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "photonics").mkdir()
    (tmp_path / "photonics" / "patent_b.txt").write_text("b", encoding="utf-8")

    assert inventory(tmp_path, ("memory", "photonics", "power_semiconductors")) == {
        "memory": 1,
        "photonics": 1,
        "power_semiconductors": 0,
    }
