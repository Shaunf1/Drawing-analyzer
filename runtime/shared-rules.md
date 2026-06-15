# Shared Rules

Loaded by [bootstrap.md](bootstrap.md) after tool initialization. These apply to **all roles and
skills** for the entire session.

## File operations

- All file changes go through git: work on a branch, never commit directly to the default branch
  unless the user asks. Initialize git via [runtime/mcp/git.md](mcp/git.md) if it isn't ready.
- Before editing a file, read it. Match the surrounding code's style, naming, and comment density.
- Do not modify files until required tools are confirmed ready.

## Variables

- The project's [ARCHITECTURE.md](../ARCHITECTURE.md) holds a `## Variables` table of `UPPER_SNAKE_CASE`
  key/value pairs. Read a needed value from there first — don't hardcode or guess.
- If a required variable is missing, ask the user and add it to the table so it persists.

## Safety

- Never read `.env` files or files holding secrets/credentials.
- Do not assume project structure or invent file paths — verify with the file tools.
- For actions that are hard to reverse or reach outside the repo (pushing, publishing, deleting),
  confirm first unless the user has clearly authorized it.

## Standards

- Always follow [CODING_STANDARDS.md](../CODING_STANDARDS.md).

## Plans

- A plan describes **what** to change and why, not the full implementation. Use pseudocode for
  non-obvious logic; leave final code to the developer role and coding standards.
- Read the coding standards before writing a plan so naming and structure in the plan match
  project conventions.

## Agent markdown changes

The **markdown** skill ([skills/markdown/SKILL.md](../skills/markdown/SKILL.md)) governs every change
to a framework `.md` file. Mode A (before writing — placement analysis) and Mode B (after — review for
duplication, staleness, scope, altitude) are both mandatory; neither can be skipped for perceived
simplicity. Exempt only for typo / whitespace, mechanical refactor, or a Mode B follow-up, and announce
the exemption out loud.

## Library knowledge

Before claiming any version-specific behaviour (library API, runtime, language feature, file format),
read the relevant entry in [library/library.md](../library/library.md) and verify against your claim.
If the entry is missing or stale (`today − last_updated > staleness_threshold_days`), research online
and update it before producing output — notify the user, don't ask permission.

## Model tiers

Any skill or role that declares a `## Model` section must run as a sub-agent. See
[model-tiers.md](model-tiers.md).

## Critical thinking

- Do not default to agreement. Evaluate proposals independently.
- Identify weaknesses, risks, and assumptions. Offer at least one alternative when relevant.
- Prioritize correctness over matching the user's stated preference.
