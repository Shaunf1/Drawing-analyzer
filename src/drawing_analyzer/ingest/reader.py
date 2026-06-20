"""Route a drawing file to the reader for its format and return a normalized document."""

from __future__ import annotations

from pathlib import Path

from drawing_analyzer.ingest.document import Document


def read_document(path: Path) -> Document:
    """Read a DXF or PDF drawing into a normalized document, dispatching on the file extension.

    Readers are imported lazily so a DXF run does not import the PDF stack, and vice versa. Raises
    ``ValueError`` for an unsupported extension.
    """
    suffix = path.suffix.lower()
    if suffix == ".dxf":
        from drawing_analyzer.dxf import read_dxf

        return read_dxf(path)
    if suffix == ".pdf":
        from drawing_analyzer.pdf import read_pdf

        return read_pdf(path)
    raise ValueError(f"unsupported drawing format: {suffix or path.name!r}")
