"""Serialize extracted domain entities to JSON."""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict

from drawing_analyzer.model import ReducedLevel


def reduced_levels_to_json(levels: Iterable[ReducedLevel], *, indent: int = 2) -> str:
    """Render reduced levels as a JSON array, including provenance.

    The provenance source path is rendered as a string so the result is plain, portable JSON.
    """
    payload = [_reduced_level_to_dict(level) for level in levels]
    return json.dumps(payload, indent=indent)


def _reduced_level_to_dict(level: ReducedLevel) -> dict[str, object]:
    data = asdict(level)
    data["provenance"]["source_file"] = str(level.provenance.source_file)
    return data
