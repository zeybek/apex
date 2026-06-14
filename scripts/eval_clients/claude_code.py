"""Claude Code adapter: shells `claude -p` and detects a Skill tool call.

Requires the `claude` CLI and a configured skill environment, so it is never
exercised by CI or unit tests (which use the stub). Detection follows the
agentskills.io trigger-eval pattern (a `Skill` tool_use whose `input.skill`
matches). Method bodies are marked no-cover because they need the real CLI.
"""

from __future__ import annotations

import json
import subprocess

from .base import EvalClient, InvocationResult


class ClaudeCodeClient(EvalClient):
    name = "claude-code"

    def run(self, prompt, *, skill=None, with_skill=True):  # pragma: no cover
        try:
            proc = subprocess.run(
                ["claude", "-p", prompt, "--output-format", "json"],
                capture_output=True,
                text=True,
                timeout=600,
            )
        except FileNotFoundError:
            raise RuntimeError("claude-code client requires the 'claude' CLI") from None
        except subprocess.TimeoutExpired:
            raise RuntimeError("claude-code client timed out after 600 seconds") from None
        if proc.returncode:
            detail = (proc.stderr or proc.stdout).strip()
            suffix = f": {detail[:500]}" if detail else ""
            raise RuntimeError(f"claude-code client exited with status {proc.returncode}{suffix}")
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError("claude-code client returned invalid JSON") from exc
        return InvocationResult(
            activated=_skill_invoked(data, skill) if skill else False,
            raw=_result_text(data),
            duration_ms=_dig(data, "duration_ms"),
            total_tokens=_total_tokens(data),
        )


def _messages(data):  # pragma: no cover
    if isinstance(data, dict) and isinstance(data.get("messages"), list):
        return [m for m in data["messages"] if isinstance(m, dict)]
    if isinstance(data, list):
        return [m for m in data if isinstance(m, dict)]
    return []


def _skill_invoked(data, skill):  # pragma: no cover
    for message in _messages(data):
        for block in message.get("content", []) or []:
            if (
                isinstance(block, dict)
                and block.get("type") == "tool_use"
                and block.get("name") == "Skill"
                and str(block.get("input", {}).get("skill", "")).endswith(skill)
            ):
                return True
    return False


def _result_text(data):  # pragma: no cover
    if isinstance(data, dict) and isinstance(data.get("result"), str):
        return data["result"]
    return json.dumps(data)[:4000]


def _total_tokens(data):  # pragma: no cover
    usage = data.get("usage") if isinstance(data, dict) else None
    if isinstance(usage, dict):
        return (usage.get("input_tokens") or 0) + (usage.get("output_tokens") or 0)
    return None


def _dig(data, key):  # pragma: no cover
    return data.get(key) if isinstance(data, dict) else None
