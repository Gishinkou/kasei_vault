<!-- task-tree:agents:v1:begin -->
<!-- This section is maintained by the Task Tree plugin. Edits inside it will be
     overwritten on plugin updates; write your own instructions OUTSIDE the markers. -->

# Working with Task Tree boards in this vault

Some notes here are **Task Tree boards**: nested Markdown checklists with roll-up
progress, stable block ids, and dependencies. Before editing tasks, know the rules:

1. **The gate:** only treat a note as a board if its frontmatter has `type: task-tree`.
   Notes with `type: task-note` are a task's own page — edit their content freely, but
   their structural frontmatter (`title`, `board`, `parent`, `depth`, `path`,
   `distance_to_main`, `task_id`, `task_status`) is plugin-managed and will be
   reconciled automatically; don't hand-edit it.
2. **Change state on leaves** (flip the char inside `[ ]`); a parent's state derives
   from its children — never mark a parent done directly. `[tt-override:: role]` on a
   line is an explicit human decision: respect it.
3. **Preserve every `tt-` field and trailing `^id`** when rewriting a line; never
   invent or reuse ids (the plugin assigns them). Never write progress counts.
4. **Restructure (move/indent) and state changes are separate edits.** Match the file's
   indentation unit. A task's own note is its **trailing** `[[wikilink]]`.
5. Dependencies: `[tt-blocked-by:: t-id1, t-id2]` — bare block ids on the same board;
   released when the target task is done/cancelled.

The plugin reconciles task-note frontmatter automatically after your edits — you may
restructure boards freely; positions in note YAML self-heal on the next render.

The full machine-readable contract follows.

# Task Tree — machine-readable contract

Compact reference for agents. Prose contract: [/AGENTS.md](../../AGENTS.md). Full spec:
[03_FORMAT_SPEC.md](../03_FORMAT_SPEC.md). Every example in this file is conformance-tested
against the parser (`tests/run.mjs`, section "contract conformance") — if this document and the
code ever disagree, the test suite fails.

## File gate

| Frontmatter | Meaning | May edit? |
|---|---|---|
| `type: task-tree` | A managed board | Yes — per this contract |
| `type: task-note` | A task's own note | Body only; structural frontmatter is plugin-managed |
| anything else | Not Task Tree's | No |

## Task line grammar

```
<indent><marker> [<status>] <text> [tt-override:: <role>]? [tt-blocked-by:: <id>, <id>…]? ^<id>?
```

Parser regexes (from `src/model/line.ts`):

| Piece | Regex |
|---|---|
| List line | `^(\s*)([-*+])(\s+)(.*)$` |
| Checkbox | `^\[(.)\]\s?(.*)$` (on the post-marker body) |
| Override field | `\[tt-override::\s*([A-Za-z]+)\s*\]` |
| Blocked-by field | `\[tt-blocked-by::\s*([^\]]*)\]` (ids match `[A-Za-z0-9-]+`, comma-separated) |
| Block id | `\s+\^([A-Za-z0-9-]+)\s*$` (trailing) |

## Roles and default status characters

| Char | Role | Notes |
|---|---|---|
| `" "` (space) | `todo` | |
| `/` | `doing` | |
| `x` | `done` | `X` is equivalent |
| `-` | `cancelled` | excluded from roll-up |
| `!` | `blocked` | dominates a parent (default; toggleable) |

A board may remap chars↔columns↔roles via `tt_columns` in its frontmatter; **roles** are the stable
layer. An unmapped char defaults to `doing` (setting: `unknownRole`).

## Reserved inline fields

| Field | Value | Placement |
|---|---|---|
| `[tt-override:: <role>]` | one role | after text, before `^id` |
| `[tt-blocked-by:: <id>, <id>]` | bare block ids, same board | after text, before `^id` |

No other `tt-` fields exist. Do not emit Tasks-plugin emoji metadata.

## Roll-up algorithm

```
role(node):
  if override(R) on node:        R
  taskChildren = direct children that are tasks
  if taskChildren empty:         role_of(status char)          # leaf
  active = taskChildren where role != cancelled
  if active empty:               cancelled
  if all active done:            done
  if any active blocked:         blocked                       # blockedDominates default on
  if any active doing|done:      doing
  else:                          todo
```

Progress `K/D` = done active children / active children. **Rendered, never stored.**

## Frontmatter keys (board)

| Key | Meaning | Written by |
|---|---|---|
| `type: task-tree` | opt-in gate | human / plugin convert command |
| `title` | project name; the plugin renames the file to match | plugin (rename) |
| `tt_columns` | per-board column set `{ name, status, role, color?, wipLimit? }` | human |
| `timestamp` | last-touch ISO time | plugin (optional setting, default off) |

## Frontmatter keys (task-note, plugin-managed)

`type: task-note`, `title`, `board` (link), `parent`, `depth`, `distance_to_main`, `path`,
`task_id`, `task_status` — **reconciled automatically every time the board renders**, no
matter who restructured the board (the plugin, an agent, or a hand edit). Hand edits to
these keys will be reconciled away; the note's *content* below the frontmatter is never
touched. `task_status: orphaned` marks a note whose task was deleted from the board; the
marker clears itself if the task comes back (undo). An agent may restructure boards
freely — note positions self-heal.

## Conformance examples

Each line below must parse to exactly the annotated fields (asserted in `tests/run.mjs`):

```markdown
- [ ] Hello world ^t-1
```
→ `status=" "` · `text="Hello world"` · `id="t-1"`

```markdown
	- [x] Ship it [tt-override:: done] ^t-2
```
→ `indent="\t"` · `status="x"` · `override="done"` · `text="Ship it"` · `id="t-2"`

```markdown
- [ ] Announce [tt-blocked-by:: t-qa, t-copy] ^t-3
```
→ `status=" "` · `text="Announce"` · `blockedBy=["t-qa","t-copy"]` · `id="t-3"`

```markdown
- [/] Both [tt-blocked-by:: t-a] [tt-override:: blocked] ^t-4
```
→ `status="/"` · `text="Both"` · `override="blocked"` · `blockedBy=["t-a"]` · `id="t-4"`

<!-- task-tree:agents:end -->

# Portable Task Tree workflow

When a request involves creating, decomposing, installing, diagnosing, or substantially editing
Task Tree content, use the repository skill at `.agents/skills/task-tree/SKILL.md` when the agent
supports Skills. Agents without Skill discovery must still follow the generated contract above.
Run `.agents/skills/task-tree/scripts/validate_board.py` after writing a board. The repository
tracks the Obsidian plugin and activation state, but file presence does not prove that Obsidian has
loaded it; use `.agents/skills/task-tree/scripts/setup_task_tree.py check` to distinguish those
states.
