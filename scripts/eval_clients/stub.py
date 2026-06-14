"""Deterministic, offline client for exercising the harness without a model.

No network or model calls. Activation is a keyword heuristic and usage is
derived from a hash of the prompt, so runs are fully reproducible. It exercises
the runner's logic (splitting, rate maths, schema emission) — not real model
accuracy. CI and unit tests use this client.
"""

from __future__ import annotations

import hashlib

from .base import EvalClient, InvocationResult


class StubClient(EvalClient):
    name = "stub"

    def run(self, prompt, *, skill=None, with_skill=True):
        activated = False
        if skill and with_skill:
            stem = skill.rsplit("-", 1)[-1]
            activated = stem in prompt.lower()
        digest = int(hashlib.sha256(prompt.encode("utf-8")).hexdigest(), 16)
        label = "with-skill" if with_skill else "baseline"
        return InvocationResult(
            activated=activated,
            raw=f"[stub:{label}] {prompt[:60]}",
            duration_ms=1000 + digest % 4000,
            total_tokens=400 + digest % 1200,
        )
