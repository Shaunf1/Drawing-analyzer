"""The CLI runs the drawing -> extract -> report pipeline end to end."""

import csv
import io
import json
from pathlib import Path

import ezdxf
import pymupdf
import pytest

from drawing_analyzer.cli import main


def _write_dxf(path: Path) -> None:
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    text = msp.add_text("RL 12.500", dxfattribs={"layer": "LEVELS"})
    text.set_placement((100.0, 200.0))
    slab = msp.add_text("SLAB 300", dxfattribs={"layer": "SLABS"})
    slab.set_placement((50.0, 60.0))
    doc.blocks.new(name="COL-300")
    msp.add_blockref("COL-300", (12.0, 34.0), dxfattribs={"layer": "COLS"})
    doc.saveas(path)


def _write_pdf(path: Path) -> None:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((100, 100), "RL 12.500")
    page.insert_text((100, 130), "SLAB 300")
    doc.save(path)
    doc.close()


def test_main_extracts_from_dxf(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    drawing = tmp_path / "plan.dxf"
    _write_dxf(drawing)

    exit_code = main([str(drawing)])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["reduced_levels"][0]["elevation_mm"] == 12500.0
    assert payload["slab_profiles"][0]["depth_mm"] == 300.0
    assert payload["ga_elements"][0]["kind"] == "column"


def test_main_extracts_from_pdf(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    drawing = tmp_path / "plan.pdf"
    _write_pdf(drawing)

    exit_code = main([str(drawing)])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["reduced_levels"][0]["elevation_mm"] == 12500.0
    assert payload["slab_profiles"][0]["depth_mm"] == 300.0


def test_main_writes_csv_format(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    drawing = tmp_path / "plan.dxf"
    _write_dxf(drawing)

    exit_code = main([str(drawing), "--format", "csv"])

    assert exit_code == 0
    rows = list(csv.DictReader(io.StringIO(capsys.readouterr().out)))
    entity_types = {row["entity_type"] for row in rows}
    assert entity_types == {"reduced_level", "slab_profile", "ga_element"}


def test_main_rejects_unsupported_extension(tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main([str(tmp_path / "plan.txt")])

    assert exit_info.value.code == 2
