"""The CSV report renders one row per value with a shared provenance schema."""

import csv
import io
from pathlib import Path

from drawing_analyzer.model import GAElement, GAElementKind, Provenance, ReducedLevel, SlabProfile
from drawing_analyzer.report import extraction_to_csv


def _provenance(*, location: tuple[float, float] | None = (10.0, 20.0)) -> Provenance:
    return Provenance(source_file=Path("plan.dxf"), layer="LEVELS", location=location)


def _rows(csv_text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(csv_text)))


def test_renders_a_row_per_entity_type() -> None:
    levels = [ReducedLevel(elevation_mm=12500.0, label="RL 12.500", provenance=_provenance())]
    slabs = [SlabProfile(depth_mm=300.0, provenance=_provenance(), label="300 THK")]
    ga = [GAElement(kind=GAElementKind.COLUMN, provenance=_provenance(), label="COL-300")]

    rows = _rows(extraction_to_csv(levels, slabs, ga))

    assert [row["entity_type"] for row in rows] == ["reduced_level", "slab_profile", "ga_element"]
    assert rows[0]["kind"] == "RL"
    assert rows[0]["value_mm"] == "12500.0"
    assert rows[0]["source_file"] == "plan.dxf"
    assert rows[0]["location_x_mm"] == "10.0"
    assert rows[1]["value_mm"] == "300.0"
    assert rows[2]["kind"] == "column"
    # GA elements carry no scalar value.
    assert rows[2]["value_mm"] == ""


def test_structural_slab_level_is_flagged_in_kind() -> None:
    levels = [
        ReducedLevel(
            elevation_mm=11250.0,
            label="SSL 11.250",
            provenance=_provenance(),
            is_structural_slab_level=True,
        )
    ]

    rows = _rows(extraction_to_csv(levels, [], []))

    assert rows[0]["kind"] == "SSL"


def test_missing_location_renders_blank_cells() -> None:
    levels = [
        ReducedLevel(
            elevation_mm=12500.0,
            label="RL 12.500",
            provenance=_provenance(location=None),
        )
    ]

    rows = _rows(extraction_to_csv(levels, [], []))

    assert rows[0]["location_x_mm"] == ""
    assert rows[0]["location_y_mm"] == ""


def test_empty_extraction_is_header_only() -> None:
    text = extraction_to_csv([], [], [])

    header = "entity_type,kind,label,value_mm,source_file,page,layer,location_x_mm,location_y_mm"
    assert text.splitlines() == [header]
