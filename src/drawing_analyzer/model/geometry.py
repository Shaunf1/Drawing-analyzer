"""Geometric primitives shared across the domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point:
    """A 2D point in drawing coordinates, measured in millimetres from the drawing origin."""

    x_mm: float
    y_mm: float
