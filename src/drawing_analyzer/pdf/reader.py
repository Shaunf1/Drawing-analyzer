"""Read text from a PDF file into a normalized document, one annotation per text line."""

from __future__ import annotations

from pathlib import Path

import pymupdf

from drawing_analyzer.ingest.document import Document, TextAnnotation

_TEXT_BLOCK = 0  # PyMuPDF block type for text (image blocks are type 1).
_MM_PER_POINT = 25.4 / 72  # PDF user-space points are 1/72 inch.


def read_pdf(path: Path) -> Document:
    """Open a PDF and return its text lines as a normalized document (no block references).

    Text is grouped per line so multi-token labels (e.g. "RL 12.500") stay intact. Line positions
    are converted from PDF points to millimetres from the page's top-left origin. Pages are numbered
    from 1.
    """
    annotations: list[TextAnnotation] = []
    # pymupdf ships py.typed but leaves Document() unannotated, so the open() call reads as untyped.
    with pymupdf.open(path) as document:  # type: ignore[no-untyped-call]
        for page_number, page in enumerate(document, start=1):
            for block in page.get_text("dict")["blocks"]:
                if block.get("type") != _TEXT_BLOCK:
                    continue
                for line in block["lines"]:
                    text = "".join(span["text"] for span in line["spans"]).strip()
                    if not text:
                        continue
                    left, top, _right, _bottom = line["bbox"]
                    annotations.append(
                        TextAnnotation(
                            text=text,
                            source_file=path,
                            location=(left * _MM_PER_POINT, top * _MM_PER_POINT),
                            page=page_number,
                        )
                    )
    return Document(text_annotations=tuple(annotations))
