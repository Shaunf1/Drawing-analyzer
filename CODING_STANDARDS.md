# Coding Standards

Language: **Python** (primary). If a module is written in another language, apply the equivalent of
each rule and keep the Comments section verbatim — it is language-agnostic.

## Philosophy

Clean code is elegant, efficient, and readable. A teammate should understand it without the author
explaining it.

- **KISS** — proven, simple techniques. No fancy tech for its own sake.
- **Root cause, not workaround** — investigate why a problem exists before adding a guard or retry.
- **Good, not perfect** — refactor when code becomes unmanageable, not preemptively.
- **DRY** — duplicate logic is duplicate bugs.
- **Single responsibility** — each module, class, or function does one thing.

## Project layout

- Package code under `src/<package_name>/`; tests under `tests/` mirroring the package tree.
- Group modules by domain/subsystem, not by type. Keep `__init__.py` exports intentional.
- Configuration and constants live in a dedicated module, not scattered as literals.

## Naming

Use meaningful names that reveal intent; easy to pronounce and search. Don't abbreviate (except math).

| Kind | Convention | Example |
|------|-----------|---------|
| Module / package | `lower_snake_case` | `dwg_parser` |
| Class / type | `UpperCamelCase` | `SlabProfile` |
| Function / method | `lower_snake_case`, verb-first | `extract_slab_depths` |
| Variable | `lower_snake_case`, noun | `reduced_level` |
| Constant | `UPPER_SNAKE_CASE` | `DEFAULT_DPI` |
| Boolean | question form | `is_structural`, `has_annotations` |
| Private | leading underscore | `_normalize_layer` |

- Use nouns for variables, verbs for functions. No single-letter names for domain objects (loop
  counters `i`/`j`, caught exceptions `e`/`exc`, and math operands are fine).
- Avoid redundancy: on a class `Drawing`, use `scale` not `drawing_scale`.
- No jokes or puns in names.

## Python conventions

- **Style:** follow PEP 8; enforce with `ruff` (or `flake8` + `black`). 4-space indent, no tabs.
- **Type hints:** annotate all public function signatures, return types, and dataclass fields. Run a
  type checker (`mypy` / `pyright`) in CI.
- **Data objects:** prefer `@dataclass` (or `pydantic` models at I/O boundaries) over loose dicts for
  structured data.
- **Imports:** absolute imports within the package; group stdlib / third-party / local; let `ruff`/`isort`
  order them. Remove unused imports.
- **f-strings** for formatting; never `%` or `.format()` for new code.
- **Paths:** use `pathlib.Path`, not string concatenation or `os.path`.
- **Comprehensions** for simple transforms; a plain loop when the comprehension would be hard to read.
- **Exceptions:** catch the narrowest type. Never a bare `except:`. An empty `except SomeError:` needs an
  inline comment naming the scenario, or it should not exist.
- **Context managers** (`with`) for any resource that must close (files, PDF/DXF document handles).
- **Avoid mutable default arguments** (`def f(x=[])`); use `None` and create inside.

## Structure & formatting

- **Early returns** over nested `if`/`else`. If exit points pile up, split the function.
- **Small functions.** Don't extract a few lines into a single-use helper that adds no clarity; do
  extract when logic is reused or the name genuinely aids reading.
- **Complex conditions → named booleans.** `is_within_tolerance = abs(a - b) < EPSILON`.
- **One statement per line.** Keep lines short enough not to scroll horizontally.
- Blank line after each function and class; group related logic.

## Member / definition order (within a module or class)

1. Module docstring, then imports.
2. Constants.
3. Public classes/functions, then the private helpers they use, grouped by related logic.
4. Within a class: class-level fields → `__init__` → public methods → private methods.

When you add a definition, place it by this order before saving. If the file you're editing already
violates it in the lines you touched, fix it in the same change.

## Documentation

- Every module, public class, and public function has a docstring covering its responsibility, key
  parameters/returns, and any non-obvious behaviour or constraint.
- Do not add a docstring that merely restates the name and signature. Document the non-obvious: side
  effects, units (e.g. "depths in millimetres"), coordinate conventions, failure modes.
