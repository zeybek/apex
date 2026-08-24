#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmet Zeybek and the Apex contributors
"""Stop hook: keep the planning workspace's progress board honest.

When an initiative is `in progress`, the working tree has uncommitted changes
outside `.apex-design/`, and that initiative's `progress.md` has not been
touched, the hook blocks the stop (exit 2 with the reason on stderr, which
both Claude Code and Codex understand) so the agent records task status,
outcomes, and the owner handoff before finishing. It never blocks twice in a
row (`stop_hook_active`), never blocks outside a git repository, and never
writes anything.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from apex_workspace import (
    WORKSPACE_DIR,
    active_initiatives,
    read_stdin_payload,
    resolve_cwd,
)


def changed_paths(cwd: Path) -> list[str] | None:
    """Paths with uncommitted changes, or None when not a git repository."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(cwd), "status", "--porcelain=v1", "--untracked-files=all"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    paths: list[str] = []
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path.strip().strip('"'))
    return paths


def evaluate(cwd: Path, payload: dict[str, object]) -> str:
    """Return the block reason, or an empty string to allow stopping."""
    if payload.get("stop_hook_active"):
        return ""
    in_progress = [i for i in active_initiatives(cwd) if i.status == "in progress"]
    if not in_progress:
        return ""
    changes = changed_paths(cwd)
    if not changes:
        return ""
    prefix = WORKSPACE_DIR + "/"
    code_changed = [p for p in changes if not p.startswith(prefix)]
    if not code_changed:
        return ""
    stale = [i for i in in_progress if f"{prefix}{i.slug}/progress.md" not in changes]
    if not stale:
        return ""
    names = ", ".join(f"{i.slug} ({i.title})" for i in stale)
    sample = ", ".join(code_changed[:5]) + (" …" if len(code_changed) > 5 else "")
    return (
        f"apex: initiative {names} is in progress and the working tree changed ({sample}), "
        f"but its .apex-design/<slug>/progress.md was not updated. Before finishing, record the "
        "task status, outcome or evidence, current position, and the owner handoff in progress.md "
        "(and any decision that changed in brief.md). If these changes are unrelated to the "
        "initiative, say so explicitly and finish."
    )


def main() -> int:
    payload = read_stdin_payload()
    reason = evaluate(resolve_cwd(payload), payload)
    if reason:
        sys.stderr.write(reason + "\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
