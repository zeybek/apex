# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmet Zeybek and the Apex contributors
"""Tests for the planning-workspace hooks (session context and stop guard)."""

from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path

import apex_session_context as session
import apex_stop_guard as guard
import apex_workspace as ws
import pytest

HOOKS = Path(__file__).resolve().parents[1] / "plugins" / "apex" / "hooks"


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def write_workspace(
    repo: Path, slug: str = "001-landing-page", status: str = "in progress"
) -> Path:
    init = repo / ".apex-design" / slug
    init.mkdir(parents=True)
    (init / "brief.md").write_text(
        f"# Marketing landing page\n\n- Status: {status}\n- Decision owner: Ahmet\n"
        "- Domain expert: Ayşe (sales)\n\n## Decisions log\n- D-01 — audience -> founders\n",
        encoding="utf-8",
    )
    (init / "design.md").write_text(
        "# Design\n\n## Decision digest\nStatic page in the existing framework.\n"
        "Riskiest assumption: spam control is enough.\n\n## Recommendation\nStatic page.\n",
        encoding="utf-8",
    )
    (init / "glossary.md").write_text(
        "# Glossary\n\n| Term | Context | Meaning | Not to be confused with | Confirmed by |\n"
        "|---|---|---|---|---|\n"
        "| Lead | marketing | a visitor who submitted the form | User | D-02 |\n"
        "| User | product | an activated account | Lead | D-02 |\n"
        "| <fill: term> | <fill: ctx> | <fill: meaning> | | |\n",
        encoding="utf-8",
    )
    (init / "plan.md").write_text(
        "# Plan\n\n- T-01 — Scaffold the route\n  - files: src/landing.tsx\n"
        "- T-02 — Build hero and CTA\n- T-03 — Add the form\n",
        encoding="utf-8",
    )
    (init / "progress.md").write_text(
        "# Progress\n\n- Updated: today\n- Current position: T-02 in progress\n\n"
        "## Status board\n- T-01 — done — route scaffolded\n- T-02 — in progress\n"
        "- T-03 — pending\n",
        encoding="utf-8",
    )
    return init


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q", ".")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "config", "user.name", "t")
    return tmp_path


# --- workspace parsing -------------------------------------------------------


def test_parse_initiative_reads_every_section(repo: Path) -> None:
    init = ws.parse_initiative(write_workspace(repo))
    assert init.title == "Marketing landing page"
    assert init.status == "in progress"
    assert init.fields == {"Decision owner": "Ahmet", "Domain expert": "Ayşe (sales)"}
    assert init.digest.startswith("Static page")
    assert [row[0] for row in init.glossary] == ["Lead", "User"]  # fill markers skipped
    assert init.position == "T-02 in progress"
    assert init.board == {"done": 1, "in progress": 1, "pending": 1}
    assert init.next_task == "T-03 — Add the form"


def test_active_initiatives_orders_in_progress_first_and_drops_done(tmp_path: Path) -> None:
    write_workspace(tmp_path, "001-a", "planned")
    write_workspace(tmp_path, "002-b", "in progress")
    write_workspace(tmp_path, "003-c", "done")
    write_workspace(tmp_path, "004-d", "superseded")
    assert [i.slug for i in ws.active_initiatives(tmp_path)] == ["002-b", "001-a"]


def test_find_initiatives_ignores_foreign_folders(tmp_path: Path) -> None:
    write_workspace(tmp_path)
    (tmp_path / ".apex-design" / "notes").mkdir()
    (tmp_path / ".apex-design" / "README.md").write_text("# index\n", encoding="utf-8")
    assert [i.slug for i in ws.find_initiatives(tmp_path)] == ["001-landing-page"]


def test_partial_workspace_yields_less_context_not_errors(tmp_path: Path) -> None:
    init = tmp_path / ".apex-design" / "007-bare"
    init.mkdir(parents=True)
    (init / "brief.md").write_text("# Bare\n\n- Status: in progress\n", encoding="utf-8")
    parsed = ws.parse_initiative(init)
    assert parsed.title == "Bare"
    assert parsed.digest == ""
    assert parsed.glossary == []
    assert parsed.next_task == ""


def test_stdin_payload_tolerates_garbage(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO("not json"))
    assert ws.read_stdin_payload() == {}
    monkeypatch.setattr(sys, "stdin", io.StringIO("[1,2]"))
    assert ws.read_stdin_payload() == {}
    monkeypatch.setattr(sys, "stdin", io.StringIO('{"cwd": "/nope/missing"}'))
    assert ws.resolve_cwd(ws.read_stdin_payload()) == Path.cwd()


