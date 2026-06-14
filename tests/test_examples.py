"""Contract tests for the runnable example workspaces."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def run_verifier(script: Path, workspace: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), str(workspace)],
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_all_skill_walkthroughs_have_required_files():
    scenarios = {
        "apex-design/service-boundary": False,
        "apex-implement/duplicate-job": True,
        "apex-investigate/flaky-ci-test": True,
        "apex-review/tenant-authorization": False,
    }
    for relative, executable in scenarios.items():
        scenario = EXAMPLES / relative
        for name in ("README.md", "prompt.md", "rubric.md", "workspace"):
            assert (scenario / name).exists(), f"{relative} is missing {name}"
        assert (scenario / "verify.py").exists() is executable


def test_duplicate_job_starts_failing_and_accepts_correct_behavior(tmp_path):
    scenario = EXAMPLES / "apex-implement" / "duplicate-job"
    workspace = tmp_path / "workspace"
    shutil.copytree(scenario / "workspace", workspace)

    initial = run_verifier(scenario / "verify.py", workspace)
    assert initial.returncode == 1
    assert "expected one charge" in initial.stderr

    (workspace / "order_worker.py").write_text(
        '''"""Correct behavior used to prove the example verifier contract."""

from dataclasses import dataclass
from threading import Lock

@dataclass
class Order:
    order_id: str
    amount_cents: int
    processed: bool = False
    claimed: bool = False

class OrderStore:
    def __init__(self):
        self._orders = {}
        self._lock = Lock()
    def add(self, order):
        self._orders[order.order_id] = order
    def claim(self, order_id):
        with self._lock:
            order = self._orders.get(order_id)
            if order is None or order.processed or order.claimed:
                return None
            order.claimed = True
            return order
    def release(self, order_id):
        with self._lock:
            self._orders[order_id].claimed = False
    def mark_processed(self, order_id):
        with self._lock:
            order = self._orders[order_id]
            order.processed = True
            order.claimed = False
    def is_processed(self, order_id):
        with self._lock:
            return self._orders[order_id].processed

class PaymentGateway:
    def __init__(self):
        self._lock = Lock()
        self.charges = []
    def charge(self, order_id, amount_cents):
        with self._lock:
            self.charges.append((order_id, amount_cents))

class OrderWorker:
    def __init__(self, store, gateway):
        self.store = store
        self.gateway = gateway
    def process(self, order_id):
        order = self.store.claim(order_id)
        if order is None:
            return False
        try:
            self.gateway.charge(order.order_id, order.amount_cents)
        except Exception:
            self.store.release(order.order_id)
            raise
        self.store.mark_processed(order.order_id)
        return True
''',
        encoding="utf-8",
    )
    solved = run_verifier(scenario / "verify.py", workspace)
    assert solved.returncode == 0, solved.stderr


def test_flaky_ci_investigation_requires_and_accepts_mechanism_record(tmp_path):
    scenario = EXAMPLES / "apex-investigate" / "flaky-ci-test"
    workspace = tmp_path / "workspace"
    shutil.copytree(scenario / "workspace", workspace)

    initial = run_verifier(scenario / "verify.py", workspace)
    assert initial.returncode == 1
    assert "investigation.json is missing" in initial.stderr

    record = {
        "trigger": "python-hash-seed",
        "mechanism": "unordered-set-iteration",
        "scope": "select_primary",
        "mitigation": "pin-hash-seed",
        "durable_fix": "explicit-region-priority",
        "prevention": "multi-seed-ci",
    }
    (workspace / "investigation.json").write_text(json.dumps(record), encoding="utf-8")
    solved = run_verifier(scenario / "verify.py", workspace)
    assert solved.returncode == 0, solved.stderr
