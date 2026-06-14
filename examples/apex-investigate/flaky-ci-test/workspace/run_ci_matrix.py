#!/usr/bin/env python3
"""Run the routing test under several deterministic hash seeds."""

from __future__ import annotations

import json
import os
import subprocess
import sys


def main() -> int:
    results = []
    for seed in range(1, 21):
        env = os.environ.copy()
        env["PYTHONHASHSEED"] = str(seed)
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "-q", "test_routing.py"],
            capture_output=True,
            text=True,
            env=env,
            timeout=10,
        )
        results.append({"seed": seed, "passed": proc.returncode == 0})
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
