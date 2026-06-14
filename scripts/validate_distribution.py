#!/usr/bin/env python3
"""Validate cross-client plugin manifests and marketplace catalogs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "apex"
PLUGIN_ROOT = ROOT / "plugins" / PLUGIN_NAME
REPOSITORY_URL = "https://github.com/zeybek/apex"
RELEASE_MANIFEST_PATH = ROOT / ".release-please-manifest.json"
SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def load_object(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: root must be a JSON object")
        return {}
    return value


def require_equal(errors: list[str], label: str, actual, expected) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, found {actual!r}")


def require_subset(errors: list[str], label: str, actual, expected: dict) -> None:
    """Require every expected key/value to be present, allowing extra keys."""
    if not isinstance(actual, dict):
        errors.append(f"{label}: expected an object, found {actual!r}")
        return
    for key, value in expected.items():
        if actual.get(key) != value:
            errors.append(f"{label}.{key}: expected {value!r}, found {actual.get(key)!r}")


def find_plugin(catalog: dict, path: Path, errors: list[str]) -> dict:
    plugins = catalog.get("plugins")
    if not isinstance(plugins, list):
        errors.append(f"{path.relative_to(ROOT)}: plugins must be an array")
        return {}
    matches = [
        plugin
        for plugin in plugins
        if isinstance(plugin, dict) and plugin.get("name") == PLUGIN_NAME
    ]
    if len(matches) != 1:
        errors.append(f"{path.relative_to(ROOT)}: expected exactly one {PLUGIN_NAME!r} entry")
        return {}
    return matches[0]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate plugin distribution manifests.")
    parser.add_argument(
        "--tag",
        help="release tag (for example v0.1.1) to assert against the manifest version",
    )
    options = parser.parse_args(argv)

    errors: list[str] = []
    codex_manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    claude_manifest_path = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
    codex_marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    claude_marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"

    codex_manifest = load_object(codex_manifest_path, errors)
    claude_manifest = load_object(claude_manifest_path, errors)
    codex_marketplace = load_object(codex_marketplace_path, errors)
    claude_marketplace = load_object(claude_marketplace_path, errors)

    for label, manifest in (
        ("Codex plugin name", codex_manifest),
        ("Claude plugin name", claude_manifest),
        ("Codex marketplace name", codex_marketplace),
        ("Claude marketplace name", claude_marketplace),
    ):
        require_equal(errors, label, manifest.get("name"), PLUGIN_NAME)

    claude_owner = claude_marketplace.get("owner")
    if not isinstance(claude_owner, dict) or not claude_owner.get("name"):
        errors.append(
            f"{claude_marketplace_path.relative_to(ROOT)}: "
            "top-level 'owner' must be an object with a name"
        )

    codex_interface = codex_marketplace.get("interface")
    if not isinstance(codex_interface, dict) or not codex_interface.get("displayName"):
        errors.append(
            f"{codex_marketplace_path.relative_to(ROOT)}: 'interface.displayName' is required"
        )

    versions = {
        codex_manifest.get("version"),
        claude_manifest.get("version"),
    }
    if len(versions) != 1 or not all(
        isinstance(version, str) and SEMVER_PATTERN.fullmatch(version) for version in versions
    ):
        errors.append("plugin manifests must use the same stable semantic version")

    manifest_version = claude_manifest.get("version")

    if RELEASE_MANIFEST_PATH.exists():
        release_manifest = load_object(RELEASE_MANIFEST_PATH, errors)
        tracked = release_manifest.get(".")
        if tracked != manifest_version:
            errors.append(
                f".release-please-manifest.json version {tracked!r} does not match "
                f"plugin manifest version {manifest_version!r}"
            )

    if options.tag:
        expected = options.tag.lstrip("v")
        if expected != manifest_version:
            errors.append(
                f"release tag {options.tag!r} does not match manifest version {manifest_version!r}"
            )

    require_equal(
        errors,
        "Codex skills path",
        codex_manifest.get("skills"),
        "./skills/",
    )
    for label, manifest in (
        ("Codex plugin", codex_manifest),
        ("Claude plugin", claude_manifest),
    ):
        require_equal(errors, f"{label} homepage", manifest.get("homepage"), REPOSITORY_URL)
        require_equal(
            errors,
            f"{label} repository",
            manifest.get("repository"),
            REPOSITORY_URL,
        )

    codex_entry = find_plugin(codex_marketplace, codex_marketplace_path, errors)
    require_subset(
        errors,
        "Codex marketplace source",
        codex_entry.get("source"),
        {"source": "local", "path": "./plugins/apex"},
    )
    require_subset(
        errors,
        "Codex marketplace policy",
        codex_entry.get("policy"),
        {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    )

    claude_entry = find_plugin(claude_marketplace, claude_marketplace_path, errors)
    require_equal(
        errors,
        "Claude marketplace source",
        claude_entry.get("source"),
        "./plugins/apex",
    )

    if errors:
        print(f"Distribution validation failed with {len(errors)} problem(s):", file=sys.stderr)
        for problem in errors:
            print(f"- {problem}", file=sys.stderr)
        return 1

    print("Validated Codex and Claude plugin manifests and marketplace catalogs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
