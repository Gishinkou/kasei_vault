# Task Tree machine-readable contract

Read this file completely before modifying an existing board.

## File gate

| Frontmatter | Meaning | Allowed edit |
| --- | --- | --- |
| `type: task-tree` | Managed board | Board edits under this contract |
| `type: task-note` | A task's own note | Body only; structural frontmatter is plugin-managed |
| Anything else | Ordinary note | Do not treat it as a board without an explicit conversion request |

## Task grammar

```text
<indent><marker> [<status>] <text> [tt-override:: <role>]? [tt-blocked-by:: <id>, <id>…]? [[task note]]? ^<id>?
```

The task note, when present, is the trailing wikilink in task text. Preserve it when renaming or moving a task.

| Piece | Recognition rule |
| --- | --- |
| List line | `^(\s*)([-*+])(\s+)(.*)$` |
| Checkbox | `^\[(.)\]\s?(.*)$` on the post-marker body |
| Override | `\[tt-override::\s*([A-Za-z]+)\s*\]` |
| Blocked by | `\[tt-blocked-by::\s*([^\]]*)\]` with comma-separated `[A-Za-z0-9-]+` ids |
| Block id | `\s+\^([A-Za-z0-9-]+)\s*$` |

Reserved fields belong after human-readable text and before the trailing block id. No other `tt-` fields exist.

## Roles and default characters

| Character | Default role | Meaning |
| --- | --- | --- |
| space | `todo` | Not started |
| `/` | `doing` | In progress |
| `x` or `X` | `done` | Complete |
| `-` | `cancelled` | Excluded from roll-up |
| `!` | `blocked` | Dominates a parent by default |

A board may remap characters and roles through `tt_columns`. Use roles as the semantic layer and respect the board mapping. An unmapped character defaults to the configured `unknownRole` (normally `doing`).

## Roll-up

```text
role(node):
  if node has override R:       R
  children = direct task children
  if children is empty:         role_of(node.status)
  active = children excluding cancelled
  if active is empty:           cancelled
  if every active child done:   done
  if any active child blocked:  blocked       # when blockedDominates is enabled
  if any active child doing or done: doing
  otherwise:                    todo
```

Progress is `done active children / all active children`. It is rendered, never stored. Apply the algorithm bottom-up. An override is an explicit human decision and wins over child state; do not remove it merely because it looks redundant unless the user requests cleanup.

## Safe edit operations

- **State change:** change only the leaf's status character.
- **Rename:** change only human-readable text; preserve reserved fields, trailing note link, and id.
- **Move:** move the whole contiguous subtree and preserve its internal indentation. Adjust every moved line by the same depth delta.
- **Add:** match marker and indentation; omit ids.
- **Delete/cancel:** deletion removes a subtree and can orphan notes. Prefer cancellation unless the user clearly asked to delete.
- **Dependency:** append `[tt-blocked-by:: target-id]` before `^id`; targets are bare ids in the same board. Reject unknown ids, self-edges, and cycles.

Do not combine a move with status changes in one edit. Do not manually rewrite calculated parent characters as a substitute for leaf changes.

## Task-note frontmatter

These fields are reconciled by the plugin and must not be hand-edited: `type`, `title`, `board`, `parent`, `depth`, `distance_to_main`, `path`, `task_id`, and `task_status`. Edit the body freely. A deleted task's note may become `orphaned`; the note is not automatically deleted.

## Reporting blockers

Report both categories:

1. Status blockers: leaf role is `blocked`; include its ancestor path.
2. Dependency holds: a task waits on a target whose derived role is neither `done` nor `cancelled`; name both tasks.

Also flag missing target ids and dependency cycles. Dependencies do not change the roll-up formula by themselves.

## Conformance examples

```markdown
- [ ] Hello world ^t-1
	- [x] Ship it [tt-override:: done] ^t-2
- [ ] Announce [tt-blocked-by:: t-qa, t-copy] ^t-3
- [/] Both [tt-blocked-by:: t-a] [tt-override:: blocked] ^t-4
```

