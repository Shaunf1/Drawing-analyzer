"""The ingest dispatcher routes by extension and rejects unknown formats."""

from pathlib import Path

import pytest

from drawing_analyzer.ingest import read_annotations


def test_rejects_unsupported_extension(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unsupported drawing format"):
        read_annotations(tmp_path / "plan.txt")
