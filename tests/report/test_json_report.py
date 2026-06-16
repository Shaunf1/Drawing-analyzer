"""The JSON report renders reduced levels and their provenance as portable JSON."""

import json
from pathlib import Path

from drawing_analyzer.model import Provenance, ReducedLevel
from drawing_analyzer.report import reduced_levels_to_json


def test_renders_level_with_string_source_path() -> None:
    level = ReducedLevel(
        elevation_mm=12500.0,
        label="RL 12.500",
        provenance=Provenance(source_file=Path("plan.dxf"), layer="LEVELS", location=(10.0, 20.0)),
        is_structural_slab_level=False,
    )

    payload = json.loads(reduced_levels_to_json([level]))

    assert payload[0]["elevation_mm"] == 12500.0
    assert payload[0]["label"] == "RL 12.500"
    assert payload[0]["provenance"]["source_file"] == "plan.dxf"
    assert payload[0]["provenance"]["layer"] == "LEVELS"


def test_empty_input_renders_empty_array() -> None:
    assert json.loads(reduced_levels_to_json([])) == []
