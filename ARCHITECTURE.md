# ARCHITECTURE.md — Template

> **This is a template.** Replace the bracketed placeholders and example content with your project's real
> structure as it takes shape. It is seeded for a PDF/DWG architectural & structural drawing-analysis tool;
> delete what doesn't apply. Keep it accurate — the framework reads this file to resolve where systems live
> and to look up `## Variables`.

## Overview

[One paragraph: what the software does and for whom.]

Example: A pipeline that ingests architectural and structural drawings (PDF and DWG/DXF) and extracts
structured data — concrete profiles, general-arrangement (GA) drawing elements, post-tensioning /
post-dressing details, structural slab depths, and Reduced Levels (RLs) for Structural Slab Level (SSL) —
into a queryable model for downstream checking and reporting.

## Variables

| Key | Value | Notes |
|-----|-------|-------|
| LANGUAGE | `python` | primary implementation language |
| PYTHON_VERSION | `3.12` | pin in `pyproject.toml` |
| PACKAGE_ROOT | `src/<package_name>` | importable package location |
| TEST_ROOT | `tests` | mirrors the package tree |
| ODA_CONVERTER_PATH | `<path-or-env-var>` | ODA File Converter, for DWG→DXF (set via env var, never hardcode) |
| SAMPLE_DATA_DIR | `tests/fixtures/drawings` | sample PDFs/DWGs for tests (keep large/real files out of git) |

Add a row whenever a role, skill, or tool needs a value. Use `UPPER_SNAKE_CASE`. Never hardcode a value that
belongs here.

## Tech stack

- **Language:** Python (see the stack rationale in the README).
- **DWG/DXF:** `ezdxf` for DXF parsing; **ODA File Converter** to convert proprietary `.dwg` → `.dxf` first.
  (`etacad` builds structural-element drawings on ezdxf if useful.)
- **PDF:** `PyMuPDF` (fitz) for fast text/vector extraction and `page.find_tables()`; `pdfplumber` for
  precision table work; **Tesseract** (`pytesseract`) for scanned/raster pages.
- **Geometry / numerics:** `numpy`, optionally `shapely` for polygon/profile operations and `opencv` for
  raster line detection.
- **Tooling:** `ruff` (lint+format), `mypy`/`pyright` (types), `pytest` (tests).

## Subsystem map

Replace with real module paths as they form. Suggested decomposition:

| Subsystem | Location (suggested) | Responsibility |
|-----------|----------------------|----------------|
| Ingestion | `src/<pkg>/ingest/` | open PDF/DWG, normalize to an internal document model, run ODA conversion |
| DXF parsing | `src/<pkg>/dxf/` | entities → geometry, layer/block resolution, unit/scale handling |
| PDF extraction | `src/<pkg>/pdf/` | text, tables, vector lines; OCR fallback |
| Domain model | `src/<pkg>/model/` | dataclasses: SlabProfile, GAElement, ReducedLevel, etc. |
| Extractors | `src/<pkg>/extract/` | recognize concrete profiles, slab depths, RLs/SSLs from parsed content |
| Reporting | `src/<pkg>/report/` | structured output (JSON/CSV), checks, summaries |
| CLI / API | `src/<pkg>/cli.py` | entry points |

## Core systems

Systems that warrant **deep** review when changed (used by the code-review skill for depth-tier classification).

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
