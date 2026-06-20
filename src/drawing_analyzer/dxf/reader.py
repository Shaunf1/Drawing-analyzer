"""Read text and block references from a DXF file into a normalized document."""

from __future__ import annotations

from pathlib import Path

from ezdxf.entities.insert import Insert
from ezdxf.entities.mtext import MText
from ezdxf.entities.text import Text
from ezdxf.filemanagement import readfile

from drawing_analyzer.ingest.document import BlockReference, Document, TextAnnotation


def read_dxf(path: Path) -> Document:
    """Open a DXF file once and return its TEXT/MTEXT and INSERT entities as a normalized document.

    MTEXT inline formatting codes are decoded to plain text. Coordinates are entity insertion points
    in the document's own drawing units; no scaling to millimetres happens here.
    """
    doc = readfile(path)
    text_annotations: list[TextAnnotation] = []
    block_references: list[BlockReference] = []
    for entity in doc.modelspace().query("TEXT MTEXT INSERT"):
        if isinstance(entity, MText):
            plain_text = entity.plain_text()
            text = plain_text if isinstance(plain_text, str) else "\n".join(plain_text)
            insert = entity.dxf.insert
            text_annotations.append(
                TextAnnotation(
                    text=text,
                    source_file=path,
                    layer=entity.dxf.layer,
                    location=(insert.x, insert.y),
                )
            )
        elif isinstance(entity, Text):
            insert = entity.dxf.insert
            text_annotations.append(
                TextAnnotation(
                    text=entity.dxf.text,
                    source_file=path,
                    layer=entity.dxf.layer,
                    location=(insert.x, insert.y),
                )
            )
        elif isinstance(entity, Insert):
            insert = entity.dxf.insert
            block_references.append(
                BlockReference(
                    name=entity.dxf.name,
                    source_file=path,
                    layer=entity.dxf.layer,
                    location=(insert.x, insert.y),
                )
            )
    return Document(
        text_annotations=tuple(text_annotations),
        block_references=tuple(block_references),
    )
