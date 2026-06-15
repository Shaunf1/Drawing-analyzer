---
name: commit
description: Use when committing or pushing changes to git — "commit this", "/commit", "push the change", "open a PR". Stages deliberately, writes a clean human-style message, and gates pushing behind explicit user approval.
---

# Skill: Commit

## Trigger

The user asks to commit, push, or open a PR for the current work.

## Model

Tier: standard | Quality: normal

## Required tools

git — see [runtime/mcp/git.md](../../runtime/mcp/git.md). Confirm the locked identity (repo / branch /
remote) before any mutating git command.

## Steps

1. **Confirm branch.** Run `git status --short` and `git branch --show-current`. If on the default branch
   (`main` / `master`) and the user has not asked to commit there, create a task branch first
   (`git switch -c <type>/<desc>`). See [Branch discipline](../../runtime/mcp/git.md#branch-discipline).
2. **Review the diff.** `git diff` (unstaged) and `git diff --staged`. Read it. Confirm every change
   belongs to this task — if unrelated edits crept in, leave them for a separate branch/commit.
3. **Check for secrets.** Scan the diff for credentials, tokens, `.env` content, API keys. If found,
   STOP and tell the user; do not commit.
4. **Stage deliberately.** `git add <specific paths>` — not `git add -A`. Verify with `git status`.
5. **Write the message.** Short imperative subject describing the **why** (not just the what); optional
   body for context. No AI-slop, no plan-stage tags, no "previous behaviour" narration — describe the new
   state. See [CODING_STANDARDS.md → Comments](../../CODING_STANDARDS.md#comments).
6. **Commit.** `git commit` with the message.
7. **Push — only when the user asks.** Pushing is outward-facing; confirm first unless durably authorized.
   `git push -u origin <branch>`. For a PR, use the project's tooling (e.g. `gh pr create`) and write the
   body to the same no-slop standard.

## Message template

```
<imperative subject — why this change exists>

<optional body: context, trade-offs, anything a reviewer needs that the diff doesn't show>
```

## Guardrails

- Never `--force` push or rewrite shared history unless the user explicitly asks and understands the impact.
- Never skip hooks (`--no-verify`) unless the user asks. If a hook fails, fix the cause.
- One task = one focused branch. Don't bundle unrelated work into one commit.
