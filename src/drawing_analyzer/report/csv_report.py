"""Serialize extracted domain entities to a flat CSV, one row per value."""

from __future__ import annotations

import csv
import io
from collections.abc import Iterable

from drawing_analyzer.model import GAElement, Provenance, ReducedLevel, SlabProfile

_FIELDNAMES = (
    "entity_type",
    "kind",
    "label",
    "value_mm",
    "source_file",
    "page",
    "layer",
    "location_x_mm",
    "location_y_mm",
)


def extraction_to_csv(
    reduced_levels: Iterable[ReducedLevel],
    slab_profiles: Iterable[SlabProfile],
    ga_elements: Iterable[GAElement],
) -> str:
    """Render a full extraction as a flat CSV, one row per value, sharing a provenance schema.

    ``value_mm`` holds the elevation for reduced levels and the depth for slab profiles, and is
    blank for GA elements (which carry no single scalar). A blank cell means the field does not
    apply or was not recorded.
    """
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=_FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    for level in reduced_levels:
        writer.writerow(
            _row(
                "reduced_level",
                kind="SSL" if level.is_structural_slab_level else "RL",
                label=level.label,
                value_mm=level.elevation_mm,
                provenance=level.provenance,
            )
        )
    for profile in slab_profiles:
        writer.writerow(
            _row(
                "slab_profile",
                kind="",
                label=profile.label,
                value_mm=profile.depth_mm,
                provenance=profile.provenance,
            )
        )
    for element in ga_elements:
        writer.writerow(
            _row(
                "ga_element",
                kind=element.kind.value,
                label=element.label,
                value_mm=None,
                provenance=element.provenance,
            )
        )
    return buffer.getvalue()


def _row(
    entity_type: str,
    *,
    kind: str,
    label: str | None,
    value_mm: float | None,
    provenance: Provenance,
) -> dict[str, object]:
    location = provenance.location
    return {
        "entity_type": entity_type,
        "kind": kind,
        "label": label or "",
        "value_mm": "" if value_mm is None else value_mm,
        "source_file": str(provenance.source_file),
        "page": "" if provenance.page is None else provenance.page,
        "layer": provenance.layer or "",
        "location_x_mm": "" if location is None else location[0],
        "location_y_mm": "" if location is None else location[1],
    }
