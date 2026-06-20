"""Normalized document primitives produced by ingestion and consumed by extractors."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TextAnnotation:
    """A piece of text read from a source drawing, with where it sits and where it came from.

    ``location`` is the insertion point in the source's native units (DXF drawing units or PDF
    page points), not millimetres. ``layer`` is the DXF layer name, or None for sources without
    layers; ``page`` is the 1-based PDF page, or None for DXF.
    """

    text: str
    source_file: Path
    layer: str | None = None
    location: tuple[float, float] | None = None
    page: int | None = None


@dataclass(frozen=True, slots=True)
class BlockReference:
    """A block (symbol) instance placed in a drawing, e.g. a column or fixture.

    ``name`` is the block definition name. ``location`` is the insertion point in the source's
    native units (DXF drawing units), not millimetres. ``layer`` is the DXF layer, or None.
    """

    name: str
    source_file: Path
    layer: str | None = None
    location: tuple[float, float] | None = None
    page: int | None = None


@dataclass(frozen=True, slots=True)
class Document:
    """The normalized contents of a drawing: its text annotations and block references."""

    text_annotations: tuple[TextAnnotation, ...] = ()
    block_references: tuple[BlockReference, ...] = ()
