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

## Domain

Version-specific or fast-moving knowledge the project depends on. Each entry carries a `last_updated`
and `staleness_threshold_days`; update it whenever a task surfaces new knowledge.

| File | Covers / load when | Staleness |
|------|--------------------|-----------|
| [domain/dwg-dxf.md](domain/dwg-dxf.md) | ezdxf entity model (TEXT/MTEXT, layers, units), reading documents, DWG->DXF via the ODA File Converter add-on. Load when working in `dxf/` or `ingest/`. | 120 days |
| [domain/pdf-extraction.md](domain/pdf-extraction.md) | PyMuPDF vs pdfplumber trade-offs, `get_text()` modes, `page.find_tables()`, vector vs scanned pages, OCR fallback (Tesseract), coordinate systems. Load when building `pdf/`. | 90 days |
| [domain/structural-conventions.md](domain/structural-conventions.md) | RL (Reduced Level) and SSL (Structural Slab Level) notation, slab-depth conventions, annotation patterns to parse. Load when working in `extract/`. | 365 days |
