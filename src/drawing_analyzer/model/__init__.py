"""Domain model: dataclasses for extracted entities (slab profiles, GA elements, reduced levels).

Lengths are stored in millimetres; every extracted value carries provenance (source file,
page/layer, coordinates).
"""

from drawing_analyzer.model.entities import (
    GAElement,
    GAElementKind,
    ReducedLevel,
    SlabProfile,
)
from drawing_analyzer.model.geometry import Point
from drawing_analyzer.model.provenance import Provenance

__all__ = [
    "GAElement",
    "GAElementKind",
    "Point",
    "Provenance",
    "ReducedLevel",
    "SlabProfile",
]
