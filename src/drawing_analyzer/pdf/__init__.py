"""PDF extraction: text, tables, and vector lines, with an OCR fallback for scanned pages."""

from drawing_analyzer.pdf.reader import read_text_annotations

__all__ = ["read_text_annotations"]