# --- session context ---------------------------------------------------------


def test_session_context_is_empty_without_workspace(tmp_path: Path) -> None:
    assert session.build_context(tmp_path) == ""


def test_session_context_contains_digest_glossary_and_next_task(repo: Path) -> None:
    write_workspace(repo)
    text = session.build_context(repo)
    assert "001-landing-page: Marketing landing page [in progress]" in text
    assert "Static page in the existing framework." in text
    assert "Lead (marketing): a visitor who submitted the form" in text
    assert "Next pending task: T-03 — Add the form" in text
    assert "keep progress.md current" in text


def test_session_context_flags_drafting_and_caps_size(tmp_path: Path) -> None:
    init = write_workspace(tmp_path, status="drafting")
    (init / "glossary.md").write_text(
        "| Term | Context | Meaning | x | y |\n|---|---|---|---|---|\n"
        + "".join(f"| Term{i} | ctx | {'m' * 200} | | |\n" for i in range(40)),
        encoding="utf-8",
    )
    text = session.build_context(tmp_path)
    assert "still drafting" in text
    assert "more in glossary.md" in text
    assert len(text) <= session.MAX_CHARS


def test_session_context_cli_prints_and_exits_zero(repo: Path) -> None:
    write_workspace(repo)
    proc = subprocess.run(
        [sys.executable, str(HOOKS / "apex_session_context.py")],
        input=json.dumps({"cwd": str(repo), "hook_event_name": "SessionStart"}),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "Marketing landing page" in proc.stdout


# --- stop guard --------------------------------------------------------------


def test_stop_guard_allows_when_no_initiative_in_progress(repo: Path) -> None:
    write_workspace(repo, status="planned")
    (repo / "x.py").write_text("x\n", encoding="utf-8")
    assert guard.evaluate(repo, {}) == ""


def test_stop_guard_allows_clean_tree(repo: Path) -> None:
    write_workspace(repo)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    assert guard.evaluate(repo, {}) == ""


def test_stop_guard_blocks_code_change_without_progress_update(repo: Path) -> None:
    write_workspace(repo)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    (repo / "src").mkdir()
    (repo / "src" / "landing.tsx").write_text("x\n", encoding="utf-8")
    reason = guard.evaluate(repo, {})
    assert "001-landing-page" in reason
    assert "src/landing.tsx" in reason
    assert "progress.md was not updated" in reason


def test_stop_guard_allows_when_progress_was_touched(repo: Path) -> None:
    init = write_workspace(repo)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    (repo / "x.py").write_text("x\n", encoding="utf-8")
    with (init / "progress.md").open("a", encoding="utf-8") as fh:
        fh.write("- T-02 — done\n")
    assert guard.evaluate(repo, {}) == ""


def test_stop_guard_never_blocks_twice(repo: Path) -> None:
    write_workspace(repo)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    (repo / "x.py").write_text("x\n", encoding="utf-8")
    assert guard.evaluate(repo, {"stop_hook_active": True}) == ""


def test_stop_guard_ignores_workspace_only_changes(repo: Path) -> None:
    init = write_workspace(repo)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    (init / "brief.md").write_text("# changed\n\n- Status: in progress\n", encoding="utf-8")
    assert guard.evaluate(repo, {}) == ""


def test_stop_guard_allows_outside_git(tmp_path: Path) -> None:
    write_workspace(tmp_path)
    (tmp_path / "x.py").write_text("x\n", encoding="utf-8")
    assert guard.changed_paths(tmp_path) is None
    assert guard.evaluate(tmp_path, {}) == ""


def test_stop_guard_cli_exit_codes(repo: Path) -> None:
    write_workspace(repo)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "init")
    (repo / "x.py").write_text("x\n", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(HOOKS / "apex_stop_guard.py")],
        input=json.dumps({"cwd": str(repo)}),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 2
    assert "progress.md" in proc.stderr
    proc = subprocess.run(
        [sys.executable, str(HOOKS / "apex_stop_guard.py")],
        input=json.dumps({"cwd": str(repo), "stop_hook_active": True}),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0


def test_hooks_json_points_at_shipped_scripts() -> None:
    data = json.loads((HOOKS / "hooks.json").read_text(encoding="utf-8"))
    assert set(data["hooks"]) == {"SessionStart", "Stop"}
    for groups in data["hooks"].values():
        for group in groups:
            for hook in group["hooks"]:
                assert hook["type"] == "command"
                script = hook["command"].rsplit("/hooks/", 1)[1].rstrip('"')
                assert (HOOKS / script).is_file()
