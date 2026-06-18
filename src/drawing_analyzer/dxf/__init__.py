"""DXF parsing: resolve entities to geometry, handle layers/blocks and unit/scale conversion."""

from drawing_analyzer.dxf.reader import read_text_annotations

__all__ = ["read_text_annotations"]
