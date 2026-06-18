"""Recognize Reduced Levels (RLs) and Structural Slab Levels (SSLs) in text annotations."""

from __future__ import annotations

import re
from collections.abc import Iterable

from drawing_analyzer.extract.provenance import provenance_of
from drawing_analyzer.ingest.document import TextAnnotation
from drawing_analyzer.model import ReducedLevel

_MM_PER_METRE = 1000.0

# Drawings annotate reduced levels in metres, e.g. "RL 12.500" or "SSL 11.250".
_RL_PATTERN = re.compile(
    r"\b(?P<kind>RL|SSL)\b[\s:=]*(?P<value>[+-]?\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


def extract_reduced_levels(annotations: Iterable[TextAnnotation]) -> list[ReducedLevel]:
    """Find RL/SSL annotations and convert their metre values to millimetre elevations.

    Text is assumed to express levels in metres, the drawing convention, so values are multiplied
    by 1000 to store millimetres. Each match keeps the source layer and location as provenance;
    an "SSL" match sets ``is_structural_slab_level``.
    """
    levels: list[ReducedLevel] = []
    for annotation in annotations:
        match = _RL_PATTERN.search(annotation.text)
        if match is None:
            continue
        levels.append(
            ReducedLevel(
                elevation_mm=float(match.group("value")) * _MM_PER_METRE,
                label=match.group(0).strip(),
                provenance=provenance_of(annotation),
                is_structural_slab_level=match.group("kind").upper() == "SSL",
            )
        )
    return levels
