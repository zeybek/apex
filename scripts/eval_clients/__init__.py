# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmet Zeybek and the Apex contributors
"""Pluggable client adapters for the apex eval harness."""

from __future__ import annotations

from .base import EvalClient, InvocationResult
from .claude_code import ClaudeCodeClient
from .stub import StubClient

_CLIENTS: dict[str, type[EvalClient]] = {cls.name: cls for cls in (StubClient, ClaudeCodeClient)}


def available_clients() -> list[str]:
    return sorted(_CLIENTS)


def get_client(name: str) -> EvalClient:
    try:
        return _CLIENTS[name]()
    except KeyError:
        raise SystemExit(
            f"unknown client {name!r}; choose from {', '.join(available_clients())}"
        ) from None


__all__ = ["EvalClient", "InvocationResult", "available_clients", "get_client"]
