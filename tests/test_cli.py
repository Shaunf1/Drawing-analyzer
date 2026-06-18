"""The CLI runs the DXF -> extract -> JSON pipeline end to end."""

import json
from pathlib import Path

import ezdxf
import pytest

from drawing_analyzer.cli import main


def _write_dxf(path: Path) -> None:
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    text = msp.add_text("RL 12.500", dxfattribs={"layer": "LEVELS"})
    text.set_placement((100.0, 200.0))
    slab = msp.add_text("SLAB 300", dxfattribs={"layer": "SLABS"})
    slab.set_placement((50.0, 60.0))
    doc.saveas(path)


def test_main_prints_extraction_as_json(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    drawing = tmp_path / "plan.dxf"
    _write_dxf(drawing)

    exit_code = main([str(drawing)])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["reduced_levels"][0]["elevation_mm"] == 12500.0
    assert payload["slab_profiles"][0]["depth_mm"] == 300.0


def test_main_rejects_non_dxf(tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main([str(tmp_path / "plan.pdf")])

    assert exit_info.value.code == 2
