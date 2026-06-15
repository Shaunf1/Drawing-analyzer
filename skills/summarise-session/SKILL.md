---
name: summarise-session
description: Use at the end of a dev session to capture what was done — "wrap up", "summarise the session", "/summarise-session". Records the work, decisions, and follow-ups into a durable, version-controlled note rather than per-machine harness memory.
---

# Skill: Summarise Session

## Trigger

End of a working session, or the user asks to wrap up / capture the session.

## Model

Tier: standard | Quality: normal

## Why version-controlled, not memory

Harness/system memory is per-machine and invisible to teammates and other sessions. Anything worth keeping
goes into a committed file so it survives across machines and is reviewable. See the memory hierarchy in
[library/standards/agent-framework.md](../../library/standards/agent-framework.md).

## Steps

1. Gather what changed this session: `git log <base>..HEAD --oneline`, current branch, and any pending diff.
2. Write a session note to `docs/sessions/<date>-<slug>.md`.
3. **Route durable knowledge to its real home, not the session note:**
   - A reusable rule or convention learned → edit the relevant agent file (AGENTS.md, a SKILL.md,
     CODING_STANDARDS.md) and commit it. The session note only references that it was done.
   - A design decision worth keeping → an ADR or doc under `docs/`.
   - Unfinished work for another session → use the **hand-off** skill instead of (or alongside) this one.
4. Commit the session note.

## Template

```markdown
# Session: <date> — <title>

## Goal
<what this session set out to do>

## Done
- <outcome> (<commit sha / files>)

## Decisions
- <decision and one-line rationale>

## Learned → encoded
- <lesson> → <which agent file / doc it was written into>

## Follow-ups
- <next step, or "handoff: docs/handoffs/<file>">
```

## Rules

- No AI-slop (see [CODING_STANDARDS.md → Comments](../../CODING_STANDARDS.md#comments)).
- Do not write the summary to harness memory. The committed note is the record.
- Keep it short — outcomes and decisions, not a transcript.
