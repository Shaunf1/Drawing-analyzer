"""Read text entities from a DXF file into normalized annotations."""

from __future__ import annotations

from pathlib import Path

from ezdxf.entities.mtext import MText
from ezdxf.entities.text import Text
from ezdxf.filemanagement import readfile

from drawing_analyzer.ingest.document import TextAnnotation


def read_text_annotations(path: Path) -> list[TextAnnotation]:
    """Open a DXF file and return its TEXT and MTEXT entities as normalized annotations.

    MTEXT inline formatting codes are decoded to plain text. Coordinates are the entity insertion
    points in the document's own drawing units; no scaling to millimetres happens here.
    """
    doc = readfile(path)
    annotations: list[TextAnnotation] = []
    for entity in doc.modelspace().query("TEXT MTEXT"):
        if isinstance(entity, MText):
            plain_text = entity.plain_text()
            text = plain_text if isinstance(plain_text, str) else "\n".join(plain_text)
        elif isinstance(entity, Text):
            text = entity.dxf.text
        else:
            continue
        insert = entity.dxf.insert
        annotations.append(
            TextAnnotation(
                text=text,
                source_file=path,
                layer=entity.dxf.layer,
                location=(insert.x, insert.y),
            )
        )
    return annotations
