"""The DXF reader normalizes TEXT and MTEXT entities, keeping layer and insertion point."""

from pathlib import Path

import ezdxf

from drawing_analyzer.dxf import read_text_annotations


def _write_dxf(path: Path) -> None:
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    text = msp.add_text("RL 12.500", dxfattribs={"layer": "LEVELS"})
    text.set_placement((100.0, 200.0))
    mtext = msp.add_mtext("SSL 11.250\\Pnote", dxfattribs={"layer": "LEVELS"})
    mtext.set_location((300.0, 400.0))
    doc.saveas(path)


def test_reads_text_and_mtext(tmp_path: Path) -> None:
    drawing = tmp_path / "sample.dxf"
    _write_dxf(drawing)

    annotations = read_text_annotations(drawing)

    by_layer = {annotation.text for annotation in annotations}
    assert "RL 12.500" in by_layer
    # MTEXT formatting code \P decodes to a newline rather than leaking into the text.
    assert "SSL 11.250\nnote" in by_layer
    assert all(annotation.layer == "LEVELS" for annotation in annotations)
    assert all(annotation.location is not None for annotation in annotations)


def test_keeps_insertion_point(tmp_path: Path) -> None:
    drawing = tmp_path / "sample.dxf"
    _write_dxf(drawing)

    text_annotation = next(
        annotation
        for annotation in read_text_annotations(drawing)
        if annotation.text == "RL 12.500"
    )

    assert text_annotation.location == (100.0, 200.0)
    assert text_annotation.source_file == drawing
