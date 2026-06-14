#!/usr/bin/env python3
"""Validate the portable skill package without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "plugins" / "apex" / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
VENDOR_TERMS = re.compile(
    r"\b(?:Codex|Claude|Anthropic|OpenAI|ChatGPT|GPT|Copilot|Gemini|"
    r"OpenCode|Antigravity)\b"
)
PLACEHOLDER_TERMS = re.compile(r"TODO|\[TODO|Structuring This Skill")
INJECTION_PATTERNS = re.compile(
    r"ignore\s+(?:all\s+|any\s+|the\s+)*(?:previous|prior|earlier|above|preceding)\s+"
    r"(?:instruction|prompt|message|context|rule)s?"
    r"|disregard\s+(?:all\s+|any\s+|the\s+)*(?:previous|prior|earlier|above|system)\s+"
    r"(?:instruction|prompt|message|rule)s?"
    r"|forget\s+(?:all\s+|everything\s+|your\s+)*(?:previous|prior|above|earlier)\s+"
    r"(?:instruction|context|message)s?"
    r"|(?:reveal|print|repeat|expose|leak)\s+(?:your|the)\s+"
    r"(?:full\s+|entire\s+|hidden\s+)*(?:system\s+)?(?:prompt|instruction)s?"
    r"|override\s+(?:the\s+|your\s+)*(?:system\s+)?(?:instruction|prompt|rule)s?"
    r"|do\s+not\s+(?:tell|inform|notify|reveal\s+to)\s+the\s+(?:user|human|operator)"
    r"|exfiltrate",
    re.IGNORECASE,
)
SECRET_PATTERNS = re.compile(
    r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"
    r"|\bAKIA[0-9A-Z]{16}\b"
    r"|\bgh[a-z]_[A-Za-z0-9]{36,}\b"
    r"|\bxox[baprs]-[A-Za-z0-9-]{10,}\b"
    r"|\bsk-[A-Za-z0-9]{20,}\b"
)


def error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def parse_frontmatter(path: Path, errors: list[str]) -> tuple[dict[str, str], str]:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        error(errors, path, f"cannot read as UTF-8: {exc}")
        return {}, ""

    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        error(errors, path, "missing or malformed YAML frontmatter")
        return {}, content

    fields: dict[str, str] = {}
    for line_number, line in enumerate(match.group(1).splitlines(), start=2):
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            error(errors, path, f"invalid top-level frontmatter line {line_number}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("\"'")

    return fields, content[match.end() :]


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        error(errors, skill_dir, "SKILL.md is missing")
        return

    fields, body = parse_frontmatter(skill_file, errors)
    unknown = sorted(set(fields) - ALLOWED_FRONTMATTER)
    if unknown:
        error(errors, skill_file, f"unknown frontmatter fields: {', '.join(unknown)}")

    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        error(errors, skill_file, "name is required")
    elif not NAME_PATTERN.fullmatch(name):
        error(errors, skill_file, "name must use lowercase alphanumeric hyphen-case")
    elif len(name) > 64:
        error(errors, skill_file, "name exceeds 64 characters")
    elif name != skill_dir.name:
        error(errors, skill_file, f"name '{name}' does not match directory '{skill_dir.name}'")

    if not description:
        error(errors, skill_file, "description is required")
    elif len(description) > 1024:
        error(errors, skill_file, "description exceeds 1024 characters")
    elif "Use this skill" not in description:
        error(
            errors,
            skill_file,
            "description must contain the literal phrase 'Use this skill' "
            "(project convention) so activation guidance is explicit",
        )

    compatibility = fields.get("compatibility")
    if compatibility is not None and not 1 <= len(compatibility) <= 500:
        error(errors, skill_file, "compatibility must be 1-500 characters when present")

    allowed_tools = fields.get("allowed-tools")
    if allowed_tools is not None and not allowed_tools.strip():
        error(
            errors,
            skill_file,
            "allowed-tools must be a non-empty space-separated string when present",
        )

    body_lines = body.count("\n") + 1
    if body_lines > 500:
        error(errors, skill_file, f"body has {body_lines} lines; keep it under 500")
    estimated_tokens = len(body) // 4
    if estimated_tokens > 5000:
        error(
            errors,
            skill_file,
            f"body is ~{estimated_tokens} estimated tokens; keep it under 5000",
        )

    if VENDOR_TERMS.search(skill_file.read_text(encoding="utf-8")):
        error(errors, skill_file, "portable core contains a client-specific product name")

    validate_skill_links(skill_file, errors)
    validate_injection_signatures(skill_dir, errors)
    validate_secret_signatures(skill_dir, errors)
    validate_evals(skill_dir, name, errors)


def validate_skill_links(skill_file: Path, errors: list[str]) -> None:
    content = skill_file.read_text(encoding="utf-8")
    for raw_target in MARKDOWN_LINK_PATTERN.findall(content):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target_path = unquote(target.split("#", 1)[0].split("?", 1)[0])
        parts = Path(target_path).parts
        if ".." in parts:
            error(errors, skill_file, f"reference escapes the skill directory: {target}")
            continue
        if len(parts) > 2:
            error(errors, skill_file, f"reference is more than one level deep: {target}")
        resolved = skill_file.parent / target_path
        if not resolved.exists():
            error(errors, skill_file, f"referenced file does not exist: {target}")


def validate_injection_signatures(skill_dir: Path, errors: list[str]) -> None:
    """Flag prompt-injection signatures in skill or reference text.

    Skill content is loaded into an agent verbatim, so instruction text that
    tries to override the agent's task is a supply-chain risk, not prose.
    """
    for path in sorted(skill_dir.rglob("*.md")):
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        match = INJECTION_PATTERNS.search(content)
        if match:
            snippet = " ".join(match.group(0).split())
            error(errors, path, f"contains a prompt-injection signature: {snippet!r}")


def validate_secret_signatures(skill_dir: Path, errors: list[str]) -> None:
    """Flag high-confidence committed-secret patterns in skill or reference text.

    A best-effort gate against pasted credentials, not a guarantee. The matched
    text is never echoed, so the error message cannot leak the secret itself.
    """
    for path in sorted(skill_dir.rglob("*.md")):
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if SECRET_PATTERNS.search(content):
            error(errors, path, "contains what looks like a committed secret or credential")


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        error(errors, path, f"invalid JSON: {exc}")
        return None


def validate_evals(skill_dir: Path, skill_name: str, errors: list[str]) -> None:
    evals_dir = skill_dir / "evals"
    trigger_file = evals_dir / "trigger-evals.json"
    output_file = evals_dir / "evals.json"

    triggers = load_json(trigger_file, errors) if trigger_file.is_file() else None
    if triggers is None:
        if not trigger_file.is_file():
            error(errors, trigger_file, "trigger eval file is missing")
    elif not isinstance(triggers, list):
        error(errors, trigger_file, "root must be a JSON array")
    else:
        if len(triggers) < 20:
            error(errors, trigger_file, "include at least 20 trigger queries")
        queries: set[str] = set()
        labels = {True: 0, False: 0}
        for index, case in enumerate(triggers):
            if not isinstance(case, dict):
                error(errors, trigger_file, f"case {index} must be an object")
                continue
            query = case.get("query")
            should_trigger = case.get("should_trigger")
            if not isinstance(query, str) or not query.strip():
                error(errors, trigger_file, f"case {index} needs a non-empty query")
            elif query in queries:
                error(errors, trigger_file, f"duplicate query at case {index}")
            else:
                queries.add(query)
            if not isinstance(should_trigger, bool):
                error(errors, trigger_file, f"case {index} needs a boolean should_trigger")
            else:
                labels[should_trigger] += 1
        if labels[True] < 8 or labels[False] < 8:
            error(errors, trigger_file, "include at least 8 positive and 8 negative queries")

    output_evals = load_json(output_file, errors) if output_file.is_file() else None
    if output_evals is None:
        if not output_file.is_file():
            error(errors, output_file, "output eval file is missing")
        return
    if not isinstance(output_evals, dict):
        error(errors, output_file, "root must be a JSON object")
        return
    if output_evals.get("skill_name") != skill_name:
        error(errors, output_file, "skill_name must match SKILL.md name")
    cases = output_evals.get("evals")
    if not isinstance(cases, list) or len(cases) < 3:
        error(errors, output_file, "include at least 3 output eval cases")
        return
    ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            error(errors, output_file, f"case {index} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            error(errors, output_file, f"case {index} needs a non-empty id")
        elif case_id in ids:
            error(errors, output_file, f"duplicate id '{case_id}'")
        else:
            ids.add(case_id)
        for field in ("prompt", "expected_output"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                error(errors, output_file, f"case {index} needs non-empty {field}")
        assertions = case.get("assertions")
        if (
            not isinstance(assertions, list)
            or len(assertions) < 3
            or not all(isinstance(item, str) and item.strip() for item in assertions)
        ):
            error(errors, output_file, f"case {index} needs at least 3 assertions")


def validate_all_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        content = path.read_text(encoding="utf-8")
        if PLACEHOLDER_TERMS.search(content):
            error(errors, path, "contains a template placeholder")
        for raw_target in MARKDOWN_LINK_PATTERN.findall(content):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not (path.parent / target_path).exists():
                error(errors, path, f"local link does not resolve: {target}")


def main() -> int:
    errors: list[str] = []
    skill_dirs = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("skills: no skill directories found")
    for skill_dir in skill_dirs:
        validate_skill(skill_dir, errors)
    validate_all_markdown_links(errors)

    if errors:
        print(f"Validation failed with {len(errors)} problem(s):", file=sys.stderr)
        for problem in errors:
            print(f"- {problem}", file=sys.stderr)
        return 1

    trigger_count = sum(
        len(json.loads((skill / "evals" / "trigger-evals.json").read_text()))
        for skill in skill_dirs
    )
    output_count = sum(
        len(json.loads((skill / "evals" / "evals.json").read_text())["evals"])
        for skill in skill_dirs
    )
    print(
        f"Validated {len(skill_dirs)} skills, {trigger_count} trigger cases, "
        f"and {output_count} output evals."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
