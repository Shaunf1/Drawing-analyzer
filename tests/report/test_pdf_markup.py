"""Markup writing draws box and label annotations for each placed value onto the PDF."""

from pathlib import Path

import pymupdf

from drawing_analyzer.model import Provenance, ReducedLevel, SlabProfile
from drawing_analyzer.report import write_markup


def _blank_pdf(path: Path) -> None:
    doc = pymupdf.open()
    doc.new_page()
    doc.save(path)
    doc.close()


def _annotation_contents(path: Path) -> list[str]:
    doc = pymupdf.open(path)
    contents = [annot.info.get("content", "") for annot in doc[0].annots()]
    doc.close()
    return contents


def test_marks_each_placed_value(tmp_path: Path) -> None:
    source = tmp_path / "plan.pdf"
    _blank_pdf(source)
    output = tmp_path / "marked.pdf"
    levels = [
        ReducedLevel(
            elevation_mm=12500.0,
            label="RL 12.500",
            provenance=Provenance(source_file=source, page=1, location=(100.0, 90.0)),
        )
    ]
    slabs = [
        SlabProfile(
            depth_mm=300.0,
            provenance=Provenance(source_file=source, page=1, location=(100.0, 120.0)),
            label="SLAB 300",
        )
    ]

    drawn = write_markup(source, output, levels, slabs)

    assert drawn == 2
    contents = _annotation_contents(output)
    assert any("RL 12500mm" in content for content in contents)
    assert any("slab 300mm" in content for content in contents)


def test_skips_values_without_a_location(tmp_path: Path) -> None:
    source = tmp_path / "plan.pdf"
    _blank_pdf(source)
    output = tmp_path / "marked.pdf"
    levels = [
        ReducedLevel(
            elevation_mm=12500.0,
            label="RL 12.500",
            provenance=Provenance(source_file=source, page=1, location=None),
        )
    ]

    drawn = write_markup(source, output, levels, [])

    assert drawn == 0
