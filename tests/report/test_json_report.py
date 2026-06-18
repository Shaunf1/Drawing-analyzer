"""The JSON report renders reduced levels and their provenance as portable JSON."""

import json
from pathlib import Path

from drawing_analyzer.model import Provenance, ReducedLevel, SlabProfile
from drawing_analyzer.report import (
    extraction_to_json,
    reduced_levels_to_json,
    slab_profiles_to_json,
)


def _provenance() -> Provenance:
    return Provenance(source_file=Path("plan.dxf"), layer="LEVELS", location=(10.0, 20.0))


def _level() -> ReducedLevel:
    return ReducedLevel(elevation_mm=12500.0, label="RL 12.500", provenance=_provenance())


def _slab() -> SlabProfile:
    return SlabProfile(depth_mm=300.0, provenance=_provenance(), label="300 THK")


def test_renders_level_with_string_source_path() -> None:
    payload = json.loads(reduced_levels_to_json([_level()]))

    assert payload[0]["elevation_mm"] == 12500.0
    assert payload[0]["label"] == "RL 12.500"
    assert payload[0]["provenance"]["source_file"] == "plan.dxf"
    assert payload[0]["provenance"]["layer"] == "LEVELS"


def test_renders_slab_profile() -> None:
    payload = json.loads(slab_profiles_to_json([_slab()]))

    assert payload[0]["depth_mm"] == 300.0
    assert payload[0]["provenance"]["source_file"] == "plan.dxf"


def test_extraction_groups_levels_and_slabs() -> None:
    payload = json.loads(extraction_to_json([_level()], [_slab()]))

    assert payload["reduced_levels"][0]["elevation_mm"] == 12500.0
    assert payload["slab_profiles"][0]["depth_mm"] == 300.0


def test_empty_input_renders_empty_array() -> None:
    assert json.loads(reduced_levels_to_json([])) == []
