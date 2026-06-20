"""The DXF reader normalizes TEXT/MTEXT and INSERT, scaling coordinates to millimetres."""

from pathlib import Path

import ezdxf

from drawing_analyzer.dxf import read_dxf


def _write_dxf(path: Path, *, units: int = ezdxf.units.MM) -> None:
    doc = ezdxf.new(setup=True)
    doc.units = units
    msp = doc.modelspace()
    text = msp.add_text("RL 12.500", dxfattribs={"layer": "LEVELS"})
    text.set_placement((100.0, 200.0))
    mtext = msp.add_mtext("SSL 11.250\\Pnote", dxfattribs={"layer": "LEVELS"})
    mtext.set_location((300.0, 400.0))
    doc.blocks.new(name="COL-300")
    msp.add_blockref("COL-300", (12.0, 34.0), dxfattribs={"layer": "COLS"})
    doc.saveas(path)


def test_reads_text_and_mtext(tmp_path: Path) -> None:
    drawing = tmp_path / "sample.dxf"
    _write_dxf(drawing)

    annotations = read_dxf(drawing).text_annotations

    texts = {annotation.text for annotation in annotations}
    assert "RL 12.500" in texts
    # MTEXT formatting code \P decodes to a newline rather than leaking into the text.
    assert "SSL 11.250\nnote" in texts


def test_reads_block_references(tmp_path: Path) -> None:
    drawing = tmp_path / "sample.dxf"
    _write_dxf(drawing)

    blocks = read_dxf(drawing).block_references

    assert len(blocks) == 1
    assert blocks[0].name == "COL-300"
    assert blocks[0].layer == "COLS"
    assert blocks[0].location == (12.0, 34.0)


def test_millimetre_drawing_keeps_coordinates(tmp_path: Path) -> None:
    drawing = tmp_path / "sample.dxf"
    _write_dxf(drawing, units=ezdxf.units.MM)

    rl = next(a for a in read_dxf(drawing).text_annotations if a.text == "RL 12.500")

    assert rl.location == (100.0, 200.0)


def test_metre_drawing_scales_to_millimetres(tmp_path: Path) -> None:
    drawing = tmp_path / "sample.dxf"
    _write_dxf(drawing, units=ezdxf.units.M)

    rl = next(a for a in read_dxf(drawing).text_annotations if a.text == "RL 12.500")

    assert rl.location == (100_000.0, 200_000.0)


def test_unitless_drawing_keeps_raw_coordinates(tmp_path: Path) -> None:
    drawing = tmp_path / "sample.dxf"
    _write_dxf(drawing, units=0)

    rl = next(a for a in read_dxf(drawing).text_annotations if a.text == "RL 12.500")

    assert rl.location == (100.0, 200.0)
