#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmet Zeybek and the Apex contributors
"""SessionStart hook: put the active planning workspace into the agent's context.

Reads `.apex-design/` in the session's working directory and prints a compact
summary of the active initiative(s): decision digest, glossary, current
position, and the next task. Plain text on stdout is added as context by the
host (Claude Code and Codex both do this for SessionStart). Prints nothing when
there is no workspace. Never writes, never blocks.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from apex_workspace import (
    Initiative,
    active_initiatives,
    read_stdin_payload,
    resolve_cwd,
)

MAX_INITIATIVES = 2
MAX_GLOSSARY_ROWS = 12
MAX_MEANING_CHARS = 100
MAX_CHARS = 2400


def render(init: Initiative) -> str:
    lines = [f"### {init.slug}: {init.title} [{init.status}]"]
    if init.status == "drafting":
        lines.append(
            "- Note: still drafting; confirm the decision digest with the owner "
            "before implementing."
        )
    lines.extend(
        f"- {key}: {init.fields[key]}"
        for key in ("Decision owner", "Domain expert")
        if key in init.fields
    )
    if init.digest:
        lines.append("- Decision digest:")
        lines.extend(f"  {ln}" for ln in init.digest.splitlines())
    if init.glossary:
        lines.append("- Glossary (use these names; do not invent synonyms or merge contexts):")
        lines.extend(
            f"  - {term} ({context}): {_clip(meaning, MAX_MEANING_CHARS)}"
            for term, context, meaning in init.glossary[:MAX_GLOSSARY_ROWS]
        )
        if len(init.glossary) > MAX_GLOSSARY_ROWS:
            lines.append(f"  - … {len(init.glossary) - MAX_GLOSSARY_ROWS} more in glossary.md")
    if init.position:
        lines.append(f"- Current position: {init.position}")
    if init.board:
        board = ", ".join(f"{count} {state}" for state, count in sorted(init.board.items()))
        lines.append(f"- Status board: {board}")
    if init.next_task:
        lines.append(f"- Next pending task: {init.next_task}")
    return "\n".join(lines)


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def build_context(cwd: Path) -> str:
    initiatives = active_initiatives(cwd)
    if not initiatives:
        return ""
    intro = (
        "Apex planning workspace (.apex-design/) is present in this repository. "
        "Read the initiative's brief, glossary, requirements, design, and plan before changing "
        "code, work the plan's tasks in order, and keep progress.md current."
    )
    parts = [intro]
    parts.extend(render(init) for init in initiatives[:MAX_INITIATIVES])
    if len(initiatives) > MAX_INITIATIVES:
        parts.append(f"({len(initiatives) - MAX_INITIATIVES} more active initiative(s) not shown.)")
    text = "\n\n".join(parts)
    if len(text) > MAX_CHARS:
        text = text[: MAX_CHARS - 1].rstrip() + "…"
    return text


def main() -> int:
    payload = read_stdin_payload()
    text = build_context(resolve_cwd(payload))
    if text:
        sys.stdout.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
