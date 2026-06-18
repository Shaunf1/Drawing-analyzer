"""Smoke tests: the package and each subsystem import cleanly."""

import importlib

import drawing_analyzer

SUBSYSTEMS = ["ingest", "dxf", "pdf", "model", "extract", "report", "cli"]


def test_package_exposes_version() -> None:
    assert drawing_analyzer.__version__


def test_subsystems_import() -> None:
    for name in SUBSYSTEMS:
        importlib.import_module(f"drawing_analyzer.{name}")
