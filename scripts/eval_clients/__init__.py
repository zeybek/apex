"""Pluggable client adapters for the apex eval harness."""

from __future__ import annotations

from .base import EvalClient, InvocationResult
from .claude_code import ClaudeCodeClient
from .stub import StubClient

_CLIENTS = {cls.name: cls for cls in (StubClient, ClaudeCodeClient)}


def available_clients():
    return sorted(_CLIENTS)


def get_client(name):
    try:
        return _CLIENTS[name]()
    except KeyError:
        raise SystemExit(
            f"unknown client {name!r}; choose from {', '.join(available_clients())}"
        ) from None


__all__ = ["EvalClient", "InvocationResult", "available_clients", "get_client"]
