"""Slab-depth recognition reads millimetres directly and carries provenance."""

from pathlib import Path

import pytest

from drawing_analyzer.extract import extract_slab_depths
from drawing_analyzer.ingest import TextAnnotation


def _annotation(text: str) -> TextAnnotation:
    return TextAnnotation(
        text=text,
        source_file=Path("plan.dxf"),
        layer="SLABS",
        location=(5.0, 6.0),
    )


@pytest.mark.parametrize(
    ("text", "expected_mm"),
    [
        ("200 THK", 200.0),
        ("200mm THICK", 200.0),
        ("THK 250", 250.0),
        ("SLAB 300", 300.0),
        ("SLAB: 175", 175.0),
    ],
)
def test_recognizes_slab_depth_forms(text: str, expected_mm: float) -> None:
    profiles = extract_slab_depths([_annotation(text)])

    assert len(profiles) == 1
    assert profiles[0].depth_mm == expected_mm
    assert profiles[0].provenance.layer == "SLABS"


def test_keeps_millimetres_without_conversion() -> None:
    # Unlike reduced levels (metres), slab depths are already millimetres.
    profiles = extract_slab_depths([_annotation("300 THK")])

    assert profiles[0].depth_mm == 300.0


def test_ignores_text_without_a_slab_depth() -> None:
    profiles = extract_slab_depths([_annotation("RL 12.500"), _annotation("GRID A")])

    assert profiles == []
