# Setup and environment portability

Use this reference only for installation, activation, diagnosis, or cross-environment questions.

## Fast path in this vault

This repository intentionally tracks:

- `.obsidian/plugins/task-tree/{main.js,manifest.json,styles.css}`
- `.obsidian/community-plugins.json` with `task-tree` enabled
- `.obsidian/plugins/task-tree/data.json`
- `.agents/skills/task-tree/`
- the root `AGENTS.md` generated contract

Therefore a complete Git checkout normally contains both the Obsidian plugin and the agent instructions. Obsidian Git synchronization transports these tracked files; it does not guarantee that another agent has the Obsidian application or has reloaded its plugins.

## Diagnose first

From anywhere inside the vault, run:

```bash
python3 .agents/skills/task-tree/scripts/setup_task_tree.py check
```

When the current directory is uncertain, pass `--vault /absolute/path/to/vault`. The command is read-only and reports these states separately:

- plugin files installed;
- plugin id enabled in `community-plugins.json`;
- agent skill present;
- Obsidian absent or not running (not an error for Markdown-only work).

Do not edit user-global Codex or Claude configuration merely to make this repository work. Codex discovers the checked-in `.agents/skills` directory from the repository hierarchy. Agents without Skill support still receive the root `AGENTS.md` contract.

## Repair or install only when asked

If files exist but the plugin is not enabled:

```bash
python3 .agents/skills/task-tree/scripts/setup_task_tree.py enable
```

If the plugin files are absent and the user explicitly asks the agent to install them, download a pinned official GitHub release and enable it:

```bash
python3 .agents/skills/task-tree/scripts/setup_task_tree.py install --version 1.0.0
```

The installer writes only the three release artifacts under `.obsidian/plugins/task-tree/` and the plugin id in `.obsidian/community-plugins.json`. It preserves `data.json`. It refuses to replace a different installed version unless `--force` is supplied. Network failure leaves the existing installation untouched.

After any installation or activation change, ask the user to restart Obsidian or reload community plugins. An agent cannot claim the plugin is running merely because files are present.

## UI alternatives

When automation is unavailable, use one of these user-driven paths:

1. Obsidian Settings → Community plugins → search **Task Tree** → Install → Enable.
2. If it is unavailable in Community plugins, install BRAT, run **BRAT: Add a beta plugin**, enter `Aldorithm392/obsidian-task-tree`, then enable Task Tree.

Do not install BRAT when the community release or the tracked plugin files already work.

## Capability matrix

| Environment | Safe capabilities | Missing runtime effects |
| --- | --- | --- |
| Git checkout, no Obsidian | Create/edit/validate boards and report status | No visual tree, automatic ids, or task-note reconciliation |
| Obsidian, plugin files disabled | Same Markdown operations | Plugin commands and reconciliation do not run |
| Obsidian with Task Tree enabled | Full board UI and commands | Restart/reload may still be needed after file changes |
| Partial checkout without `.obsidian` | Agent skill may still guide Markdown authoring | Cannot install into a vault until its root is known |

