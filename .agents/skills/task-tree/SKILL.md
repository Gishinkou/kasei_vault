---
name: task-tree
description: "Create, decompose, validate, and safely maintain Obsidian Task Tree boards (`type: task-tree` Markdown), including setup checks, nested task generation, roll-up status, task notes, and same-board dependencies. Use for Task Tree installation or activation, turning a goal or document into an executable task tree, or editing/reporting an existing Task Tree board. Do not use for ordinary Markdown checklists without the Task Tree frontmatter unless the user asks to convert them."
---

# Task Tree

Treat the Markdown files as the source of truth. Obsidian is an optional renderer and reconciler; do not assume its UI, plugin runtime, network access, or a particular home directory exists in the agent environment.

## Start here

1. Locate the vault from the requested file, then the nearest ancestor containing `.obsidian/` or the repository root. Never assume the current directory is the vault.
2. Read the applicable `AGENTS.md`. Its generated Task Tree contract may be newer than this skill and takes precedence.
3. Select only the reference needed for the request:
   - Install, enable, diagnose, or work across different environments: read [references/setup.md](references/setup.md).
   - Create a board, turn a goal into tasks, expand a branch, or improve task wording: read [references/authoring.md](references/authoring.md).
   - Edit, move, complete, cancel, block, validate, or report existing tasks: read [references/contract.md](references/contract.md) completely before writing.

## Operating rules

- A file is a managed board only when its frontmatter contains `type: task-tree`.
- Inspect the board before changing it. Preserve its indentation unit, list marker, custom `tt_columns`, every reserved `tt-` field, trailing task-note link, and trailing `^id`.
- Change completion state on leaves. Parent state and progress are derived; never store calculated progress text.
- Separate a structural change (add, remove, move, indent, rename) from a state change. Make the smallest reviewable edit.
- Never invent, reuse, or repair block ids. New tasks may omit ids; Task Tree assigns them when Obsidian next opens the board. Add a dependency only when both existing ids are known and the edge is acyclic.
- Do not modify Task Tree's managed task-note frontmatter. Edit only the task-note body.
- If the user asks to create or update a board, act directly after resolving safe local conventions. Explain material assumptions afterward instead of requiring a draft approval.
- Before finishing a write, run `python3 <skill-dir>/scripts/validate_board.py <board...>`. Treat errors as blockers; report warnings that are intentional.

## Common outcomes

- **Create:** Write the smallest useful tree whose leaves can be acted on and verified. Leave uncertain status as todo and omit ids.
- **Expand:** Add only the next useful layer beneath the named node; do not redesign unrelated branches.
- **Complete:** Flip the leaf status character only, then explain any ancestor roll-up or released dependency.
- **Report:** Compute roles bottom-up from the board; list active leaves, blockers and dependency holds with their ancestor paths. Do not write the report into the board unless asked.
- **Set up:** Start with the read-only doctor. Mutating setup commands require an explicit installation or enablement request.
