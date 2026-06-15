---
last_updated: 2026-06-15
---

# Knowledge Library — Index

Always-loaded index. Before any task, check the relevant entry; if `today − last_updated >
staleness_threshold_days`, research online and update the entry before relying on it.

## Standards

| File | Covers / load when | Staleness |
|------|--------------------|-----------|
| [standards/agent-framework.md](standards/agent-framework.md) | Framework design: CLAUDE.md/AGENTS.md structure, bootstrap gate, context budget, memory hierarchy, multi-agent coordination, compress-don't-promote. Load when setting up or auditing the framework. | 30 days |
| [standards/agent-roles.md](standards/agent-roles.md) | Role design: anatomy, activation, consulting vs activating, role-vs-skill boundary, scope discipline, anti-patterns. Load when authoring/reviewing a role. | 30 days |
| [standards/agent-skills.md](standards/agent-skills.md) | Skill design: anatomy, trigger-first phrasing, progressive disclosure, trim-don't-promote, model tiers, anti-patterns. Load when authoring/reviewing a skill. | 30 days |

## Domain (add as the project grows)

Create entries here for version-specific or fast-moving knowledge the project depends on — e.g. a
`domain/pdf-extraction.md` (PyMuPDF/pdfplumber API surface, table-detection gotchas) or
`domain/dwg-dxf.md` (ezdxf entity model, ODA File Converter workflow, coordinate/unit conventions). Give
each a `last_updated` and `staleness_threshold_days`, and update it whenever a task surfaces new knowledge.

Suggested seed entries for this project:

| File (to create) | Covers |
|------|--------|
| `domain/dwg-dxf.md` | ezdxf entity model (LINE/LWPOLYLINE/TEXT/INSERT/DIMENSION), layer conventions, blocks/xrefs, DWG→DXF via ODA File Converter, unit/scale handling |
| `domain/pdf-extraction.md` | PyMuPDF vs pdfplumber trade-offs, `page.find_tables()`, vector vs scanned pages, OCR fallback (Tesseract), coordinate systems |
| `domain/structural-conventions.md` | RL (Reduced Level) and SSL (Structural Slab Level) notation, slab-depth/GA-drawing conventions, annotation patterns to parse |
