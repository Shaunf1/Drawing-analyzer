---
name: Agent Skill Design Standards
last_updated: 2026-06-15
staleness_threshold_days: 30
tags: [agent, skills, claude-code, skill-design, context-engineering]
---

# Agent Skill Design Standards

Reference for designing, writing, or reviewing `SKILL.md` files. Load before creating a skill, refactoring
one, or diagnosing why a skill isn't triggering.

## Skill anatomy

Every skill is a directory; the minimum is `SKILL.md` with YAML frontmatter. Sibling files load on demand.

```
my-skill/
├── SKILL.md            # mandatory — frontmatter + core instructions
├── references/*.md     # heavy/edge-case content — loaded only when needed
└── scripts/*.py        # executed via bash; source never enters context
```

**Mandatory frontmatter:** `name` (kebab-case, ≤64 chars) and `description` (third person, ≤1024 chars,
includes the domain terms that appear in real requests). The `description` is injected into the system
prompt at session start (~100 tokens) and is the *only* thing read until the skill fires — invest in it.

**Recommended:** `model` (tier), `triggers` (example phrasings), `required_mcps` / `required tools`.

## Right-altitude writing — two failure modes

1. **Too verbose** — hardcoded prose for every sub-case; bloated context, low signal, buried critical
   instructions. A body over 500 lines is a warning sign.
2. **Too vague** — high-level direction with no concrete signals; Claude can't tell which library, flag, or
   error to handle, so it trial-and-errors what should have been encoded.

Target: specific enough to guide, flexible enough not to break on variation. Test every paragraph: "Does
Claude need this, or does it already know it?" Keep load-bearing values inline; give direction only where
Claude can reason independently.

## Trigger precision and trigger-first phrasing

The `description` is the trigger. Pattern: `[what it does] + [when to use / key domain terms]`. Include
synonyms from real requests ("test plan", "QA checklist", "acceptance criteria" may all mean one thing).
Write in third person — first-person phrasing degrades triggering.

The **first phrase** of `description:` is what every autoloader (Claude Code, Cursor, Gemini CLI, Codex)
reads first. Put the tool name and path glob (or specific user phrases) there, not the skill's philosophy:

```yaml
# Good — trigger first
description: Required for every `Write` / `Edit` of `docs/**/*.md`. Mode A finds placement; Mode B reviews.
# Bad — trigger buried after 30 tokens of what-it-does prose
description: A two-mode markdown discipline skill that analyses placement and dependencies... use before editing docs.
```

The same applies to the body's first heading — lead with a `## Trigger` block, not prose about philosophy.

## Enforcement: trim, don't promote

Adding `**MANDATORY**` to a skipped rule makes adherence *worse*. Autoloaders match structure, not intensity;
tier labels consume budget that competes with the trigger. In order: (1) move the trigger to the first phrase
of `description:` and the first heading; (2) cut competing prose; (3) add concrete tool+path patterns; (4)
optionally layer a harness/git hook on top, flagging the one-time user setup. See
[agent-framework.md](agent-framework.md).

## Progressive disclosure

| Level | Loaded | Cost | Content |
|---|---|---|---|
| Metadata | always | ~100 tok/skill | `name` + `description` |
| Core | when the skill fires | <5k tok ideally | SKILL.md body |
| Sibling files | on demand via pointer | ~unbounded | references, scripts, templates |

Keep SKILL.md lean — an overview and navigation doc. Over ~300–500 lines, split specialist content into
sibling `references/*.md` and point to them. Keep references **one level deep** (SKILL.md → reference, not a
chain) — preview reads of intermediary files cause incomplete information.

## Model tier declaration

Skills needing high reasoning, or that run as long sub-agent tasks, declare a `## Model` section (or `model:`
frontmatter). No section → runs inline on the current session model. Inline suits short deterministic
procedures; sub-agent (a higher tier) suits open-ended investigation and sustained multi-step reasoning.
Sub-agents return condensed summaries (1–2k tokens), not raw records.

## Scope discipline

Shared skills must be project-agnostic — no hardcoded paths, project names, IDs, or version-specific APIs.
Concrete values go in project overlay skills. When resolving an ambiguity reveals a project-specific value,
record the generic pattern in the shared skill and the concrete value in the overlay.

## Skill learning — self-improvement loop

When executing a skill needs trial-and-error or discovery of undocumented values, encode what you learned
into the SKILL.md at the end of the session. Generic discovery → shared skill; project-specific → overlay. A
skill not updated after resolving ambiguity is debt that compounds.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Bloated rationale prose | cut to the conclusion; link background docs |
| Missing preconditions | add an explicit precondition check at the top |
| Trigger too broad / too narrow | add domain terms / add a synonym list |
| Hardcoded paths | relative paths or env vars |
| Deeply nested references | keep all references one level from SKILL.md |
| No tool declaration | add `## Required tools` |
| Offering too many options | pick one default; mention alternatives as escape hatches |
| Time-sensitive phrasing ("before August 2025…") | use Legacy / Current sections |

## Sources

- [Equipping Agents for the Real World with Agent Skills — Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Agent Skills Overview — Anthropic Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Effective Context Engineering for AI Agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
