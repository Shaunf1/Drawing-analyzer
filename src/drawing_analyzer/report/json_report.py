"""Serialize extracted domain entities to JSON."""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict
from typing import Any

from drawing_analyzer.model import ReducedLevel, SlabProfile


def reduced_levels_to_json(levels: Iterable[ReducedLevel], *, indent: int = 2) -> str:
    """Render reduced levels as a JSON array, including provenance."""
    return json.dumps([_entity_to_dict(level) for level in levels], indent=indent)


def slab_profiles_to_json(profiles: Iterable[SlabProfile], *, indent: int = 2) -> str:
    """Render slab profiles as a JSON array, including provenance."""
    return json.dumps([_entity_to_dict(profile) for profile in profiles], indent=indent)


def extraction_to_json(
    reduced_levels: Iterable[ReducedLevel],
    slab_profiles: Iterable[SlabProfile],
    *,
    indent: int = 2,
) -> str:
    """Render a full extraction as one JSON object keyed by entity type."""
    payload = {
        "reduced_levels": [_entity_to_dict(level) for level in reduced_levels],
        "slab_profiles": [_entity_to_dict(profile) for profile in slab_profiles],
    }
    return json.dumps(payload, indent=indent)


def _entity_to_dict(entity: Any) -> dict[str, Any]:
    """Convert an extracted dataclass to a JSON-ready dict, stringifying the provenance path."""
    data: dict[str, Any] = asdict(entity)
    data["provenance"]["source_file"] = str(data["provenance"]["source_file"])
    return data
