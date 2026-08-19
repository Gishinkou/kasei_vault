#!/usr/bin/env python3
"""Diagnose, enable, or install Task Tree in an Obsidian vault."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PLUGIN_ID = "task-tree"
REPOSITORY = "Aldorithm392/obsidian-task-tree"
RELEASE_FILES = ("main.js", "manifest.json", "styles.css")


def find_vault(start: Path) -> Path | None:
    current = start.expanduser().resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".obsidian").is_dir():
            return candidate
    return None


def resolve_vault(value: str | None) -> Path:
    vault = find_vault(Path(value) if value else Path.cwd())
    if vault is None:
        raise RuntimeError("no Obsidian vault found; pass --vault /absolute/path/to/vault")
    return vault


def read_json(path: Path, default: object) -> object:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot parse {path}: {exc}") from exc


def installation(vault: Path) -> tuple[Path, dict[str, object] | None, list[str]]:
    plugin_dir = vault / ".obsidian" / "plugins" / PLUGIN_ID
    missing = [name for name in RELEASE_FILES if not (plugin_dir / name).is_file()]
    manifest: dict[str, object] | None = None
    if not missing:
        value = read_json(plugin_dir / "manifest.json", {})
        if not isinstance(value, dict):
            raise RuntimeError(f"{plugin_dir / 'manifest.json'} must contain a JSON object")
        manifest = value
        if manifest.get("id") != PLUGIN_ID:
            raise RuntimeError(f"unexpected plugin id in {plugin_dir / 'manifest.json'}")
    return plugin_dir, manifest, missing


def enabled_plugins(vault: Path) -> tuple[Path, list[str]]:
    path = vault / ".obsidian" / "community-plugins.json"
    value = read_json(path, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise RuntimeError(f"{path} must contain a JSON string array")
    return path, value


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def enable(vault: Path) -> bool:
    _, manifest, missing = installation(vault)
    if missing or manifest is None:
        raise RuntimeError(f"Task Tree is not installed; missing: {', '.join(missing)}")
    path, plugins = enabled_plugins(vault)
    if PLUGIN_ID in plugins:
        return False
    plugins.append(PLUGIN_ID)
    write_json_atomic(path, plugins)
    return True


def download(url: str, destination: Path) -> None:
    request = Request(url, headers={"User-Agent": "task-tree-skill-setup/1"})
    try:
        with urlopen(request, timeout=30) as response, destination.open("wb") as stream:
            shutil.copyfileobj(response, stream)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"download failed for {url}: {exc}") from exc


def install(vault: Path, version: str, force: bool, no_enable: bool) -> None:
    if not version or "/" in version or version in {".", ".."}:
        raise RuntimeError("--version must be a release tag such as 1.0.0")
    plugin_dir, manifest, missing = installation(vault)
    installed_version = str(manifest.get("version")) if manifest else None
    if not missing and installed_version == version and not force:
        print(f"Task Tree {version} is already installed")
    else:
        if installed_version and installed_version != version and not force:
            raise RuntimeError(
                f"Task Tree {installed_version} is installed; pass --force to replace it with {version}"
            )
        plugin_dir.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="task-tree-download-", dir=plugin_dir.parent) as name:
            staging = Path(name)
            base = f"https://github.com/{REPOSITORY}/releases/download/{version}"
            for filename in RELEASE_FILES:
                download(f"{base}/{filename}", staging / filename)
            downloaded = read_json(staging / "manifest.json", {})
            if not isinstance(downloaded, dict) or downloaded.get("id") != PLUGIN_ID:
                raise RuntimeError("downloaded manifest has an unexpected plugin id")
            if str(downloaded.get("version")) != version:
                raise RuntimeError(
                    f"downloaded manifest version {downloaded.get('version')!r} does not match {version!r}"
                )
            plugin_dir.mkdir(parents=True, exist_ok=True)
            for filename in RELEASE_FILES:
                os.replace(staging / filename, plugin_dir / filename)
        print(f"Installed Task Tree {version}")
    if not no_enable:
        print("Enabled Task Tree" if enable(vault) else "Task Tree was already enabled")


def check(vault: Path) -> int:
    plugin_dir, manifest, missing = installation(vault)
    _, plugins = enabled_plugins(vault)
    skill = vault / ".agents" / "skills" / "task-tree" / "SKILL.md"
    installed = not missing and manifest is not None
    active = PLUGIN_ID in plugins
    print(f"Vault: {vault}")
    print(f"Plugin files: {'ready' if installed else 'missing ' + ', '.join(missing)}")
    if installed:
        print(f"Plugin version: {manifest.get('version', 'unknown')}")
    print(f"Enabled in Obsidian config: {'yes' if active else 'no'}")
    print(f"Codex/agent skill: {'ready' if skill.is_file() else 'missing'}")
    if installed and active:
        print("Result: ready on disk; reload Obsidian if the plugin is not visible")
    else:
        print(f"Plugin directory: {plugin_dir}")
        print("Result: setup incomplete")
    return 0 if installed and active and skill.is_file() else 1


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--vault", help="vault path or a path inside it")
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="report setup state without writing")
    commands.add_parser("enable", help="add task-tree to community-plugins.json")
    install_parser = commands.add_parser("install", help="install a pinned GitHub release")
    install_parser.add_argument("--version", default="1.0.0", help="GitHub release tag")
    install_parser.add_argument("--force", action="store_true", help="replace another installed version")
    install_parser.add_argument("--no-enable", action="store_true", help="install without enabling")
    return result


def main() -> int:
    arguments = parser().parse_args()
    try:
        vault = resolve_vault(arguments.vault)
        if arguments.command == "check":
            return check(vault)
        if arguments.command == "enable":
            print("Enabled Task Tree" if enable(vault) else "Task Tree was already enabled")
            return 0
        install(vault, arguments.version, arguments.force, arguments.no_enable)
        return 0
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

