#!/usr/bin/env python3
"""Validate Task Tree board structure, ids, and same-board dependencies."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re

TASK = re.compile(r"^(?P<indent>\s*)(?P<marker>[-*+])\s+\[(?P<status>.)\]\s?(?P<body>.*)$")
ID = re.compile(r"\s+\^(?P<id>[A-Za-z0-9-]+)\s*$")
BLOCKED_BY = re.compile(r"\[tt-blocked-by::\s*(?P<ids>[^\]]*)\]")
RESERVED = re.compile(r"\[tt-(?P<name>[A-Za-z0-9-]+)::")


@dataclass
class Task:
    line: int
    task_id: str | None
    dependencies: list[str]


def frontmatter_type(lines: list[str]) -> str | None:
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^type\s*:\s*['\"]?([^'\"#\s]+)", line.strip())
        if match:
            return match.group(1)
    return None


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [f"cannot read: {exc}"], warnings
    if frontmatter_type(lines) != "task-tree":
        errors.append("frontmatter must contain type: task-tree")
        return errors, warnings

    tasks: list[Task] = []
    id_lines: dict[str, list[int]] = defaultdict(list)
    indentation_kinds: set[str] = set()
    for number, line in enumerate(lines, 1):
        match = TASK.match(line)
        if not match:
            continue
        indent = match.group("indent")
        if indent:
            indentation_kinds.add(
                "tabs" if set(indent) == {"\t"} else "spaces" if set(indent) == {" "} else "mixed"
            )
        body = match.group("body")
        id_match = ID.search(body)
        task_id = id_match.group("id") if id_match else None
        if task_id:
            id_lines[task_id].append(number)
        reserved = RESERVED.findall(body)
        unknown = sorted(set(reserved) - {"override", "blocked-by"})
        if unknown:
            errors.append(f"line {number}: unknown reserved fields: {', '.join(unknown)}")
        dependencies: list[str] = []
        blocked_matches = list(BLOCKED_BY.finditer(body))
        if len(blocked_matches) > 1:
            errors.append(f"line {number}: multiple tt-blocked-by fields")
        if blocked_matches:
            raw_ids = [item.strip() for item in blocked_matches[0].group("ids").split(",")]
            if not raw_ids or any(not re.fullmatch(r"[A-Za-z0-9-]+", item or "") for item in raw_ids):
                errors.append(f"line {number}: invalid tt-blocked-by id list")
            else:
                dependencies = raw_ids
        if "[tt-" in body and task_id and body.rfind("[tt-") > body.rfind(f"^{task_id}"):
            errors.append(f"line {number}: reserved field must appear before the trailing block id")
        tasks.append(Task(number, task_id, dependencies))

    if not tasks:
        warnings.append("board contains no task lines")
    if "mixed" in indentation_kinds or len(indentation_kinds - {"mixed"}) > 1:
        errors.append("task indentation mixes tabs and spaces")
    for task_id, occurrences in sorted(id_lines.items()):
        if len(occurrences) > 1:
            errors.append(f"duplicate id {task_id} on lines {', '.join(map(str, occurrences))}")

    known = set(id_lines)
    graph: dict[str, list[str]] = defaultdict(list)
    for task in tasks:
        for target in task.dependencies:
            if target not in known:
                errors.append(f"line {task.line}: dependency target {target} is missing")
            if task.task_id == target:
                errors.append(f"line {task.line}: task depends on itself ({target})")
            if task.task_id and target in known:
                graph[task.task_id].append(target)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, trail: list[str]) -> None:
        if node in visiting:
            start = trail.index(node)
            errors.append(f"dependency cycle: {' -> '.join(trail[start:])}")
            return
        if node in visited:
            return
        visiting.add(node)
        for target in graph[node]:
            visit(target, trail + [target])
        visiting.remove(node)
        visited.add(node)

    for node in sorted(graph):
        visit(node, [node])
    return list(dict.fromkeys(errors)), warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("boards", nargs="+", type=Path)
    arguments = parser.parse_args()
    failed = False
    for board in arguments.boards:
        errors, warnings = validate(board)
        for message in errors:
            print(f"ERROR {board}: {message}")
        for message in warnings:
            print(f"WARN  {board}: {message}")
        if not errors and not warnings:
            print(f"OK    {board}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

