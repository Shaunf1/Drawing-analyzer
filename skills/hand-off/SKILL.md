---
name: hand-off
description: Use when work needs to pass to another session, machine, or person — ending with pending/unpushed work, a multi-session investigation worth preserving, or a discovered issue outside the current scope. Produces a self-contained handoff document a fresh session can act on with no prior context.
---

# Skill: Hand-off

## Trigger

The user says "hand off", "/hand-off", "write a handoff", or a session-boundary condition fires:
unpushed/branch work another session must continue; a multi-session investigation has accumulated state;
about to switch machines with unfinished work; a design decision or out-of-scope issue surfaced that the
next session needs.

## Model

Tier: standard | Quality: normal

## Required tools

git — to record the exact branch / commit / dirty-state the handoff is anchored to.

## Output

Write a markdown file to `docs/handoffs/<date>-<slug>.md` (create the folder if absent). The document must
be **self-contained** — a fresh session reads only this file plus the repo and can continue. Use repo-relative
paths and links, never machine-specific absolute paths.

## Template

```markdown
# Handoff: <title>

- **Date:** <YYYY-MM-DD>
- **Branch:** <branch>   **Base:** <base-branch>
- **Last commit:** <sha — subject>
- **Working tree:** clean | dirty (list uncommitted files)
- **Author session goal:** <one line>

## Context
<Why this work exists — the problem, in plain language. Enough that someone with no prior context understands the goal.>

## State — what's done
- <completed item, with the files/commits that delivered it>

## State — what's left
- <remaining item, concrete: file, function, what to change>

## Key decisions & rationale
- <decision made, and why — so the next session doesn't relitigate it>

## Gotchas / open questions
- <traps, unknowns, things to verify before relying on them>

## How to verify
- <commands to run: tests, linter, a manual check that proves the feature works>

## Entry points
- <the files/functions to start reading from>
```

## Rules

- Lead with context and goal (non-developer-readable), then the technical state. Same altitude rule as plans.
- No AI-slop (see [CODING_STANDARDS.md → Comments](../../CODING_STANDARDS.md#comments)). Write like a teammate
  briefing the next shift.
- Commit the handoff doc on the work branch so it travels with the code.
- If the work is genuinely done and verified, say so plainly — a "nothing left" handoff is still useful as a record.
