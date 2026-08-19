# Task Tree 中文快速使用指南

> 适用于 Obsidian 插件 **Task Tree 1.0**。本文按 2026-08-19 的官方 README、格式规范与路线图整理。

## 0. 本仓库的最短路径

这个 Vault 已把 Task Tree 插件文件、启用配置、Agent Skill 和格式契约一起纳入 Git。
完整 checkout 后，先在仓库任意子目录运行：

```bash
python3 .agents/skills/task-tree/scripts/setup_task_tree.py check
```

若结果显示 `ready on disk`，只需打开或重启 Obsidian；不必重复安装。Codex 会从
`.agents/skills/task-tree/` 自动发现 Skill，可以直接说：

```text
$task-tree 把“评估 MySQL 8 升级风险”生成一棵可执行的任务树
```

没有 Obsidian 的 AI 环境也可以创建、编辑和校验 Markdown Board，只是不能运行可视化、
自动分配 ID 或同步 task-note frontmatter。跨环境说明见
[`setup.md`](../.agents/skills/task-tree/references/setup.md)。

## 1. 它是什么

Task Tree 把普通 Markdown 任务显示为一棵可折叠、可拖动的任务树，并同时提供看板和项目仪表盘。

它特别适合这类工作：

- 一个目标会不断拆出问题、子问题和行动项；
- 可以从任意分支开始深入处理；
- 子任务完成后，父任务的状态和进度自动更新；
- 每个任务可能需要单独记录资料、代码、实验和结论；
- 某些任务必须等另一条分支完成后才能开始。

底层数据仍是普通 Markdown。即使以后不用插件，任务内容也能直接阅读。

---

## 2. 安装

> 本仓库通常不需要手工安装。以下步骤用于新 Vault；当前 Vault 请先执行第 0 节的检查。

### 方法 A：从 Obsidian 社区插件安装

1. 打开 Obsidian。
2. 进入 **设置 → 第三方插件/社区插件**。
3. 关闭安全模式（如果尚未关闭）。
4. 搜索 **Task Tree**。
5. 安装并启用。

若社区插件中暂时搜索不到，使用下面的 BRAT 方法。

### 方法 B：通过 BRAT 安装

1. 在社区插件中安装并启用 **BRAT**。
2. 打开命令面板。
3. 执行 **BRAT: Add a beta plugin**。
4. 输入仓库地址：

   ```text
   Aldorithm392/obsidian-task-tree
   ```

5. 安装完成后，在社区插件列表中启用 **Task Tree**。

### 方法 C：让 Agent 安装固定版本

只有在插件文件缺失、并且你明确要求 Agent 安装时使用：

```bash
python3 .agents/skills/task-tree/scripts/setup_task_tree.py install --version 1.0.0
```

脚本会从 Task Tree 官方 GitHub Release 下载三个插件文件并启用插件；它不会覆盖
`data.json`，也不会静默替换不同版本。完成后仍需重启 Obsidian 或重新加载社区插件。

---

## 3. 创建第一棵任务树

### 最简单的方法

打开命令面板，执行：

```text
Task Tree: Create a new board
```

一个 Board 对应一个项目，也对应一个 Markdown 文件。

### 把现有笔记转成任务树

1. 打开包含 Markdown checklist 的笔记。
2. 执行：

   ```text
   Task Tree: Convert current file to a Task Tree board
   ```

插件会在文件顶部加入：

```yaml
---
type: task-tree
---
```

Task Tree 只管理带有 `type: task-tree` 的文件，不会改动其他普通笔记。

### 最小示例

```markdown
---
type: task-tree
title: 弄清楚 MySQL 8 升级风险
description: 调查升级可能产生的行为变化
tags: [research, mysql]
---

- [ ] 弄清楚 MySQL 8 升级风险
	- [ ] Connector/J 行为变化
		- [x] ODKU update count
		- [ ] 批处理行为
	- [/] Server 语义变化
		- [x] GROUP BY
		- [ ] collation
```

推荐用一个 Tab 表示一层缩进。也可以直接在可视化界面中创建和移动节点，不必手写 Markdown。

---

## 4. 打开不同视图

在当前 Board 上可以运行以下命令：

| 命令 | 用途 |
| --- | --- |
| `Open current file as tree` | 打开任务树 |
| `Open current file as Kanban board` | 按状态查看看板 |
| `Open current file as dashboard` | 查看整体进度、阻塞项和下一步 |

任务树本身提供三种布局：

| 布局 | 适合场景 |
| --- | --- |
| **List** | 垂直层级列表，快速编辑大量任务 |
| **Diagram** | 横向树状图，观察整个问题结构 |
| **Columns** | 类似 Finder 的分栏，逐层浏览问题 |

Diagram 和 Columns 可以反转方向，让底层行动项流向最终目标。

点击节点的 **Focus** 按钮，可以只显示该节点及其子树；顶部面包屑可以返回上层。

