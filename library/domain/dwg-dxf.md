---
last_updated: 2026-06-16
staleness_threshold_days: 120
---

# DWG / DXF parsing with ezdxf

Verified against **ezdxf 1.4.4** (the pinned dependency). Re-check when bumping ezdxf.

## Reading a document

- `from ezdxf.filemanagement import readfile` then `doc = readfile(path)`. The top-level
  `ezdxf.readfile` is the same function; importing from `ezdxf.filemanagement` keeps strict mypy
  happy (the top-level alias is not in `ezdxf.__all__`).
- `doc.modelspace()` returns the modelspace; `doc.units` is an integer `$INSUNITS` code.
- Query entities by type with a space-separated DXF-type string: `msp.query("TEXT MTEXT")` returns
  an iterable `EntityQuery`.

## Entities

- Concrete classes live in their defining modules: `from ezdxf.entities.text import Text`,
  `from ezdxf.entities.mtext import MText`. Importing from `ezdxf.entities` trips no-implicit-reexport
  under mypy strict, so import from the submodule.
- `entity.dxftype()` gives the DXF type string ("TEXT", "MTEXT"); `entity.dxf.layer` is the layer.
- **TEXT:** `entity.dxf.text` is the string; `entity.dxf.insert` is the insertion point.
- **MTEXT:** `entity.text` is the raw content with inline formatting codes (e.g. `\P` for a
  paragraph break); `entity.plain_text()` decodes them (so `\P` becomes `\n`). Its return type is
  `list[str] | str` (a list only when called with `split=True`); narrow with `isinstance` before use.
- `entity.dxf.insert` is a `Vec3` — index access raises; use `.x` / `.y` / `.z`.

## Units and scale

- `$INSUNITS` codes via `ezdxf.units`: `MM` = 4, `M` = 6 (also CM, INCH, FEET, etc.). `doc.units`
  returns the raw int. A document may carry `0` (unitless), so a parser must not assume millimetres.
- Coordinates from entities are in the document's drawing units, **not** millimetres. Scaling to the
  domain model's millimetres belongs in the DXF subsystem, not in extractors.

## DWG -> DXF (ODA File Converter)

- `.dwg` is proprietary; ezdxf cannot read it directly. The `ezdxf.addons.odafc` add-on shells out to
  the externally installed **ODA File Converter**.
- `odafc.is_installed()` checks availability; `odafc.readfile(path, version=None, *, audit=False)`
  converts a DWG/DXB/DXF to a temp DXF and loads it; `odafc.export_dwg(doc, path, version=...)` writes
  DWG; `odafc.convert(...)` converts between formats.
- The converter must be installed by the user. Its path is configured (Linux/macOS via the
  `unix_exec_path` option, Windows defaults to the Program Files install). Store the path in the
  `ODA_CONVERTER_PATH` variable (see ARCHITECTURE.md), never hardcode it.

## Sources

- [ezdxf 1.4.4 docs](https://ezdxf.readthedocs.io/) and the
  [odafc add-on docs](https://ezdxf.readthedocs.io/en/stable/addons/odafc.html). API specifics above
  were confirmed by introspecting the installed package.
