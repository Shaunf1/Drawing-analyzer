"""GA-element recognition classifies block references by name and keeps provenance."""

from pathlib import Path

from drawing_analyzer.extract import extract_ga_elements
from drawing_analyzer.extract.ga_element import classify_block_name
from drawing_analyzer.ingest import BlockReference
from drawing_analyzer.model import GAElementKind


def _block(name: str) -> BlockReference:
    return BlockReference(
        name=name, source_file=Path("plan.dxf"), layer="COLS", location=(1.0, 2.0)
    )


def test_classifies_known_block_names() -> None:
    assert classify_block_name("COL-300") == GAElementKind.COLUMN
    assert classify_block_name("steel beam") == GAElementKind.BEAM
    assert classify_block_name("WALL-EXT") == GAElementKind.WALL
    assert classify_block_name("SLAB-EDGE") == GAElementKind.SLAB


def test_unknown_name_defaults_to_other() -> None:
    assert classify_block_name("TITLEBLOCK") == GAElementKind.OTHER


def test_extracts_element_per_block_with_provenance() -> None:
    elements = extract_ga_elements([_block("COL-300"), _block("GRID-BUBBLE")])

    assert [element.kind for element in elements] == [GAElementKind.COLUMN, GAElementKind.OTHER]
    assert elements[0].label == "COL-300"
    assert elements[0].provenance.layer == "COLS"
    assert elements[0].provenance.location == (1.0, 2.0)


def test_empty_input_yields_no_elements() -> None:
    assert extract_ga_elements([]) == []