---

## 5. 新增、编辑和移动节点

### 新增

- 点击顶部 **Add task** 添加根任务；
- 将鼠标移到某节点上，点击 `+` 添加子任务；
- 也可以通过右键菜单添加根节点、同级节点或子节点；
- 新增后直接输入，按 Enter 保存并继续添加下一个同级任务；
- 按 Esc 或留空会取消这个新节点。

### 编辑与删除

- 点击或双击任务文字进行重命名；
- 使用右键菜单添加标签、删除任务或执行其他操作；
- 鼠标移到节点上后，可用 `−` 删除；
- 删除有子节点的任务时，插件会要求确认，因为整棵子树会一起删除。

### 调整结构

在树视图中拖动节点，会移动该节点及其整棵子树。也可以使用右键菜单中的：

- **Nest under…**：移到另一个节点下面；
- **Indent / Outdent**：增加或减少一层深度；
- **Move up / Move down**：在同层调整顺序。

需要注意两个不同操作：

- 在 **Tree** 中拖动：改变父子关系，整棵子树一起移动；
- 在 **Kanban** 中拖动：只改变这个节点的状态，不移动其子节点。

---

## 6. 状态与父节点自动归并

默认状态为：

| Markdown | 状态 |
| --- | --- |
| `- [ ]` | To Do / 未开始 |
| `- [/]` | Doing / 进行中 |
| `- [x]` | Done / 已完成 |

父节点的状态由直接子节点自动推导：

- 所有有效子节点完成 → 父节点完成；
- 任一子节点开始、完成或阻塞 → 父节点进行中；
- 所有子节点都未开始 → 父节点未开始；
- 部分完成 → 显示类似 `2/5` 的进度和进度条。

计算会从叶节点向根节点逐层进行。因此完成一整棵子树后，它的父节点也会自动更新。

### 叶节点与父节点的区别

- **叶节点**没有子任务，它自身的 checkbox 是真实状态；
- **父节点**有子任务，它的 checkbox 通常只是子节点状态的计算结果。

所以，不要把父节点手动勾选理解为“孩子也全部完成”。如果确实想带着未完成事项关闭父节点，请使用手动覆盖。

### 带着遗留项关闭父节点

插件会写入类似：

```markdown
- [x] 暂停继续研究这个方向 [tt-override:: done] ^t-aa10
	- [ ] 阅读另一篇论文 ^t-bb20
```

这表示父节点是有意关闭的，而不是因为所有孩子都完成。把父任务拖回它本应归属的计算状态，可以清除 override。

如果配置了 **Cancelled** 状态，被取消的孩子不会进入完成比例；如果所有孩子都被取消，父节点也会推导为取消。

---

## 7. 给任务建立研究笔记

右键任务，选择：

```text
Open / create note
```

插件会为该任务建立单独的 Obsidian 笔记，并自动在任务末尾加入 `[[笔记链接]]`。

任务笔记适合记录：

- 为什么要研究这个问题；
- 找到的资料和链接；
- 实验过程、代码和截图；
- 临时结论；
- 最终答案和剩余疑问。

移动或重命名任务后，插件会自动更新任务笔记中的结构信息。删除任务不会删除笔记，而会把笔记标为 `orphaned`，避免研究记录丢失。

注意：1.0 版本中，写在任务笔记正文里的更深层 checklist **不会自动参与主 Board 的进度归并**。需要参与归并的工作仍应作为 Board 上的子节点。递归读取任务笔记中的子任务目前只是路线图功能。

---

## 8. 设置任务依赖

当一个任务必须等待另一个任务完成时：

1. 右键等待中的任务；
2. 选择 **Blocked by…**；
3. 选择它所依赖的任务。

底层格式类似：

```markdown
- [ ] 完成接口实验 ^t-aa10
- [ ] 总结结论 [tt-blocked-by:: t-aa10] ^t-bb20
```

依赖项完成或取消后，等待状态会解除。

依赖关系与父子关系不同：

- 父子关系表示“这个问题由哪些子问题组成”；
- 依赖关系表示“这个任务暂时要等待谁”；
- 依赖不会改变父节点的进度归并算法；
- Dashboard 会列出等待依赖的任务和目前可以开始的任务；
- Diagram 会用虚线显示依赖；
- 未知目标、自我依赖和循环依赖会显示警告。

当前只支持同一个 Board 文件内的依赖，不支持跨 Board 依赖。

---

## 9. 推荐的探索型工作流

### 第一步：内部节点写“问题”，叶节点写“下一步动作”

例如：

```markdown
- [ ] 搞清楚 Connector/J 8 的兼容风险
	- [ ] 返回值是否变化
		- [ ] 阅读官方 update count 文档
		- [ ] 写最小复现实验
	- [ ] 连接参数是否变化
		- [ ] 对比 5.1 与 8.0 参数表
```

“返回值是否变化”是问题节点，“阅读文档”和“写实验”是可以立即执行的叶节点。

