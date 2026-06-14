#!/usr/bin/env python3
"""Verify the duplicate-job example through observable behavior."""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import threading
import time
from pathlib import Path


def load_candidate(workspace: Path):
    module_path = workspace / "order_worker.py"
    spec = importlib.util.spec_from_file_location("candidate_order_worker", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_workspace_tests(workspace: Path) -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(workspace), "-p", "test*.py"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if proc.returncode:
        detail = (proc.stdout + proc.stderr).strip()
        raise AssertionError(f"workspace tests failed:\n{detail}")


def verify_competing_workers(module) -> None:
    class BlockingGateway:
        def __init__(self) -> None:
            self.entered = threading.Event()
            self.release = threading.Event()
            self.lock = threading.Lock()
            self.charges: list[tuple[str, int]] = []

        def charge(self, order_id: str, amount_cents: int) -> None:
            with self.lock:
                self.charges.append((order_id, amount_cents))
                self.entered.set()
            if not self.release.wait(timeout=5):
                raise TimeoutError("payment release was not signaled")

    store = module.OrderStore()
    store.add(module.Order("order-race", 5000))
    gateway = BlockingGateway()
    workers = [module.OrderWorker(store, gateway), module.OrderWorker(store, gateway)]
    results: list[bool] = []
    errors: list[BaseException] = []

    def process(worker) -> None:
        try:
            results.append(worker.process("order-race"))
        except BaseException as exc:
            errors.append(exc)

    first = threading.Thread(target=process, args=(workers[0],))
    second = threading.Thread(target=process, args=(workers[1],))
    first.start()
    if not gateway.entered.wait(timeout=5):
        raise AssertionError("first worker never reached the payment gateway")
    second.start()
    time.sleep(0.1)
    gateway.release.set()
    first.join(timeout=5)
    second.join(timeout=5)

    if first.is_alive() or second.is_alive():
        raise AssertionError("competing workers did not complete")
    if errors:
        raise AssertionError(f"competing workers raised: {errors!r}")
    if gateway.charges != [("order-race", 5000)]:
        raise AssertionError(f"expected one charge, observed {gateway.charges!r}")
    if sorted(results) != [False, True]:
        raise AssertionError(f"expected one worker to process the order, observed {results!r}")
    if not store.is_processed("order-race"):
        raise AssertionError("successfully charged order was not marked processed")


def verify_retry_after_failure(module) -> None:
    class FailOnceGateway:
        def __init__(self) -> None:
            self.attempts = 0

        def charge(self, order_id: str, amount_cents: int) -> None:
            self.attempts += 1
            if self.attempts == 1:
                raise RuntimeError("simulated payment failure")

    store = module.OrderStore()
    store.add(module.Order("order-retry", 3100))
    gateway = FailOnceGateway()
    worker = module.OrderWorker(store, gateway)

    try:
        worker.process("order-retry")
    except RuntimeError:
        pass
    else:
        raise AssertionError("payment failure was unexpectedly swallowed")

    if not worker.process("order-retry"):
        raise AssertionError("order was not retryable after payment failure")
    if gateway.attempts != 2 or not store.is_processed("order-retry"):
        raise AssertionError("retry did not complete the order exactly once")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", nargs="?", default=Path(__file__).parent / "workspace")
    args = parser.parse_args(argv)
    workspace = Path(args.workspace).resolve()

    try:
        run_workspace_tests(workspace)
        module = load_candidate(workspace)
        verify_competing_workers(module)
        verify_retry_after_failure(module)
    except (AssertionError, OSError, RuntimeError, TimeoutError) as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        return 1

    print("verification passed: competing workers charge once and failed payments remain retryable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
