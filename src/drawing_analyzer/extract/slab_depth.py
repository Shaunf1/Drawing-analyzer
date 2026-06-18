"""Recognize slab depths (thicknesses) in text annotations."""

from __future__ import annotations

import re
from collections.abc import Iterable

from drawing_analyzer.extract.provenance import provenance_of
from drawing_analyzer.ingest.document import TextAnnotation
from drawing_analyzer.model import SlabProfile

# Slab thickness is annotated in millimetres, with the value before or after the keyword:
# "200 THK", "200mm THICK", "THK 200", "SLAB 300".
_SLAB_PATTERNS = (
    re.compile(r"(?P<value>\d+(?:\.\d+)?)\s*(?:mm)?\s*(?:THK|THICK)\b", re.IGNORECASE),
    re.compile(
        r"\b(?:SLAB|THK|THICK)\s*[:=]?\s*(?P<value>\d+(?:\.\d+)?)\s*(?:mm)?\b",
        re.IGNORECASE,
    ),
)


def extract_slab_depths(annotations: Iterable[TextAnnotation]) -> list[SlabProfile]:
    """Find slab-thickness annotations and record them as slab profiles.

    The matched value is already millimetres, the slab-depth convention, so it is stored directly
    on ``depth_mm`` with no unit conversion (unlike reduced levels, which are metres). Each match
    keeps the source layer and location as provenance.
    """
    profiles: list[SlabProfile] = []
    for annotation in annotations:
        match = _match_depth(annotation.text)
        if match is None:
            continue
        profiles.append(
            SlabProfile(
                depth_mm=float(match.group("value")),
                provenance=provenance_of(annotation),
                label=match.group(0).strip(),
            )
        )
    return profiles


def _match_depth(text: str) -> re.Match[str] | None:
    for pattern in _SLAB_PATTERNS:
        match = pattern.search(text)
        if match is not None:
            return match
    return None
