# Agent Framework Starter

A reusable, project-agnostic Claude Code agent framework — extracted and genericized from a production
setup, stripped of all game/engine/project specifics. Drop it into a new repo to give Claude Code a
disciplined bootstrap, a default developer role, a set of reusable skills, and the design standards that
keep the framework itself healthy.

Seeded for a **PDF + DWG architectural & structural drawing-analysis** project (concrete profiles, GA
drawings, post-tensioning details, slab depths, RLs for SSL), but everything except `ARCHITECTURE.md` and a
few library seed entries is domain-neutral.

## How it works

1. Claude Code auto-loads `CLAUDE.md` → it forces a read of `AGENTS.md`.
2. `AGENTS.md` routes to `runtime/bootstrap.md`, which activates a role, initializes tools (git),
   loads shared rules + the library index, and locks the workspace identity.
3. Roles define standing constraints; skills define on-demand procedures; the library holds design
   standards and (you add) domain knowledge.

## Layout

```
CLAUDE.md              session entry point
AGENTS.md              framework index (roles, skills, conventions)
ARCHITECTURE.md        TEMPLATE — fill in with your project's real structure + variables
CODING_STANDARDS.md    Python conventions + the (language-agnostic) comment / anti-AI-slop discipline
runtime/
  bootstrap.md         mandatory execution gate
  shared-rules.md      session-wide constraints
  model-tiers.md       abstract tier → model mapping
  mcp/git.md           version control: Check / Init / Verify + branch/commit discipline
roles/developer/       default role (Python developer)
skills/                code-review, deep-dive, markdown, commit, hand-off, summarise-session
library/
  library.md           always-loaded knowledge index
  standards/           agent-framework / agent-roles / agent-skills design docs
```

## First steps in a new repo

1. Copy these files to your repo root (or keep them in an `agents/` subfolder and adjust the `@AGENTS.md`
   import path in `CLAUDE.md`).
2. Fill in `ARCHITECTURE.md`: the `## Variables` table, subsystem map, and core systems.
3. Adjust `CODING_STANDARDS.md` if you change language (it's currently Python).
4. Add domain knowledge entries under `library/` as you learn the codebase.
5. Start a Claude Code session — it will run the bootstrap and report a locked identity.

## Stack note (why Python)

For PDF + DWG analysis the open-source Python ecosystem is the strongest: `ezdxf` is the benchmark DXF
library (pair with the ODA File Converter for DWG→DXF), `PyMuPDF`/`pdfplumber` lead PDF text/table
extraction, and `numpy`/`shapely`/`opencv` cover geometry. **C# + the commercial ODA SDK** is the fallback
if you need native DWG read/write without the converter step or tight Windows desktop integration — if you
go that way, re-template `CODING_STANDARDS.md` to C# and keep the Comments section verbatim.

## What was intentionally left out

Project- and engine-specific roles/skills (Unity, PM/Notion pipelines, QA/UX platform overlays,
Perforce-specific tooling) were dropped. This is the **curated generic core**: bootstrap + developer role +
coding standards + reusable dev skills + the agent-design standards. Add specialized roles/skills following
the patterns in `library/standards/`.
