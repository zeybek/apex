"""Client adapters for the apex eval harness.

An adapter runs one prompt through some agent client and reports whether a
skill activated plus optional usage. Adapters are read-only with respect to
skills and never imported by the runtime validators.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InvocationResult:
    """Outcome of running one prompt through a client."""

    activated: bool
    raw: str = ""
    duration_ms: int | None = None
    total_tokens: int | None = None


class EvalClient:
    """Base adapter. Subclasses run a prompt and report activation + usage."""

    name = "base"

    def run(
        self, prompt: str, *, skill: str | None = None, with_skill: bool = True
    ) -> InvocationResult:
        raise NotImplementedError
