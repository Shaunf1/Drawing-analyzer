"""Provenance: where an extracted value came from, for traceability back to the source drawing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Provenance:
    """Source location of an extracted value.

    ``page`` is the 1-based PDF page the value was read from (None for DXF sources); ``layer`` is
    the DXF layer name (None for PDF). ``location`` is the point on the source sheet in the
    source's native units (PDF page points, or DXF drawing units), not millimetres.
    """

    source_file: Path
    page: int | None = None
    layer: str | None = None
    location: tuple[float, float] | None = None
