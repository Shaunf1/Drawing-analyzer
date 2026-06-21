"""Command-line entry point for the drawing-analyzer pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from drawing_analyzer.extract import (
    extract_ga_elements,
    extract_reduced_levels,
    extract_slab_depths,
)
from drawing_analyzer.ingest import read_document
from drawing_analyzer.report import extraction_to_csv, extraction_to_json, write_markup


def main(argv: list[str] | None = None) -> int:
    """Extract reduced levels, slab depths, and GA elements from a drawing.

    Prints the extraction as JSON (default) or CSV, or with --markup writes an annotated copy of a
    PDF drawing with the detected values marked. Accepts a DXF or PDF drawing. Returns an exit code.
    """
    parser = argparse.ArgumentParser(
        prog="drawing-analyzer",
        description="Extract reduced levels (RL/SSL), slab depths, and GA elements from a drawing.",
    )
    parser.add_argument("drawing", type=Path, help="path to a .dxf or .pdf drawing")
    parser.add_argument(
        "--format",
        choices=("json", "csv"),
        default="json",
        help="output format (default: json)",
    )
    parser.add_argument(
        "--markup",
        type=Path,
        default=None,
        metavar="OUTPUT_PDF",
        help="write an annotated PDF copy with detected values marked (PDF input only)",
    )
    args = parser.parse_args(argv)

    try:
        document = read_document(args.drawing)
    except ValueError as error:
        parser.error(str(error))

    levels = extract_reduced_levels(document.text_annotations)
    slabs = extract_slab_depths(document.text_annotations)
    ga_elements = extract_ga_elements(document.block_references)

    if args.markup is not None:
        if args.drawing.suffix.lower() != ".pdf":
            parser.error("--markup requires a .pdf drawing")
        marked = write_markup(args.drawing, args.markup, levels, slabs)
        print(f"wrote {marked} markup annotations to {args.markup}")
        return 0

    if args.format == "csv":
        print(extraction_to_csv(levels, slabs, ga_elements), end="")
    else:
        print(extraction_to_json(levels, slabs, ga_elements))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
