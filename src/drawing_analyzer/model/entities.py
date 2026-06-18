"""Domain entities extracted from drawings: reduced levels, slab profiles, GA elements.

All lengths are millimetres. Every entity carries ``Provenance`` for traceability.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from drawing_analyzer.model.geometry import Point
from drawing_analyzer.model.provenance import Provenance


@dataclass(frozen=True, slots=True)
class ReducedLevel:
    """A Reduced Level (RL) read off a drawing, such as a Structural Slab Level (SSL).

    ``elevation_mm`` is millimetres relative to the project datum. ``label`` is the annotation
    text as drawn (e.g. "SSL" or "RL 12.500").
    """

    elevation_mm: float
    label: str
    provenance: Provenance
    is_structural_slab_level: bool = False


@dataclass(frozen=True, slots=True)
class SlabProfile:
    """A structural slab profile extracted from a drawing.

    ``depth_mm`` is the slab thickness in millimetres. ``outline`` is the slab boundary in drawing
    coordinates (millimetres); empty when no boundary was recovered.
    """

    depth_mm: float
    provenance: Provenance
    label: str | None = None
    outline: tuple[Point, ...] = ()


class GAElementKind(StrEnum):
    """Category of a general-arrangement (GA) structural element."""

    COLUMN = "column"
    BEAM = "beam"
    WALL = "wall"
    SLAB = "slab"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class GAElement:
    """A recognized structural member on a general-arrangement (GA) drawing.

    ``outline`` is the element boundary in drawing coordinates (millimetres); empty when no
    boundary was recovered.
    """

    kind: GAElementKind
    provenance: Provenance
    label: str | None = None
    outline: tuple[Point, ...] = ()
