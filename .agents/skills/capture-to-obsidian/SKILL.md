---
name: capture-to-obsidian
description: Turn a current or referenced conversation into durable, connected knowledge in an authorized Obsidian vault. Use when the user says “记一下”, “落个笔记”, “写进 Obsidian”, or asks to capture a discussion into their vault; do not use for a plain chat summary that is not meant to be written to the vault.
---

# Capture to Obsidian

Create or update useful knowledge notes, not transcript archives.

## Workflow

1. Read the vault's applicable `AGENTS.md` and inspect its current folder, naming, frontmatter,
   template, wikilink, and source conventions. Preserve plugin-managed content.
2. Read the full relevant conversation. If it references another ChatGPT conversation and the
   available preview is incomplete, retrieve the needed turns before writing.
3. Search filenames and note bodies for the main concepts, synonyms, English names, and likely
   related notes.
4. Decide separately for each knowledge unit:
   - **append** when it extends an existing note cleanly;
   - **merge** when the same concept is duplicated and consolidation is safe;
   - **create** only when it is independently reusable and lacks a natural home.
5. Rewrite the discussion into durable knowledge: conclusions, mental models, relationships,
   examples, practical next steps, and unresolved questions. Omit conversational filler.
6. Separate checkable material from sections such as “我的观察”, “我的理解”, “待验证”, or
   “开放问题”. Preserve authoritative source URLs near the claims they support.
7. Add only useful `[[wikilinks]]`, preferably to notes that already exist. Avoid empty link-target
   notes and repeated links that add no navigation value.
8. Review the diff for duplication, broken or ambiguous links, accidental frontmatter changes,
   and edits outside the requested topic. Report created/updated files and the decision for each.

## Vault defaults

- Adapt to the current vault; do not impose a new taxonomy, mandatory frontmatter, or template.
- Keep folders shallow and stable. Do not move, rename, delete, or mass-merge notes without an
  explicit request.
- Never edit Task Tree structure or its managed fields as part of ordinary capture.
- If no local filesystem access or authorized vault is available, explain that capture cannot be
  completed in that environment; do not pretend the note was written.

## Minimal trigger

Within a local task that can access the vault, the user may simply say: **“记一下。”**
