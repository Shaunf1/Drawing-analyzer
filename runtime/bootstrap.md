# Bootstrap — Mandatory Execution Gate

**This file runs at the start of every conversation before any task work begins.**

Do not activate any role, skill, or task until bootstrap completes. Failure at any step is
fatal — STOP immediately and report it. Do not continue under any circumstances.

**Exception — subagent delegation:** if the main agent's only action is to spawn a subagent
(e.g. invoking a skill), it may skip bootstrap and spawn directly. The subagent runs the full
chain itself. A parent that has already bootstrapped must pass an `## MCP State` block to the
subagent (see Warm-start).

---

## Warm-start (subagent with pre-verified tools)

When a parent that already bootstrapped spawns a subagent, it includes an `## MCP State` block
listing initialized tools and their exported values:

```
## MCP State
- git: ready | repo=<path>, branch=<name>, remote=<url>
```

For each tool listed `ready`, run only its **Warm-start verify** step (in its module file). If
that fails, fall back to the full Check → Init → Verify. Run verifications inline — do not spawn
subagents for them. Then continue with Steps 3–4.

---

## Step 1: Activate role and determine required tools

Identify the correct role from the Roles section in [AGENTS.md](../AGENTS.md) and **read its file**.
The role's `## Required MCPs` / `## Required tools` section declares what to initialize.

Identifying a role is not activating it — activation requires reading the role file. This holds in
plan mode too: read the role file and apply its rules during planning.

If no task is specified yet, no tools are required at startup — they initialize on-demand.

## Step 2: Initialize required tools

Run each required tool's **Check → Init → Verify** sequence from its module file under
[runtime/mcp/](mcp/). Independent tools can be initialized in parallel. If any verification fails,
STOP and report.

- [runtime/mcp/git.md](mcp/git.md) — version control. Required when file changes are needed.

Add further tool modules (language server, test runner, an issue-tracker MCP, etc.) as the project
adopts them, each following the same Check → Init → Verify shape.

## Step 3: Load shared rules

Read [runtime/shared-rules.md](shared-rules.md). These constraints apply for the whole session
across all roles and skills.

## Step 3b: Load library index

Read [library/library.md](../library/library.md) so the knowledge base is discoverable. Load full
entries on demand per task. If it doesn't exist yet, skip.

## Step 4: Confirm readiness and lock identity

Verify every required tool passed. State the locked identity in the readiness report — the git repo
+ branch + remote. Any later result that contradicts the lock is a cross-wiring failure: STOP and
re-verify rather than proceeding.

---

## On-demand initialization

Not every task needs every tool at startup. When the task or shared rules indicate a tool is needed,
run its Check → Init → Verify before using it. If a tool that was working becomes unresponsive
mid-session, re-run its sequence before continuing — never silently work around a broken tool.
