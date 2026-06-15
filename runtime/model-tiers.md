# Model Tier Mapping

Abstract tiers decouple role/skill model requirements from concrete model names. Each environment
maps tiers to the models it has.

## Tiers

| Tier | Capability | Use for |
|------|-----------|---------|
| high | Best reasoning, architecture, precision | Complex analysis, critical decisions, deep investigation |
| standard | Good general capability | Procedural work, established patterns, mechanical workflows |
| light | Fast, low-cost | Single-step transformations, narrow extraction, immediately checkable results |

## Quality

| Quality | Behavior |
|---------|----------|
| normal | Default — full reasoning |
| fast | Reduced deliberation for speed |

## Environment: Claude Code

| Tier | Model | | Quality | Mode |
|------|-------|-|---------|------|
| high | opus | | normal | default |
| standard | sonnet | | fast | /fast |
| light | haiku | | | |

## Execution

- Any skill or role that declares a `## Model` section **must** run as a sub-agent — no exceptions
  for task size. The main agent cannot switch its own model mid-session; a sub-agent is the only way
  to enforce the declared tier.
- Skills/roles without a `## Model` section run in the main conversation.
- When a skill references another skill, invoke the dependency as a sub-agent — pass its inputs and
  the MCP State block; do not inline its steps.
- Map the tier to a concrete model via the environment table, then pass it as the sub-agent's `model`.
  Quality applies to the main conversation only.

## Light-tier reliability

`light` is unsafe for multi-step tool workflows — it silently skips items in "for each X" loops, acts
on assumptions instead of querying, paraphrases content meant to be copied verbatim, and fabricates
self-reported counts/status. Safe use: single-step transforms (summarize, classify, extract) where the
parent can immediately check the result. When in doubt, use `standard`.

## Adding a new environment

Add a `## Environment: <name>` section with a tier→model table and a quality→mode table (or note that
quality is not configurable).
