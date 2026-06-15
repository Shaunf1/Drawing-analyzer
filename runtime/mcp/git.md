# Git — Check / Init / Verify

Version control for the framework. Git is driven through the `Bash` tool (or a git MCP if the
project adds one); this module defines the readiness sequence and the working discipline.

## 1. Check

Run `git rev-parse --is-inside-work-tree`. If it errors, the working directory is not a git repo —
STOP and report, or offer to `git init` if the user wants a new repo here.

## 2. Init

Read and record:

- **Repo root** — `git rev-parse --show-toplevel`
- **Current branch** — `git rev-parse --abbrev-ref HEAD`
- **Remote** — `git remote get-url origin` (may be absent for a local-only repo)

If the working tree is detached or on the default branch (`main` / `master`) and the task will make
changes, plan to branch before the first edit (see Branch discipline).

## 3. Verify — identity lock

Confirm the repo root contains the session's working directory and the branch is the one expected for
this task. Record `repo / branch / remote` as the session's **locked identity**. Treat any later git
result whose repo or remote contradicts the lock as a cross-wiring failure — re-run this step rather
than proceeding (matters when several clones are open at once).

## Warm-start verify

When the parent's MCP State lists `git: ready`, run `git status --short` as a connectivity check and
reuse the exported `repo / branch / remote`. If it fails, fall back to full Check → Init → Verify.

## Exported values

| Value | Source |
|-------|--------|
| Repo root | `git rev-parse --show-toplevel` |
| Branch | `git rev-parse --abbrev-ref HEAD` |
| Remote URL | `git remote get-url origin` |

## Branch discipline

**Never commit task work directly to the default branch unless the user asks.** Before the first edit
of a task, create a task-scoped branch:

```
git switch -c <type>/<short-description>   # feat/dwg-layer-parser, fix/pdf-table-offset
```

One task = one branch = one focused set of commits. Mid-task scope change → a separate branch, not a
bundled one.

## Commit discipline

- Stage deliberately (`git add <paths>`), not `git add -A`, so unrelated changes don't ride along.
- Commit messages: short imperative subject describing the **why**, optional body for detail. No
  AI-slop (see [CODING_STANDARDS.md → Comments](../../CODING_STANDARDS.md#comments)). Do not reference
  the change process, plan-stage tags, or "previous behaviour" in the subject — describe the new state.
- Commit and push only when the user asks. Pushing is an outward-facing action — confirm first unless
  durably authorized.

## Required setup (one-time, optional)

For hard enforcement of the "branch before committing to default" and "no secrets committed" rules,
the project can add a `pre-commit` hook or a Claude Code `PreToolUse` hook in `.claude/settings.json`
that denies `git commit` on the default branch. The portable fallback is the discipline above; the
hook is belt-and-braces. See [library/standards/agent-framework.md](../../library/standards/agent-framework.md)
for the hook pattern.
