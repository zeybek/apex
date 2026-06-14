#!/usr/bin/env python3
"""Verify that the flaky-test investigation identified the mechanism."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

EXPECTED = {
    "trigger": "python-hash-seed",
    "mechanism": "unordered-set-iteration",
    "scope": "select_primary",
    "mitigation": "pin-hash-seed",
    "durable_fix": "explicit-region-priority",
    "prevention": "multi-seed-ci",
}


def reproduce(workspace: Path) -> list[dict]:
    proc = subprocess.run(
        [sys.executable, "run_ci_matrix.py"],
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if proc.returncode:
        raise AssertionError(f"reproduction command failed: {proc.stderr.strip()}")
    results = json.loads(proc.stdout)
    if not isinstance(results, list) or not results:
        raise AssertionError("reproduction command did not emit a result list")
    if not any(item.get("passed") is True for item in results):
        raise AssertionError("no passing seed was preserved")
    if not any(item.get("passed") is False for item in results):
        raise AssertionError("no failing seed was preserved")
    return results


def verify_record(workspace: Path) -> None:
    path = workspace / "investigation.json"
    if not path.is_file():
        raise AssertionError("investigation.json is missing")
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise AssertionError("investigation.json must contain an object")
    for field, expected in EXPECTED.items():
        if record.get(field) != expected:
            raise AssertionError(f"{field} must be {expected!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", nargs="?", default=Path(__file__).parent / "workspace")
    args = parser.parse_args(argv)
    workspace = Path(args.workspace).resolve()

    try:
        results = reproduce(workspace)
        verify_record(workspace)
    except (AssertionError, json.JSONDecodeError, OSError, subprocess.SubprocessError) as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        return 1

    passing = sum(item["passed"] for item in results)
    print(
        f"verification passed: mechanism recorded; observed {passing}/{len(results)} passing seeds"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
