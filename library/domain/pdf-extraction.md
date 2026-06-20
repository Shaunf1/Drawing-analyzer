---
last_updated: 2026-06-18
staleness_threshold_days: 90
---

# PDF extraction (PyMuPDF / pdfplumber / OCR)

PyMuPDF (`pymupdf>=1.24`) is a project dependency; the text-extraction facts below are verified against
the installed package. pdfplumber is not yet used. The table and OCR sections remain research-level
until that code is written, so re-verify them then.

The PDF reader (`drawing_analyzer.pdf.reader`) extracts one `TextAnnotation` per text line via
`get_text("dict")`, joining a line's spans so multi-token labels like "RL 12.500" stay intact.

## Library choice

- **PyMuPDF (fitz):** fast text, vector, and table extraction. Modern import is `import pymupdf`;
  `import fitz` is a still-supported legacy alias. `pymupdf.open(path)` returns a `Document`; iterate
  pages with `for page in doc:`.
- **pdfplumber:** slower but precise word/line/table geometry; reach for it when PyMuPDF's table
  heuristics miss. Good for ruled tables and exact bounding boxes.

## Text extraction (PyMuPDF)

- `page.get_text(option)` where option is:
  - `"text"` plain text in reading order (fastest),
  - `"words"` list of words with bounding boxes,
  - `"blocks"` paragraph/image blocks with boxes,
  - `"dict"` / `"rawdict"` full structure with fonts, spans, and coordinates.
- Coordinates are in PDF points (1/72 inch), origin top-left. This is the source-native unit to record
  in `Provenance.location`; it is not millimetres.

## Tables

- `page.find_tables()` (added in PyMuPDF 1.23.0) returns a finder whose `.tables` each expose
  `.extract()` (list of row lists) and `.to_pandas()`. The table API has shifted across 1.23/1.24, so
  pin and re-verify.

## Scanned / raster pages

- A page with no text layer yields empty `get_text()`. Detect this (empty text + present images) and
  fall back to OCR.
- PyMuPDF can OCR via Tesseract (`page.get_textpage_ocr(...)`, requires Tesseract installed) or render
  to a pixmap and run `pytesseract` directly. OCR is slow and error-prone on drawings, dense with thin
  annotation; treat OCR output as low-confidence and keep provenance.

## Gotchas

- Open the document once and page through it; `Document` holds the file mapped until `close()` (use a
  `with` block).
- Vector line work (for GA geometry) uses `page.get_drawings()`, separate from text extraction.

## Sources

- [PyMuPDF docs](https://pymupdf.readthedocs.io/) and
  [find_tables write-up](https://medium.com/@pymupdf/table-recognition-and-extraction-with-pymupdf-54e54b40b760).
