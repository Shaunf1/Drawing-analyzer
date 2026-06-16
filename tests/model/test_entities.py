"""Domain entities carry millimetre values and provenance, and are immutable."""

from pathlib import Path

import pytest

from drawing_analyzer.model import (
    GAElement,
    GAElementKind,
    Point,
    Provenance,
    ReducedLevel,
    SlabProfile,
)


def _provenance() -> Provenance:
    return Provenance(source_file=Path("drawing.pdf"), page=3, location=(120.0, 80.0))


def test_reduced_level_holds_elevation_and_provenance() -> None:
    ssl = ReducedLevel(
        elevation_mm=12500.0,
        label="SSL",
        provenance=_provenance(),
        is_structural_slab_level=True,
    )
    assert ssl.elevation_mm == 12500.0
    assert ssl.is_structural_slab_level
    assert ssl.provenance.page == 3


def test_slab_profile_outline_defaults_empty() -> None:
    slab = SlabProfile(depth_mm=300.0, provenance=_provenance())
    assert slab.outline == ()
    assert slab.label is None


def test_ga_element_kind_is_string_valued() -> None:
    element = GAElement(
        kind=GAElementKind.COLUMN,
        provenance=_provenance(),
        outline=(Point(0.0, 0.0), Point(0.0, 500.0)),
    )
    assert element.kind == "column"
    assert len(element.outline) == 2


def test_entities_are_frozen() -> None:
    slab = SlabProfile(depth_mm=300.0, provenance=_provenance())
    with pytest.raises(AttributeError):
        slab.depth_mm = 350.0  # type: ignore[misc]
