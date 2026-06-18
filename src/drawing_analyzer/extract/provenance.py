"""Map a normalized annotation to domain provenance."""

from __future__ import annotations

from drawing_analyzer.ingest.document import TextAnnotation
from drawing_analyzer.model import Provenance


def provenance_of(annotation: TextAnnotation) -> Provenance:
    """Build the provenance record for a value extracted from ``annotation``."""
    return Provenance(
        source_file=annotation.source_file,
        page=annotation.page,
        layer=annotation.layer,
        location=annotation.location,
    )
