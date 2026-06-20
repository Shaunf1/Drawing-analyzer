"""Read text and block references from a DXF file into a normalized document."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ezdxf.entities.insert import Insert
from ezdxf.entities.mtext import MText
from ezdxf.entities.text import Text
from ezdxf.filemanagement import readfile

from drawing_analyzer.dxf.units import millimetres_per_unit
from drawing_analyzer.ingest.document import BlockReference, Document, TextAnnotation


def read_dxf(path: Path) -> Document:
    """Open a DXF file once and return its TEXT/MTEXT and INSERT entities as a normalized document.

    MTEXT inline formatting codes are decoded to plain text. Insertion points are converted to
    millimetres using the drawing's $INSUNITS header; when the drawing is unitless (or uses an
    unsupported unit) coordinates are kept as raw drawing units.
    """
    doc = readfile(path)
    mm_per_unit = millimetres_per_unit(doc.units)

    def to_mm(insert: Any) -> tuple[float, float]:
        if mm_per_unit is None:
            return (insert.x, insert.y)
        return (insert.x * mm_per_unit, insert.y * mm_per_unit)

    text_annotations: list[TextAnnotation] = []
    block_references: list[BlockReference] = []
    for entity in doc.modelspace().query("TEXT MTEXT INSERT"):
        if isinstance(entity, MText):
            plain_text = entity.plain_text()
            text = plain_text if isinstance(plain_text, str) else "\n".join(plain_text)
            text_annotations.append(
                TextAnnotation(
                    text=text,
                    source_file=path,
                    layer=entity.dxf.layer,
                    location=to_mm(entity.dxf.insert),
                )
            )
        elif isinstance(entity, Text):
            text_annotations.append(
                TextAnnotation(
                    text=entity.dxf.text,
                    source_file=path,
                    layer=entity.dxf.layer,
                    location=to_mm(entity.dxf.insert),
                )
            )
        elif isinstance(entity, Insert):
            block_references.append(
                BlockReference(
                    name=entity.dxf.name,
                    source_file=path,
                    layer=entity.dxf.layer,
                    location=to_mm(entity.dxf.insert),
                )
            )
    return Document(
        text_annotations=tuple(text_annotations),
        block_references=tuple(block_references),
    )
