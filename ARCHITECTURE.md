# ARCHITECTURE.md

Project structure, variables, and subsystem map. The framework reads this file to resolve where
systems live and to look up `## Variables`. Keep it accurate as the code takes shape.

## Overview

Drawing Analyzer is a pipeline that ingests architectural and structural drawings (PDF and DWG/DXF)
and extracts structured data — concrete profiles, general-arrangement (GA) drawing elements,
post-tensioning / post-dressing details, structural slab depths, and Reduced Levels (RLs) for
Structural Slab Level (SSL) — into a queryable model for downstream checking and reporting. It serves
structural engineers and reviewers who need to pull verifiable values off drawings without reading
each sheet by hand.

## Variables

| Key | Value | Notes |
|-----|-------|-------|
| LANGUAGE | `python` | primary implementation language |
| PYTHON_VERSION | `3.12` | pinned in `pyproject.toml` (`requires-python = ">=3.12"`) |
| PACKAGE_NAME | `drawing_analyzer` | importable package |
| PACKAGE_ROOT | `src/drawing_analyzer` | importable package location (src layout) |
| TEST_ROOT | `tests` | mirrors the package tree |
| ODA_CONVERTER_PATH | `<env var: ODA_CONVERTER_PATH>` | ODA File Converter, for DWG->DXF (set via env var, never hardcode) |
| SAMPLE_DATA_DIR | `tests/fixtures/drawings` | sample PDFs/DWGs for tests (keep large/real files out of git) |

Add a row whenever a role, skill, or tool needs a value. Use `UPPER_SNAKE_CASE`. Never hardcode a value
that belongs here.

## Tech stack

- **Language:** Python (see the stack rationale in the README).
- **DWG/DXF:** `ezdxf` for DXF parsing; **ODA File Converter** to convert proprietary `.dwg` -> `.dxf`
  first. (`etacad` builds structural-element drawings on ezdxf if useful.)
- **PDF:** `PyMuPDF` (fitz) for fast text/vector extraction and `page.find_tables()`; `pdfplumber` for
  precision table work; **Tesseract** (`pytesseract`) for scanned/raster pages.
- **Geometry / numerics:** `numpy`, optionally `shapely` for polygon/profile operations and `opencv` for
  raster line detection.
- **Tooling:** `ruff` (lint+format), `mypy` (types), `pytest` (tests). Configured in `pyproject.toml`.

## Subsystem map

| Subsystem | Location | Responsibility |
|-----------|----------|----------------|
| Ingestion | `src/drawing_analyzer/ingest/` | open PDF/DWG, normalize to an internal document model, run ODA conversion |
| DXF parsing | `src/drawing_analyzer/dxf/` | entities -> geometry, layer/block resolution, unit/scale handling |
| PDF extraction | `src/drawing_analyzer/pdf/` | text, tables, vector lines; OCR fallback |
| Domain model | `src/drawing_analyzer/model/` | dataclasses: SlabProfile, GAElement, ReducedLevel, etc. |
| Extractors | `src/drawing_analyzer/extract/` | recognize concrete profiles, slab depths, RLs/SSLs from parsed content |
| Reporting | `src/drawing_analyzer/report/` | structured output (JSON/CSV), checks, summaries |
| CLI | `src/drawing_analyzer/cli.py` | command-line entry point |

## Core systems

Systems that warrant **deep** review when changed (used by the code-review skill for depth-tier
classification).

| System | Why deep review |
|--------|-----------------|
| DXF parsing | geometry/units errors silently corrupt every downstream extraction |
| PDF extraction | layout/table heuristics are fragile; regressions are easy to miss |
| Domain model | high fan-out; a schema change ripples through extractors and reporting |
| RL/SSL extraction | a units or datum bug produces plausible-but-wrong levels — high-stakes |

## Conventions specific to this project

- Carry **units** explicitly in the domain model (store millimetres; never mix mm/m implicitly).
- Record **provenance** on every extracted value (source file, page/layer, coordinates) for traceability.
- Keep large or client-confidential drawings **out of git**; commit small redacted fixtures only.