- Don't add comments to compensate for unclear code — restructure instead.
- Remove commented-out code; rely on version control.
- Do not leave a "removed in commit X" tombstone comment. The deletion is in git history.

## Comments

Comments must read as if they were always part of the file, written for someone seeing the code for
the first time. The change that produced them is irrelevant. Version control records the change;
comments record the intent. **A comment is not a release note.**

### Always

- Explain **why** when the why is non-obvious: a hidden constraint, an invariant, a workaround for a
  specific bug, behaviour that would surprise a reader.
- State the constraint, surprise, or gotcha and stop.
- Stay timeless. The comment must still read correctly years from now without anyone remembering the
  change that introduced it.

### Never

- **Reference the current change, plan slug, ticket number, removed code, or "previous behaviour".**
  This is the most common AI-comment failure mode. `# Replaces the old polling loop`,
  `# with the wrapper deleted in P1.4`, `# Without this, ...` — all narrate the diff. Delete or rewrite
  as a current-state explanation.
- **Cite plan-stage references in source.** Patterns like `(P1.4)`, `P2.7` are change-narration with a
  fancy syntax; treat them like a commit hash. The plan tracks iterations; the code does not.
- **Re-litigate performance trade-offs at every call site.** If a project standard mandates a pattern,
  the rationale lives in this file, not above every use.
- **Narrate what the syntax already shows.** A function named `load_and_validate_drawing` returning a
  `Drawing` does not need `# Loads and validates the drawing, returns a Drawing`.
- **Use em dashes (—) or en dashes (–).** ASCII only — hyphen, comma, period, or parentheses. Same in
  docstrings.
- **Use filler openers** ("It's worth noting", "Note that", "Keep in mind", "In essence", "Basically",
  "Simply put", "In summary"). `# NOTE:` prefixes are slop too — drop the prefix or delete the comment.
- **Use tour-guide verbs** ("delve", "dive into", "explore", "navigate", "journey", "unpack").
- **Use hedging hype** ("robust", "seamless", "elegant", "powerful", "comprehensive", "leverage",
  "utilize", "facilitate", "streamline").
- **Restate the identifier name in prose** (`# Returns the slab depth.` on `def get_slab_depth()`).

### Self-check before saving (every code change)

Read every comment and docstring you added or edited. For each:

1. Does it describe the **change** rather than the code's **current state**? Rewrite or delete.
2. Does it contain `—` or `–`? Replace with ASCII.
3. Does it contain a filler opener, tour-guide verb, or hype word from the lists above? Strip them.
4. Would a teammate seeing the file fresh in three years find it puzzling, condescending, or stale? Fix it.
5. Could it be deleted with no information loss because the name + types + structure already explain it? Delete it.

**Apply retroactively:** when you touch a file, fix any AI-slop comment in the lines you read or edit.

### Examples

Bad (change-narration):

```python
# Replaces a manual page loop that re-opened the PDF for every page.
# Now uses fitz.open once, as decided this sprint.
doc = fitz.open(path)
```

Good (timeless why):

```python
# fitz keeps the file mapped until close(); open once and page through, or large
# DWG-exported PDFs exhaust file handles.
doc = fitz.open(path)
```

Bad (restates the syntax):

```python
# Extract slab depths from the drawing and return them as a list.
def extract_slab_depths(drawing: Drawing) -> list[float]:
```

Good (delete it; the name and signature already say this):

```python
def extract_slab_depths(drawing: Drawing) -> list[float]:
```

## Code quality

- Remove all unused code: variables, parameters, imports.
- Avoid duplication; search for an existing solution before writing a new one.
- Prefer refactoring the original over copy-modify.

## Performance

- Profile before optimizing; don't guess hot paths.
- Avoid repeated heap allocation in tight loops; reuse buffers where it measurably helps.
- For large PDF/DXF documents, stream/page rather than loading everything into memory at once.
- Use vectorized NumPy operations over Python-level loops for geometry math where it's clearer and faster.

## Tooling

- Pin tool versions in `pyproject.toml`. Run `ruff`, the type checker, and `pytest` in CI and before commit.
