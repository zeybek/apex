# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmet Zeybek and the Apex contributors
"""Read-only helpers for the .apex-design planning workspace.

Shared by the session-context and stop-guard hooks. Standard library only,
never writes, never talks to the network. Every parser here is tolerant: a
malformed or partial workspace yields less context, not an error.
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

WORKSPACE_DIR = ".apex-design"
INITIATIVE_PATTERN = re.compile(r"^\d{3,}-[a-z0-9][a-z0-9-]*$")
STATUS_PATTERN = re.compile(r"^\s*-\s*Status:\s*(.+?)\s*$", re.MULTILINE)
FIELD_PATTERN = re.compile(r"^\s*-\s*(Decision owner|Domain expert):\s*(.+?)\s*$", re.MULTILINE)
TITLE_PATTERN = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
SECTION_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
TASK_PATTERN = re.compile(r"^-\s*(T-\d+)\s*[—-]\s*(.+?)\s*$", re.MULTILINE)
BOARD_PATTERN = re.compile(
    r"^-\s*(T-\d+)\s*[—-]\s*(pending|in progress|done|blocked)\b", re.MULTILINE | re.IGNORECASE
)
POSITION_PATTERN = re.compile(r"^\s*-\s*Current position:\s*(.+?)\s*$", re.MULTILINE)
ACTIVE_STATUSES = ("in progress", "planned", "drafting")


@dataclass
class Initiative:
    """One `.apex-design/<NNN-slug>/` folder, parsed leniently."""

    path: Path
    title: str = ""
    status: str = "unknown"
    fields: dict[str, str] = field(default_factory=dict)
    digest: str = ""
    glossary: list[tuple[str, str, str]] = field(default_factory=list)
    position: str = ""
    board: dict[str, int] = field(default_factory=dict)
    next_task: str = ""

    @property
    def slug(self) -> str:
        return self.path.name

    @property
    def progress_file(self) -> Path:
        return self.path / "progress.md"


def read_stdin_payload() -> dict[str, Any]:
    """Parse the hook's JSON payload from stdin; tolerate empty or bad input."""
    if sys.stdin is None or sys.stdin.isatty():
        return {}
    try:
        raw = sys.stdin.read()
    except OSError:
        return {}
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def resolve_cwd(payload: dict[str, Any]) -> Path:
    """The session's working directory: the payload's cwd, else the process cwd."""
    cwd = payload.get("cwd")
    if isinstance(cwd, str) and cwd and Path(cwd).is_dir():
        return Path(cwd)
    return Path(os.getcwd())


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def _section(text: str, heading: str) -> str:
    """Body of the `## heading` section, up to the next `##`."""
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return ""
    rest = text[match.end() :]
    nxt = SECTION_PATTERN.search(rest)
    body = rest[: nxt.start()] if nxt else rest
    return body.strip()


def _clean_digest(body: str) -> str:
    lines = [ln.strip() for ln in body.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("<fill:")]
    return "\n".join(lines)


def _parse_glossary(text: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0].lower() == "term" or set(cells[0]) <= {"-", ":"}:
            continue
        if cells[0].startswith("<fill:"):
            continue
        rows.append((cells[0], cells[1], cells[2]))
    return rows


def parse_initiative(path: Path) -> Initiative:
    init = Initiative(path=path)
    brief = _read(path / "brief.md")
    design = _read(path / "design.md")
    glossary = _read(path / "glossary.md")
    plan = _read(path / "plan.md")
    progress = _read(path / "progress.md")

    title = TITLE_PATTERN.search(brief)
    init.title = title.group(1) if title else path.name
    status = STATUS_PATTERN.search(brief)
    if status:
        init.status = status.group(1).split("|")[0].strip().lower()
    for m in FIELD_PATTERN.finditer(brief):
        if not m.group(2).startswith("<fill:"):
            init.fields[m.group(1)] = m.group(2)
    init.digest = _clean_digest(
        _section(design, "Decision digest") or _section(brief, "Decision digest")
    )
    init.glossary = _parse_glossary(glossary)

    position = POSITION_PATTERN.search(progress)
    if position and not position.group(1).startswith("<fill:"):
        init.position = position.group(1)
    for m in BOARD_PATTERN.finditer(progress):
        key = m.group(2).lower()
        init.board[key] = init.board.get(key, 0) + 1
    done_or_active = {
        m.group(1) for m in BOARD_PATTERN.finditer(progress) if m.group(2).lower() != "pending"
    }
    for m in TASK_PATTERN.finditer(plan):
        if m.group(1) not in done_or_active:
            init.next_task = f"{m.group(1)} — {m.group(2)}"
            break
    return init


def find_initiatives(cwd: Path) -> list[Initiative]:
    """All initiatives under cwd/.apex-design, most recently touched first."""
    root = cwd / WORKSPACE_DIR
    if not root.is_dir():
        return []
    found: list[tuple[float, Initiative]] = []
    for child in root.iterdir():
        if not child.is_dir() or not INITIATIVE_PATTERN.match(child.name):
            continue
        try:
            stamp = (
                max(p.stat().st_mtime for p in child.glob("*.md"))
                if any(child.glob("*.md"))
                else 0.0
            )
        except OSError:
            stamp = 0.0
        found.append((stamp, parse_initiative(child)))
    found.sort(key=lambda item: item[0], reverse=True)
    return [init for _, init in found]


def active_initiatives(cwd: Path) -> list[Initiative]:
    """Initiatives that are not done or superseded, in-progress ones first."""
    order = {name: index for index, name in enumerate(ACTIVE_STATUSES)}
    active = [i for i in find_initiatives(cwd) if i.status in order]
    active.sort(key=lambda i: order[i.status])
    return active
