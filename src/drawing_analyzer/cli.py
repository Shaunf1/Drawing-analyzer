"""Command-line entry point for the drawing-analyzer pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from drawing_analyzer.dxf import read_text_annotations
from drawing_analyzer.extract import extract_reduced_levels
from drawing_analyzer.report import reduced_levels_to_json


def main(argv: list[str] | None = None) -> int:
    """Extract reduced levels from a DXF drawing and print them as JSON. Returns an exit code."""
    parser = argparse.ArgumentParser(
        prog="drawing-analyzer",
        description="Extract reduced levels (RL/SSL) from a DXF drawing.",
    )
    parser.add_argument("drawing", type=Path, help="path to a .dxf drawing")
    args = parser.parse_args(argv)

    if args.drawing.suffix.lower() != ".dxf":
        parser.error("only .dxf drawings are supported for now")

    annotations = read_text_annotations(args.drawing)
    levels = extract_reduced_levels(annotations)
    print(reduced_levels_to_json(levels))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
