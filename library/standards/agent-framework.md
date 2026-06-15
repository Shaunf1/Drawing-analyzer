---
name: Agent Framework Design Standards
last_updated: 2026-06-15
staleness_threshold_days: 30
tags: [agent, framework, claude-code, agents-md, bootstrap, context-engineering, memory]
---

# Agent Framework Design Standards

Reference for designing or reviewing the top-level agent framework: `CLAUDE.md`, `AGENTS.md`, bootstrap,
shared-rules, context budget, memory hierarchy, multi-agent coordination. Load when setting up a new
project's framework, auditing why agents skip steps, or planning multi-agent work.

## CLAUDE.md — the minimal entry point

Loaded automatically every session, so its contents must be **universally applicable** — no task-specific
or conditional content. **Target: under 300 lines** (production root files are often under 60).

Adherence drops sharply with instruction count. The *Curse of Instructions* benchmark shows success at
following *all* instructions falling to ~15% at 10 simultaneous constraints; *When Models Can't Follow*
(256 models) confirms it. Implication: each Critical/Mandatory label costs adherence somewhere else. Spend
the budget deliberately.

CLAUDE.md's purpose is narrow: (1) point to AGENTS.md with a mandatory "read before any work" instruction;
(2) state the single most critical override, if any; (3) nothing else. Test every line: "Would removing
this cause a mistake on almost every task?" If no, move it to a skill or role.

## AGENTS.md — the framework index

A navigation layer, not an instruction manual. Sections in order: bootstrap gate → roles index → skills
index (mark `Important` deliberately; every Important skill must fire reliably) → conventions (the hardest
constraints) → self-improvement process → project overlays → structure tree. Detail lives in role and skill
files; AGENTS.md holds the routing.

## Bootstrap gate pattern

The mandatory sequence before any work:

```
Step 1 — Role: read the roles index; activate the correct role.
Step 2 — Tools: for each tool the role requires, run Check → Init → Verify.
Step 3 — Shared rules: load shared-rules.md.
Step 3b — Library index: load library.md.
Step 4 — Confirm readiness; lock identity (repo/branch/remote). STOP on any failure.
```

**Check → Init → Verify** per tool: Check is a fast non-destructive ping; Init runs only if Check fails;
Verify is a task-representative call confirming the tool can do what the role needs. **STOP on failure** —
an agent proceeding with a failed tool produces broken output silently. **Warm-start:** sub-agents get an
`## MCP State` block and run only Verify.

## Context budget management

Context is the fundamental constraint; every framework decision is a context decision. The guiding
principle (Anthropic, *Effective Context Engineering*): the smallest set of high-signal tokens that
maximizes the desired outcome. Accuracy degrades as tokens grow ("context rot").

| Content | Loading | Why |
|---|---|---|
| CLAUDE.md | always (auto) | session-universal; keep short |
| AGENTS.md, shared-rules | once at bootstrap | routing + session constraints |
| Library index | always | enables on-demand lookup |
| Role file + overlays | once at bootstrap | role constraints for the session |
| Skill SKILL.md | on demand when triggered | loaded only when the skill fires |
| Sibling/reference files, specs | on demand | never pre-loaded |

Avoid front-loading "just in case" — it crowds out the actual task. Use the index to know what exists; load
when needed.

## Two failure modes of agent instructions

1. **Overly complex (brittle)** — so detailed it breaks on variation; deep-buried rules get ignored. Signs:
   CLAUDE.md over 300 lines, step-by-step procedures in a role, SKILL.md over 500 lines.
2. **Overly vague** — no actionable specifics; Claude can't tell which tool/flag/file. Signs: triggers with
   no domain terms, "follow best practices" with no definition.

Resolution: right-altitude writing. Encode the non-obvious; trust Claude with the obvious.

## Memory hierarchy

| Level | Mechanism | Visibility | Use for |
|---|---|---|---|
| 1 (durable, preferred) | committed agent files (AGENTS.md, SKILL.md, roles) | whole team, all machines | rules, conventions, skill iterations |
| 2 (durable) | committed docs (ADRs, specs, knowledge notes under `docs/`) | whole team | decisions, plans, cross-machine context |
| 3 (ephemeral cache) | harness/system memory | current machine only | session narrative for picking up tomorrow |

Harness memory is per-machine and invisible to teammates. Anything that must be shared ends up at level 1
or 2. When you learn something, ask: "Does another machine need this?" If yes → level 1/2.

## Multi-agent coordination

Spawn sub-agents when a task needs many file reads (keeps the main context clean), parallelizes
independently, needs a specific model tier, or benefits from an unbiased fresh context. Not for simple tool
calls or short lookups.

When spawning, pass: (1) an `## MCP State` block, (2) a 1–2k-token task context summary (not a transcript),
(3) the expected output format. Sub-agents return condensed summaries, not raw logs. **Default to sequential**
unless parallelism is clearly safe — parallel agents writing the same files or branch will conflict. The
orchestrator must verify results before acting (a commit sha, a test result, a reviewable diff — not "done").

## Self-improvement — encode lessons into agent files

When behaviour deviates: (1) diagnose which file should have prevented it, (2) use the markdown skill Mode A
to place the fix, (3) make the rule clearer / add an example / move it higher, (4) commit. Don't stash it as
a one-off memory note. Each encoded lesson lowers the chance of recurrence; unencoded lessons are silent debt.

## Strengthening rules: compress, don't promote

When a rule is silently skipped, the instinct is `**CRITICAL**` / `**MANDATORY**` prose. That *lowers*
adherence on the same rule:

- Each tier label is another instruction in the budget; the model drops something to make room.
- Tier labels are model-side and unreliable — read at the same attention as surrounding prose, gating nothing.
- Autoloaders match **structure** (path globs, tool names, `description:` first phrase) far more reliably than
  **intensity** (uppercase labels).

Three recovery moves, in order: (1) move the trigger to the first phrase of `description:` / the first
heading; (2) cut competing prose — one imperative sentence beats a nine-line block; (3) add concrete
tool+path patterns the autoloader can match.

**When hooks are the right answer:** a `PreToolUse` hook (Claude Code `.claude/settings.json`) or a git
`pre-commit` hook is the most reliable layer — it fires before permission checks and can't be talked around.
Because hooks are harness-specific and live in user config (not source control by default), any shared rule
that depends on a hook **must flag the one-time setup** to the user under a `## Required setup (one-time)`
section. Keep the portable LLM-side pattern too, as the cross-harness fallback.

## Sources

- [Effective Context Engineering for AI Agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)
- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Writing a Good CLAUDE.md — HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [AGENTS.md Specification](https://agents.md/)
- [Curse of Instructions — OpenReview](https://openreview.net/forum?id=R6q67CDBCH)
- [When Models Can't Follow (256 LLMs) — arXiv 2510.18892](https://www.arxiv.org/pdf/2510.18892)
- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
