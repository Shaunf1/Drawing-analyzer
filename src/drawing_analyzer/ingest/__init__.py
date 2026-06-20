"""Ingestion: open PDF/DWG sources, run ODA DWG->DXF conversion, normalize to a document model."""

from drawing_analyzer.ingest.document import TextAnnotation
from drawing_analyzer.ingest.reader import read_annotations

__all__ = ["TextAnnotation", "read_annotations"]
