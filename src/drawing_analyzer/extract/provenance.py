"""Map a normalized source item to domain provenance."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from drawing_analyzer.model import Provenance


class SourcePlaced(Protocol):
    """A source item that knows where it came from: any annotation or block reference.

    Members are read-only properties so frozen dataclass fields (which are read-only) match.
    """

    @property
    def source_file(self) -> Path: ...

    @property
    def layer(self) -> str | None: ...

    @property
    def location(self) -> tuple[float, float] | None: ...

    @property
    def page(self) -> int | None: ...


def provenance_of(item: SourcePlaced) -> Provenance:
    """Build the provenance record for a value extracted from ``item``."""
    return Provenance(
        source_file=item.source_file,
        page=item.page,
        layer=item.layer,
        location=item.location,
    )
