---
name: Agent Role Design Standards
last_updated: 2026-06-15
staleness_threshold_days: 30
tags: [agent, roles, claude-code, role-design, bootstrap]
---

# Agent Role Design Standards

Reference for designing, writing, or reviewing role `AGENTS.md` files. Load before creating a new role,
extending one, or diagnosing inconsistent role activation.

## Role anatomy

A role is a directory under `roles/`; the primary file is `AGENTS.md`. Version/platform overlays, if needed,
are sibling markdown files loaded conditionally.

**Mandatory sections:**

1. **Purpose** — one paragraph: what the role is responsible for and what it is *not*. The boundary is explicit.
2. **Required tools** — every tool the role may need; bootstrap initializes these before activation.
3. **Activation conditions** — when bootstrap selects this role (triggers, task types, default fallback).
4. **Conventions** — role-specific constraints that extend or override the shared coding standards.
5. **Branching instructions** — how to load version/platform overlays, if any.

## Role activation

Bootstrap Step 1 selects **exactly one primary role** per session. A session that activates two roles has
competing constraints. If a task spans domains, activate the primary and *consult* the secondary as read-only.

**Default role:** every framework needs one that handles any task not covered by a more specific role —
without it, undefined tasks fall through to raw model behaviour with no project context.

## Consulting vs activating

- **Activated** — owns the session, applies all its constraints to every action.
- **Consulted** — read by the active role for specialist perspective; advisory, not session-wide.

Document the mode in the role file:

```markdown
## Activation mode
This role is a **consultable specialist**, not directly activated by the user. Other roles read it to
apply its standards to their own output.
```

## Branching (version / platform)

When behaviour must differ across versions or deployment targets, use overlay files (`roles/developer/
<variant>.md`) loaded from a variable set in shared-rules or the project AGENTS.md. The base file holds the
variant-agnostic content; overlays hold only the additive/overriding parts — they never repeat the base. Use
branching sparingly, only where the surface genuinely diverges.

## Role vs skill boundary

| | Role AGENTS.md | Skill SKILL.md |
|---|---|---|
| Defines | identity, standing constraints, tool list, conventions | one invocable procedure |
| Loaded | once per session at bootstrap | on demand when triggered |
| Scope | everything the agent does this session | one repeatable workflow |
| Mutation | rarely (standing constraints) | often (as the skill learns) |

A role with a detailed step-by-step workflow should extract it into a skill. A skill that re-declares
identity or session-wide constraints is over-scoped. Example: the role declares "all code passes the
linter"; the `code-review` skill declares the review procedure.

## Scope discipline — shared vs project overlay

Shared roles must not contain project-specific paths, IDs, naming conventions, domain terminology, or
hardcoded version assumptions. Project overlays add concrete coding standards, architecture context,
configuration, and version/platform defaults. **An overlay exists only when there is genuinely
project-specific content** — an empty stub that re-declares the base is a scope violation; delete it and rely
on the base.

## Warm-start for sub-agent roles

A role activated inside a sub-agent can't assume the parent's tool/context state. It: (1) reads the
`## MCP State` block from the handoff prompt, (2) verifies each tool with a lightweight ping rather than full
init, (3) inherits a 1–2k-token context summary instead of re-reading every file.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Role covering too many domains | split into focused roles; use the consulting pattern |
| Missing Required tools | audit every tool call in the role and list them all |
| No activation conditions | write explicit triggers + a default fallback |
| Step-by-step procedures in a role | extract to a skill |
| Overlay duplicating shared content | overlay adds/overrides only, never copies |
| Hardcoded paths in a shared role | use relative paths; concrete values in the overlay |

## Sources

- [Effective Context Engineering for AI Agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
- [AGENTS.md Specification](https://agents.md/)
