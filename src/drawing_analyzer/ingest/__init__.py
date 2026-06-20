"""Ingestion: open PDF/DWG sources, run ODA DWG->DXF conversion, normalize to a document model."""

from drawing_analyzer.ingest.document import BlockReference, Document, TextAnnotation
from drawing_analyzer.ingest.reader import read_document

__all__ = ["BlockReference", "Document", "TextAnnotation", "read_document"]
