#!/usr/bin/env python3
"""Regression tests for Task Tree skill helpers."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


setup = load("task_tree_setup", ROOT / "scripts" / "setup_task_tree.py")
validator = load("task_tree_validator", ROOT / "scripts" / "validate_board.py")


class BoardValidatorTests(unittest.TestCase):
    def test_valid_board(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            board = Path(directory) / "board.md"
            board.write_text(
                "---\ntype: task-tree\ntitle: Test\n---\n\n"
                "- [ ] Prepare ^t-a\n\t- [x] Verify ^t-b\n"
                "- [ ] Publish [tt-blocked-by:: t-b] ^t-c\n",
                encoding="utf-8",
            )
            errors, warnings = validator.validate(board)
            self.assertEqual([], errors)
            self.assertEqual([], warnings)

    def test_duplicate_cycle_and_misplaced_id(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            board = Path(directory) / "board.md"
            board.write_text(
                "---\ntype: task-tree\n---\n\n"
                "- [ ] A [tt-blocked-by:: t-b] ^t-a\n"
                "- [ ] B [tt-blocked-by:: t-a] ^t-b\n"
                "- [ ] Duplicate ^t-a\n"
                "- [ ] Misplaced ^t-z [tt-override:: done]\n",
                encoding="utf-8",
            )
            errors, _ = validator.validate(board)
            joined = "\n".join(errors)
            self.assertIn("duplicate id t-a", joined)
            self.assertIn("dependency cycle", joined)
            self.assertIn("block id must be the final field", joined)


class SetupTests(unittest.TestCase):
    def test_enable_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            plugin = vault / ".obsidian" / "plugins" / "task-tree"
            plugin.mkdir(parents=True)
            (plugin / "main.js").write_text("", encoding="utf-8")
            (plugin / "styles.css").write_text("", encoding="utf-8")
            setup.write_json_atomic(
                plugin / "manifest.json", {"id": "task-tree", "version": "1.0.0"}
            )
            self.assertTrue(setup.enable(vault))
            self.assertFalse(setup.enable(vault))
            _, plugins = setup.enabled_plugins(vault)
            self.assertEqual(["task-tree"], plugins)

    @unittest.skipUnless(os.environ.get("TASK_TREE_NETWORK_TEST") == "1", "network test disabled")
    def test_install_official_release(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / ".obsidian").mkdir()
            setup.install(vault, "1.0.0", force=False, no_enable=False)
            _, manifest, missing = setup.installation(vault)
            self.assertEqual([], missing)
            self.assertEqual("1.0.0", manifest["version"])
            _, plugins = setup.enabled_plugins(vault)
            self.assertIn("task-tree", plugins)


if __name__ == "__main__":
    unittest.main()
