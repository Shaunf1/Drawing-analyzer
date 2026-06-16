"""RL/SSL recognition converts metre annotations to millimetres and carries provenance."""

from pathlib import Path

from drawing_analyzer.extract import extract_reduced_levels
from drawing_analyzer.ingest import TextAnnotation


def _annotation(text: str) -> TextAnnotation:
    return TextAnnotation(
        text=text,
        source_file=Path("plan.dxf"),
        layer="LEVELS",
        location=(10.0, 20.0),
    )


def test_recognizes_rl_and_converts_metres_to_millimetres() -> None:
    levels = extract_reduced_levels([_annotation("RL 12.500")])

    assert len(levels) == 1
    assert levels[0].elevation_mm == 12500.0
    assert not levels[0].is_structural_slab_level
    assert levels[0].provenance.layer == "LEVELS"
    assert levels[0].provenance.location == (10.0, 20.0)


def test_flags_structural_slab_level() -> None:
    levels = extract_reduced_levels([_annotation("SSL 11.250")])

    assert levels[0].is_structural_slab_level
    assert levels[0].elevation_mm == 11250.0


def test_ignores_text_without_a_level() -> None:
    levels = extract_reduced_levels([_annotation("GRID LINE A"), _annotation("COLUMN C1")])

    assert levels == []


def test_matches_separators_and_negative_values() -> None:
    levels = extract_reduced_levels([_annotation("RL: -1.250"), _annotation("ssl=0.000")])

    assert [level.elevation_mm for level in levels] == [-1250.0, 0.0]
