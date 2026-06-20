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
from drawing_analyzer.report import extraction_to_json


def main(argv: list[str] | None = None) -> int:
    """Extract reduced levels, slab depths, and GA elements from a drawing and print them as JSON.

    Accepts a DXF or PDF drawing. Returns a process exit code.
    """
    parser = argparse.ArgumentParser(
        prog="drawing-analyzer",
        description="Extract reduced levels (RL/SSL), slab depths, and GA elements from a drawing.",
    )
    parser.add_argument("drawing", type=Path, help="path to a .dxf or .pdf drawing")
    args = parser.parse_args(argv)

    try:
        document = read_document(args.drawing)
    except ValueError as error:
        parser.error(str(error))

    levels = extract_reduced_levels(document.text_annotations)
    slabs = extract_slab_depths(document.text_annotations)
    ga_elements = extract_ga_elements(document.block_references)
    print(extraction_to_json(levels, slabs, ga_elements))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
