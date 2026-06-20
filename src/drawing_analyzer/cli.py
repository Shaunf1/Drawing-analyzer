"""Command-line entry point for the drawing-analyzer pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from drawing_analyzer.extract import extract_reduced_levels, extract_slab_depths
from drawing_analyzer.ingest import read_annotations
from drawing_analyzer.report import extraction_to_json


def main(argv: list[str] | None = None) -> int:
    """Extract reduced levels and slab depths from a DXF or PDF drawing and print them as JSON.

    Returns a process exit code.
    """
    parser = argparse.ArgumentParser(
        prog="drawing-analyzer",
        description="Extract reduced levels (RL/SSL) and slab depths from a DXF or PDF drawing.",
    )
    parser.add_argument("drawing", type=Path, help="path to a .dxf or .pdf drawing")
    args = parser.parse_args(argv)

    try:
        annotations = read_annotations(args.drawing)
    except ValueError as error:
        parser.error(str(error))

    levels = extract_reduced_levels(annotations)
    slabs = extract_slab_depths(annotations)
    print(extraction_to_json(levels, slabs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
