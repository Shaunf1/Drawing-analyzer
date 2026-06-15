---
name: markdown
description: Required for every `Write` / `Edit` of a framework `*.md` file (AGENTS.md, SKILL.md, role/runtime/library docs). Mode A (pre-change) finds placement and pre-existing coverage; Mode B (post-change) reviews for duplication, staleness, scope, and altitude. Skip only for typo / whitespace, mechanical refactor with no semantic change, or a Mode B follow-up edit — and announce the skip out loud.
---

# Skill: Markdown

## Trigger

A `Write` or `Edit` whose path is a framework markdown file (this file included).

- **Before** the call: run **Mode A** in the same turn (inline is fine — answer the placement
  questions out loud).
- **After** the change lands: run **Mode B** before the turn ends.
- **Exempt** (announce, e.g. `Skipping Mode A: typo fix`): typo / whitespace; mechanical refactor with
  no semantic change; Mode B's own follow-ups. Silent skip = workflow violation.

## Model

Tier: standard | Quality: normal

## Mode A — Structure Analysis (before writing)

Determine where content belongs and whether it already exists, so the write is right the first time.

1. Read the target file(s) where the content might go.
2. Trace the dependency graph — what references them, what they reference (`@includes`, links,
   `## Required tools`).
3. Answer:
   - **Placement** — which file and section is the correct home?
   - **Pre-existing coverage** — does an equivalent already exist? Is the altitude right (specific
     without duplicating a more-general source)?
   - **Downstream impact** — which other files reference this area and need a pointer update?
4. Output a 3–5 bullet placement recommendation. Write nothing during Mode A.

## Mode B — Review (after changing files)

Scope: only the file(s) changed this session.

**Guiding principle: right altitude.** Minimal ≠ short. Docs fail two ways — too verbose (repeats
general knowledge, pads with prose that doesn't change behaviour) or too vague (trims a precondition or
known pitfall that changes behaviour). Target one sentence of load-bearing context per non-obvious step.

**Checks:**

1. **Duplication** — same instruction elsewhere. Keep it in the most general file; remove the rest.
2. **Staleness** — references tools, fields, or paths that no longer exist.
3. **Contradictions** — conflicts with another file. Pick one authoritative source.
4. **Bloat** — prose that doesn't change agent behaviour. Cut it. Prefer bullets, imperative voice.
5. **Over-compression** — trimmed past the point a first-time reader avoids a known failure mode.
   Restore the minimum caveat (often a "but if X…" clause) or a pointer to the longer section.
6. **Structure** — tool modules have Check / Init / Verify + Warm-start verify; roles and skills declare
   `## Required tools` and `name` + `description` frontmatter.
7. **Scope** — shared/framework content stays generic and project-agnostic. Red flags: project names,
   project-specific paths or system names, concrete platform pins, project-specific tool/env references.
   Project-specific content belongs in a project overlay or ARCHITECTURE.md.
8. **Trigger-first phrasing** — the first phrase of `description:` and of the body's first heading must
   name the trigger (tool + path glob, or specific user phrases), not the skill's philosophy. See
   [library/standards/agent-skills.md → Trigger-first phrasing](../../library/standards/agent-skills.md).
9. **Compress, don't promote** — `**CRITICAL**` / `**MANDATORY**` blocks where a one-sentence imperative
   with a concrete tool + path would do are violations. Adding more tier labels to a skipped rule is the
   wrong move; trim and restructure instead. See
   [library/standards/agent-framework.md](../../library/standards/agent-framework.md).
10. **Body length** — a SKILL.md body over ~300–500 lines is a warning sign; extract per-step procedures
    into sibling `references/*.md` and link from SKILL.md.

**Output:** fix issues directly (files are already open for edit). Report findings per file in under
150 words; omit files with no findings.

## Design principles

The structural rules above derive from the library design docs — consult them when a review touches a
structural decision (split a file, role vs skill, elevate vs trim a label):
[agent-skills.md](../../library/standards/agent-skills.md),
[agent-framework.md](../../library/standards/agent-framework.md).
