"""Route a drawing file to the reader for its format and return normalized annotations."""

from __future__ import annotations

from pathlib import Path

from drawing_analyzer.ingest.document import TextAnnotation


def read_annotations(path: Path) -> list[TextAnnotation]:
    """Read text annotations from a DXF or PDF drawing, dispatching on the file extension.

    Readers are imported lazily so a DXF run does not import the PDF stack, and vice versa. Raises
    ``ValueError`` for an unsupported extension.
    """
    suffix = path.suffix.lower()
    if suffix == ".dxf":
        from drawing_analyzer.dxf import read_text_annotations

        return read_text_annotations(path)
    if suffix == ".pdf":
        from drawing_analyzer.pdf import read_text_annotations

        return read_text_annotations(path)
    raise ValueError(f"unsupported drawing format: {suffix or path.name!r}")
