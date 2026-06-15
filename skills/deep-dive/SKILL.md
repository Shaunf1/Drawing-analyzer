---
name: deep-dive
description: Use when the user says "deep dive", "/deep-dive", "fully understand <system>", or asks for an exhaustive investigation of a system, feature, or subsystem. Reads every related file in full and follows every trail to build a complete mental model before writing it up. Read-only — modifies nothing.
---

# Skill: Deep Dive

## Model

Tier: standard | Quality: normal

## Purpose

Exhaustively investigate a codebase area — read every related file in full, follow every trail
(references, callers, config, data, tests), and produce a structured summary that gives the user and
future sessions a complete mental model. **Read-only**: creates, modifies, deletes nothing.

## Required tools

git (to scope the repo) and the read/search tools. If the project has a semantic-analysis MCP
(language server), use it for symbol resolution, call graphs, and reference finding in preference to
text search.

## Confirmation gate (mandatory)

Before investigating, present:

1. **Scope** — what you understand the target to be.
2. **Starting points** — the files/modules you'll begin from.
3. **Trails to follow** — related modules, callers, config, data, tests.
4. **Estimated breadth** — rough number of files.

Wait for explicit confirmation. If the user re-scopes, adjust and re-confirm.

## Process

### Step 1 — Discover (main agent)

- Find all related files by name pattern, symbol name, and references. Use semantic search first if
  available; fall back to glob/grep.
- Build a complete file list, then measure each file's line count.
- Build a line-count inventory before partitioning.

### Step 2 — Parallel investigation (sub-agents)

Partition by **line budget**, not file count: ~3000 lines of source per sub-agent. A single 2500-line
file warrants its own agent; ten 150-line files can share one.

```
agents = max(1, ceil(total_lines / 3000))   # clamp to 4
```

If the total exceeds 12000 lines, ask whether to continue at this breadth or narrow. Launch all chosen
sub-agents in a single message so they run concurrently.

Each sub-agent prompt **must** include: its assigned file list with line counts; the reading protocol
below verbatim; instructions to note (not follow) trails that cross into another agent's partition or
leave the system boundary (stdlib, third-party packages); and the output sections it owns.

**Reading protocol (paste verbatim into every sub-agent prompt):**

```
Read every assigned file with the Read tool, sequentially, line 1 to end.
- Files up to 2000 lines: one Read call.
- Files over 2000 lines: sequential 2000-line chunks until the end. Do not skip chunks.
- Do not use grep/search as a substitute for reading. Search is for discovery; Read is for investigation.
- Do not skim, summarize from names, or skip "boilerplate".
End your report with a verification table: | File | Lines read | Method |. Do not fabricate ranges.
```

### Step 3 — Combine (main agent)

Verify each sub-agent's "files read" table; read any unread file directly. Merge findings, resolve
overlaps (prefer the agent that read the primary source), and follow up any cross-partition trail that
was noted but not covered.

## Output format

- **Architecture overview** — module/class relationships, key data structures, file locations.
- **Lifecycle** — initialization/bootstrap chain, main processing flow, teardown.
- **Subsystems** — per major subsystem: what it does, key functions, config parameters, known issues/TODOs.
- **Data flow** — input sources/formats, output targets/formats, tuning parameters.
- **Integration points** — what calls in, what it calls out to, events/interfaces.

Tailor depth to complexity. Prefer concrete details (function names, line numbers, parameter values) over
vague description.

### Development suggestions

After the summary, propose **exactly two** next actions grounded in the investigation (TODOs/FIXMEs,
fragile patterns, gaps). For each: **What**, **Why** (tied to a specific finding), **Where to start** (key files).

## Guardrails

- Read-only. Modify nothing.
- Don't skip files that look unimportant — read first, judge after.
- At 30+ files or 12000+ lines, give a progress update and ask whether to continue or narrow.