### 第二步：探索中随时长出新分支

如果阅读文档时发现 `useAffectedRows`，直接在当前问题下面增加：

```markdown
		- [ ] 验证 useAffectedRows 的影响
```

不用预先把整棵树规划完整。

### 第三步：按需要选择 DFS 或 BFS

**DFS：一次深入一个分支**

1. 在树中选中一个问题；
2. 点击 Focus，只看这一棵子树；
3. 不断处理或新增叶节点；
4. 子树完成后沿面包屑返回上层。

**BFS：先横向扫描同一层**

1. 切换到 Columns 或完整 Diagram；
2. 先检查同一层的问题；
3. 决定哪些需要继续展开；
4. 再进入下一层。

**只想找现在能做什么**

打开 Dashboard，查看 **Blockers & next-up**。它会列出被阻塞的叶节点，以及当前可以直接开始的任务。

### 第四步：区分三种结束方式

- **解决**：完成叶节点，让状态自然向上归并；
- **放弃/无须继续**：使用 Cancelled 状态；
- **接受遗留问题并关闭**：使用 override，并在任务笔记中写明原因。

这样不会把“已经证明完成”与“决定暂时不做”混在一起。

---

## 10. 常用命令速查

| 命令 | 作用 |
| --- | --- |
| `Create a new board` | 创建新任务树 |
| `Convert current file to a Task Tree board` | 转换现有笔记 |
| `Open current file as dashboard` | 打开仪表盘 |
| `Open current file as Kanban board` | 打开看板 |
| `Open current file as tree` | 打开树视图 |
| `Open a board…` | 搜索并打开其他 Board |
| `Assign block IDs to all tasks in current file` | 为全部任务补充稳定 ID |
| `Build the boards index (index.md)` | 生成 Board 索引 |
| `Append an entry to the boards log (log.md)` | 向 Board 日志追加记录 |
| `Resync all task-note frontmatter` | 重新同步任务笔记结构信息 |

实际命令在 Obsidian 命令面板中通常带有 `Task Tree:` 前缀。

---

## 11. 当前版本的限制

截至 Task Tree 1.0：

- 尚无内建的截止日期和日程视图；
- 尚无循环任务；
- 尚无跨所有 Board 的全局任务查询；
- 依赖关系只支持同一个 Board；
- 不能直接把子树移动到另一个 Board；
- 任务笔记内部的 checklist 不参与主树归并；
- 几百个以上的可见节点可能遇到性能问题，虚拟化仍在路线图中。

因此它更适合“项目/研究探索树”，而不是替代完整的日历提醒型 Todo 软件。

---

## 12. 官方资料

- [Task Tree 官方 README](https://github.com/Aldorithm392/obsidian-task-tree)
- [Obsidian 插件页面](https://community.obsidian.md/plugins/task-tree)
- [Markdown 格式规范](https://github.com/Aldorithm392/obsidian-task-tree/blob/main/docs/03_FORMAT_SPEC.md)
- [项目指南与术语表](https://github.com/Aldorithm392/obsidian-task-tree/blob/main/docs/PROJECT_GUIDE.md)
- [路线图](https://github.com/Aldorithm392/obsidian-task-tree/blob/main/ROADMAP.md)
- [1.0.0 发布说明](https://github.com/Aldorithm392/obsidian-task-tree/releases/tag/1.0.0)

---

## 13. 让 AI 自动生成和维护任务树

### 推荐说法

```text
$task-tree 把这份需求拆成最小可执行任务树，直接写入「项目/MySQL 8 升级风险.md」。
内部节点写待解决的问题或结果，叶节点写能产出证据的动作；未知状态保持 todo。
```

也可以对已有 Board 说：

```text
$task-tree 展开“验证兼容性”分支，只增加下一层可执行任务，不改其他分支。
$task-tree 根据这份实验记录更新叶节点状态，并说明哪些父节点发生了归并。
$task-tree 检查这个 Board 的重复 ID、未知依赖、循环依赖和格式错误。
```

### Agent 的生成原则

- Board 标题表达项目结果；顶层直接放相互独立的里程碑，不再造一个重复标题的根节点；
- 内部节点写问题、决策或结果，叶节点以具体动词开头，并能判断何时完成；
- 只展开到“现在可以做”的深度，不一次生成大量猜测性的未来任务；
- 新任务不伪造 `^id`，等 Obsidian 插件分配；没有现成 ID 时不强行写依赖；
- 除非资料明确证明状态，否则统一从 `[ ]` 开始；
- 写完运行 `validate_board.py`，错误修好后再交付。

详细规则由仓库内唯一事实源维护：

- [Skill 入口](../.agents/skills/task-tree/SKILL.md)
- [AI 拆题规则](../.agents/skills/task-tree/references/authoring.md)
- [Board 编辑契约](../.agents/skills/task-tree/references/contract.md)
