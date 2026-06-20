---
last_updated: 2026-06-20
staleness_threshold_days: 365
---

# Structural drawing conventions (RL / SSL / slab depths)

Domain notation the extractors recognize. This is field convention, not a library API; it changes
slowly but varies by office and region, so treat patterns as defaults to widen against real drawings.

## Reduced Level (RL)

- A **Reduced Level** is a height relative to a fixed survey datum, conventionally written in **metres**
  on drawings, e.g. `RL 12.500`. The project domain model stores millimetres, so a parsed RL is
  multiplied by 1000 (`extract_reduced_levels` does this).
- Annotations vary: `RL 12.500`, `R.L. 12.500`, `RL+12.500`, `RL -1.250`. The current extractor matches
  `RL` or `SSL` followed by an optional separator and a signed decimal; broaden the pattern as new forms
  appear rather than special-casing call sites.

## Structural Slab Level (SSL)

- **SSL** is the RL of the top of the structural slab (before finishes/screed). Distinct from FFL
  (Finished Floor Level) and FL. An SSL is a kind of RL; the model flags it with
  `is_structural_slab_level` rather than a separate type.
- Other level prefixes seen on structural drawings: FFL, FL, TOS (top of steel), TOC (top of concrete),
  IL (invert level). Not yet extracted; add them as kinds/flags when needed.

## Slab depths and profiles

- Slab depth (thickness) is annotated in **millimetres**, e.g. `200 THK` or `SLAB 300`. Store directly
  as millimetres (no metre conversion, unlike RLs) on `SlabProfile.depth_mm`.
- A "concrete profile" is the section/outline of a concrete element; capture the boundary as a
  millimetre polyline (`SlabProfile.outline`) when geometry is recoverable.

## General-arrangement (GA) elements

- Structural members on a GA drawing are typically placed as **block references** (DXF INSERT), not
  loose geometry, so the block name is the main classification signal.
- `extract_ga_elements` classifies each block by keyword in its name: `COL` -> column, `BEAM` -> beam,
  `WALL` -> wall, `SLAB` -> slab, otherwise `OTHER`. Block naming is not standardized across offices,
  so treat the keyword list as a default to widen against real drawings rather than a fixed schema.
- Every block reference becomes one `GAElement` (unknown names get `OTHER`) so nothing is silently
  dropped; filter by kind downstream if title blocks or grid bubbles are noise.

## Provenance and units, always

- Levels are easy to misread by a factor of 1000 (m vs mm) or against the wrong datum. Every extracted
  value carries `Provenance` (source file, page/layer, location) so a reviewer can trace it back, and
  units are explicit in field names (`elevation_mm`, `depth_mm`). See
  [ARCHITECTURE.md](../../ARCHITECTURE.md) "Conventions specific to this project".
