"""Recognize general-arrangement (GA) elements from drawing block references."""

from __future__ import annotations

from collections.abc import Iterable

from drawing_analyzer.extract.provenance import provenance_of
from drawing_analyzer.ingest.document import BlockReference
from drawing_analyzer.model import GAElement, GAElementKind

# Block names rarely follow a strict standard, so classification is a keyword heuristic over the
# block name. Order matters only when a name contains more than one keyword; first match wins.
_KIND_KEYWORDS: tuple[tuple[str, GAElementKind], ...] = (
    ("COL", GAElementKind.COLUMN),
    ("BEAM", GAElementKind.BEAM),
    ("WALL", GAElementKind.WALL),
    ("SLAB", GAElementKind.SLAB),
)


def classify_block_name(name: str) -> GAElementKind:
    """Map a block name to a GA element kind by keyword, defaulting to ``OTHER``."""
    upper = name.upper()
    for keyword, kind in _KIND_KEYWORDS:
        if keyword in upper:
            return kind
    return GAElementKind.OTHER


def extract_ga_elements(block_references: Iterable[BlockReference]) -> list[GAElement]:
    """Turn block references into GA elements, classifying each by its block name.

    Every block reference becomes one GA element; unrecognized names get kind ``OTHER`` rather than
    being dropped, so nothing is silently lost. The block name is kept as the element label and the
    block's layer and location as provenance.
    """
    return [
        GAElement(
            kind=classify_block_name(reference.name),
            provenance=provenance_of(reference),
            label=reference.name,
        )
        for reference in block_references
    ]
