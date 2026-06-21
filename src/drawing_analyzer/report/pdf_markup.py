"""Write detected values onto a PDF as review markup annotations."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pymupdf

from drawing_analyzer.model import Provenance, ReducedLevel, SlabProfile

_RED = (0.85, 0.0, 0.0)  # reduced levels
_BLUE = (0.0, 0.0, 0.85)  # slab depths
_CHAR_WIDTH_PT = 6.0  # rough width of one character at the label font size
_LINE_HEIGHT_PT = 14.0
_LABEL_GAP_PT = 4.0
_LABEL_FONT_SIZE = 9


def write_markup(
    source_pdf: Path,
    output_pdf: Path,
    reduced_levels: Iterable[ReducedLevel],
    slab_profiles: Iterable[SlabProfile],
) -> int:
    """Mark each detected value on a copy of the PDF and save it, returning the number marked.

    Each value gets a coloured box around where it was read plus a label showing its millimetre
    value. Values with no page or location cannot be placed and are skipped.
    """
    drawn = 0
    with pymupdf.open(source_pdf) as document:  # type: ignore[no-untyped-call]
        for level in reduced_levels:
            kind = "SSL" if level.is_structural_slab_level else "RL"
            label = f"{kind} {level.elevation_mm:g}mm"
            if _mark(document, level.provenance, level.label, label, _RED):
                drawn += 1
        for profile in slab_profiles:
            detected = profile.label or "slab"
            label = f"slab {profile.depth_mm:g}mm"
            if _mark(document, profile.provenance, detected, label, _BLUE):
                drawn += 1
        document.save(output_pdf)
    return drawn


def _mark(
    document: Any,
    provenance: Provenance,
    detected_text: str,
    label: str,
    color: tuple[float, float, float],
) -> bool:
    if provenance.page is None or provenance.location is None:
        return False
    page = document[provenance.page - 1]
    left, top = provenance.location

    box = pymupdf.Rect(  # type: ignore[no-untyped-call]
        left, top, left + len(detected_text) * _CHAR_WIDTH_PT, top + _LINE_HEIGHT_PT
    )
    outline = page.add_rect_annot(box)
    outline.set_colors(stroke=color)
    outline.set_border(width=1.2)
    outline.set_info(content=label)
    outline.update()

    label_left = box.x1 + _LABEL_GAP_PT
    label_box = pymupdf.Rect(  # type: ignore[no-untyped-call]
        label_left, top, label_left + len(label) * _CHAR_WIDTH_PT, top + _LINE_HEIGHT_PT
    )
    note = page.add_freetext_annot(label_box, label, fontsize=_LABEL_FONT_SIZE, text_color=color)
    note.update()
    return True
