"""The PDF reader returns one annotation per text line, keeping page and position."""

from pathlib import Path

import pymupdf

from drawing_analyzer.pdf import read_text_annotations


def _write_pdf(path: Path) -> None:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((100, 100), "RL 12.500")
    page.insert_text((100, 130), "SLAB 300")
    doc.save(path)
    doc.close()


def test_reads_lines_with_page_number(tmp_path: Path) -> None:
    drawing = tmp_path / "plan.pdf"
    _write_pdf(drawing)

    annotations = read_text_annotations(drawing)

    texts = {annotation.text for annotation in annotations}
    assert "RL 12.500" in texts
    assert "SLAB 300" in texts
    assert all(annotation.page == 1 for annotation in annotations)
    assert all(annotation.layer is None for annotation in annotations)


def test_keeps_line_position(tmp_path: Path) -> None:
    drawing = tmp_path / "plan.pdf"
    _write_pdf(drawing)

    rl = next(a for a in read_text_annotations(drawing) if a.text == "RL 12.500")

    assert rl.location is not None
    assert rl.location[0] == 100.0
    assert rl.source_file == drawing
