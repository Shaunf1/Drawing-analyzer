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
    doc.saveas(path)


def test_main_prints_reduced_levels_as_json(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    drawing = tmp_path / "plan.dxf"
    _write_dxf(drawing)

    exit_code = main([str(drawing)])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload[0]["elevation_mm"] == 12500.0


def test_main_rejects_non_dxf(tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main([str(tmp_path / "plan.pdf")])

    assert exit_info.value.code == 2
