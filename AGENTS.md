# AGENTS.md

This is the framework index — a navigation layer, not an instruction manual. It routes to
the roles, skills, and rules that live in their own files. Keep it lean; detail belongs in
the files it points to.

## Mandatory first step (do not skip)

**Read and execute** [runtime/bootstrap.md](runtime/bootstrap.md) before activating any role,
skill, or task. Do not proceed until bootstrap completes successfully. Failure at any step is
fatal — STOP and report it.

## Roles (activated during bootstrap Step 1)

One primary role per session. Read the role file before acting — identifying a role is not
the same as activating it.

- **Default:** Any task that investigates, debugs, plans, writes, or reviews code requires the
  **developer** role — [roles/developer/AGENTS.md](roles/developer/AGENTS.md).

Add further roles (e.g. `qa`, `reviewer`, `pm`) as the project grows. Mark consultable-only
roles explicitly; see [library/standards/agent-roles.md](library/standards/agent-roles.md).

## Skills

Skills marked **Important** are mandatory when their trigger condition is met — no exceptions
for perceived task size. Non-important skills are advisory.

- **Important** For code reviews — refactoring, quality, correctness on a diff — use the
  **code-review** skill ([skills/code-review/SKILL.md](skills/code-review/SKILL.md)).
- **Important** For committing/pushing changes to git, use the **commit** skill
  ([skills/commit/SKILL.md](skills/commit/SKILL.md)).
- **Important** For exhaustive investigation of a system or feature, use the **deep-dive** skill
  ([skills/deep-dive/SKILL.md](skills/deep-dive/SKILL.md)).
- Before `Write` / `Edit` on any `*.md` file under this agents framework, invoke the **markdown**
  skill (Mode A); after the change, invoke Mode B. Exempt only for typo / whitespace, mechanical
  refactor, or a Mode B follow-up — announce the exemption out loud. See
  [skills/markdown/SKILL.md](skills/markdown/SKILL.md).
- At the end of any dev session, use the **summarise-session** skill to capture work.
- For handing work to another session or person, use the **hand-off** skill
  ([skills/hand-off/SKILL.md](skills/hand-off/SKILL.md)).

## Conventions

- **No AI-slop in generated text.** Code comments, commit messages, PR descriptions, and docs
  must read like a human teammate wrote them. Full rule + examples: [CODING_STANDARDS.md → Comments](CODING_STANDARDS.md#comments).
- **Plans lead with user experience; technical detail goes at the bottom.** A plan's top half is
  readable by a non-developer (what problem, what the user sees, scope, open questions); a
  horizontal rule separates it from the developer-only implementation detail below.
- **Do not write to harness/system memory autonomously.** When you learn something worth keeping,
  encode it in the right agent file (AGENTS.md, SKILL.md, CODING_STANDARDS.md) — version-controlled,
  visible to the whole team — not in a per-machine memory file. If the user says "remember that X",
  diagnose the correct agent file and edit it.
- **No machine-specific absolute paths in agent files.** Use repo-relative paths, markdown relative
  links, or environment variables.
- Every role and skill declares a `## Required MCPs` / `## Required tools` section. Bootstrap uses
  it to decide what to initialize.

## Agent self-improvement

When behaviour deviates from intent (a step skipped, a rule misread): (1) diagnose which agent file
should have prevented it, (2) use the markdown skill Mode A to place the fix, (3) edit that file to
make the rule clearer or harder to skip, (4) commit it in the same session. Encode the lesson in the
file — do not stash it as a one-off note. Keeping the agent setup accurate outranks finishing any
single task.

## Project context

Read [ARCHITECTURE.md](ARCHITECTURE.md) for the project's structure, the `## Variables` table, and
subsystem map. Read [CODING_STANDARDS.md](CODING_STANDARDS.md) for language conventions.

## Structure

```tree
.
├── CLAUDE.md                 ← session entry point (points to AGENTS.md)
├── AGENTS.md                 ← this file (framework index)
├── ARCHITECTURE.md           ← project structure, variables, subsystem map
├── CODING_STANDARDS.md       ← language conventions + comment rules
├── runtime/
│   ├── bootstrap.md          ← mandatory execution gate
│   ├── shared-rules.md       ← session-wide constraints
│   ├── model-tiers.md        ← abstract tier → concrete model mapping
│   └── mcp/
│       └── git.md            ← version control: Check / Init / Verify + workflow
├── roles/
│   └── developer/AGENTS.md   ← default role
├── skills/
│   ├── code-review/          ├── deep-dive/      ├── markdown/
│   ├── commit/               ├── hand-off/       └── summarise-session/
└── library/
    ├── library.md            ← always-loaded knowledge index
    └── standards/            ← agent-framework / agent-roles / agent-skills design docs
```
