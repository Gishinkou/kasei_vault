# Agent-authored boards and tasks

Use this reference when creating a board, turning source material into tasks, expanding a branch, or improving task titles.

## Generate the smallest useful tree

1. Establish the intended outcome from the request and nearby project notes. Use a concise noun phrase or question as the board title.
2. Identify the few independent result areas that determine success. Make these top-level milestones; do not add a redundant root task that repeats the board title.
3. Decompose each milestone only until its leaves are immediately executable by the expected worker and have an observable completion signal.
4. Add research branches when the answer is unknown. Use a question or decision as the internal node and evidence-producing actions as leaves.
5. Stop before speculative future work. Let new evidence grow the next layer later.

Typical boards have two to five top-level milestones and two to four useful levels, but clarity overrides those ranges.

## Write titles that drive action

- Internal node: a result, question, or decision that its children collectively resolve.
- Leaf: begin with a concrete verb and name the artifact, evidence, or decision produced.
- Keep one concern per node. Split titles joined by unrelated “and”.
- Include scope in the title when the same action could apply to several systems.
- Avoid vague leaves such as “research”, “handle”, “follow up”, or “optimize” without an object and completion signal.
- Put lengthy context, sources, experiment logs, and conclusions in a task note; keep the board scannable.

Example:

```markdown
---
type: task-tree
title: MySQL 8 升级风险
---

- [ ] 明确 Connector/J 行为差异
	- [ ] 对比 5.1 与 8.0 的连接参数表
	- [ ] 用最小实验记录 ODKU update count
- [ ] 验证服务端语义变化
	- [ ] 用现网 SQL 样本检查 GROUP BY 兼容性
	- [ ] 输出 collation 差异与迁移建议
```

## Status and metadata on generation

- Use `[ ]` unless the source explicitly proves another state.
- Preserve explicit source truth, but do not infer “done” from past-tense wording alone.
- Omit block ids on new tasks. Never make plausible-looking ids.
- Omit dependencies until both task ids exist. Record a suspected ordering relationship in the response or task-note body, then wire it after the plugin assigns ids.
- Match an existing board's indentation and marker. For a new board in this vault, use tabs and `-`.
- Do not add deadlines, priorities, emoji metadata, or unsupported `tt-` fields.

## Create versus propose

When the user asks to create, generate, add, break down, or update tasks, write the board directly. Use a preview only when the user asks for one or when the target file cannot be determined safely. For ambiguity that does not materially alter the project, make the most conservative useful assumption and state it in the handoff.

Before writing a new board, search the intended folder for naming and frontmatter conventions. Do not overwrite an existing note. After writing, run the board validator and tell the user that ids and task-note metadata will appear only after Obsidian with Task Tree enabled processes the board.

