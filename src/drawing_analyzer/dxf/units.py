"""Convert DXF drawing-unit coordinates to millimetres via the $INSUNITS header code."""

from __future__ import annotations

# Millimetres per drawing unit, keyed by $INSUNITS code. Factors match ezdxf's own unit table.
# Codes absent here (notably 0, unitless) mean the drawing declares no usable scale.
_MILLIMETRES_PER_UNIT: dict[int, float] = {
    1: 25.4,  # inches
    2: 304.8,  # feet
    4: 1.0,  # millimetres
    5: 10.0,  # centimetres
    6: 1000.0,  # metres
}


def millimetres_per_unit(insunits: int) -> float | None:
    """Return millimetres per drawing unit for an $INSUNITS code.

    Returns None when the drawing is unitless (code 0) or uses a unit outside the supported set, so
    callers decide how to handle an unknown scale rather than silently assuming millimetres.
    """
    return _MILLIMETRES_PER_UNIT.get(insunits)
