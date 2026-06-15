---
name: code-review
description: Use when the user says "code review", "review my changes", "review this PR/branch/commit", or asks for refactoring / quality / correctness review on a diff. Produces a user-editable plan of findings before applying any change; never edits without approval.
---

# Skill: Code Review

## Trigger

The user asks to review a diff — working changes, a branch vs its base, a commit, or a PR.

## First step

Enter plan mode if the harness supports it; otherwise state up front that you will present findings as a
plan and apply nothing until the user approves. Do not edit files before approval.

## Required tools

git (for the diff), the read/search tools, the linter/formatter and test runner (on demand in the
execute phase). If a semantic-analysis MCP exists, use it to find references and callers before proposing
a removal or refactor.

## Required context

Read [CODING_STANDARDS.md](../../CODING_STANDARDS.md) and [ARCHITECTURE.md](../../ARCHITECTURE.md) before
reviewing.

## Scope auto-detection (never ask)

| User says | Diff source |
|-----------|-------------|
| `code review` (no target) | working tree + staged: `git diff HEAD` (fall back to `git diff <base>...HEAD` on a feature branch) |
| `review this branch` | `git diff <base-branch>...HEAD` |
| `review commit <sha>` | `git show <sha>` |
| `review PR <n>` | the PR's diff via the project's git tooling |

Force depth with `quick` / `deep` if the user says so.

## Depth tiers (classify after collecting the file list)

- **QUICK** — ≤3 files AND ≤100 diff lines AND no core-system files. Single pass, inline.
- **STANDARD** — 4–15 files OR 101–500 diff lines OR touches a `## Core Systems` entry (see ARCHITECTURE).
  Adds lint/type diagnostics and complexity check on changed functions.
- **DEEP** — >15 files OR >500 diff lines OR touches a critical subsystem. Adds impact analysis on changed
  symbols and refactoring proposals outside the immediate diff.

## Pipeline

1. **Triage** — detect scope, get the file list, filter out noise (generated files, vendored deps,
   whitespace-only and pure-import-reorder diffs, non-code assets). Classify depth.
2. **Collect** — for each changed file: gather the diff, run the linter/formatter and type checker, run the
   comment-slop sweep and structural checks below. For STANDARD/DEEP, measure complexity of changed functions.
3. **Analyze** — identify findings using the principles below. Severity: errors → critical; lint/type
   warnings → medium; complexity 16+ → high; 11–15 → refactoring proposal.
4. **Present & approve** — write a plan file (template below). Share it, let the user edit, wait for explicit
   approval. Apply nothing before that.
5. **Execute** — apply approved items with the Edit tool (small, auditable patches in plan order). After each
   change, re-run the linter and the relevant tests; fix errors before the next step.
6. **Verify** — run the full linter + test suite on the changed area. Summarize what changed.

## Plan template

```markdown
# Code Review — <scope>

## Summary
<one paragraph: what changed, overall health, headline risks>

## Findings (apply in order)
1. [critical|high|medium|low] <title>
   - File: path/to/file.py:LINE
   - Issue: <what's wrong and why it matters>
   - Fix: <concrete change, as old → new where possible>

## Refactoring proposals (optional, outside the diff)
- <opportunity, payoff, risk>

## Not reviewed
- <generated / vendored / asset files excluded, and why>
```

## Review principles

- Bugs, regressions, security risks, and missing tests come first.
- Enforce [CODING_STANDARDS.md](../../CODING_STANDARDS.md) in every proposal.
- Prefer the simpler form when it produces the same result.
- Look to extract shared logic, remove dead/duplicate code, simplify complex functions, improve naming.
- Verify a member is unused (find references) before proposing its removal.
- Don't avoid a multi-file refactor with clear payoff — break it into safe, reviewable steps.

## Mechanical sweeps (every changed file, full text not just hunks)

- **Comment-slop sweep** — flag em/en dashes, change-narration, plan-stage tags, filler openers, tour-guide
  verbs, hype, and name-restating comments per [CODING_STANDARDS.md → Comments](../../CODING_STANDARDS.md#comments).
- **Empty except / catch** — any empty handler for a type other than cancellation needs an inline reason or removal.
- **Bare `except:` / broad catches**, mutable default arguments, unused imports/variables/parameters.

## Guardrails

- Prioritize behaviour preservation and data integrity.
- If intent is unclear, ask before applying a risky change.
- Avoid speculative rewrites; prefer existing project patterns over new abstractions without need.
