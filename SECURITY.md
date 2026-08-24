# Security Policy

## Reporting a vulnerability

Please do not open a public issue for security problems. Use either channel:

- [GitHub private vulnerability reporting](https://github.com/zeybek/apex/security/advisories/new) (preferred; visible to both maintainers), or
- email **me@zeybek.dev**

with a description, reproduction steps, and the potential impact.

## Response process

1. **Acknowledge** within a few business days.
2. **Triage** severity and scope; confirm or ask for more detail.
3. **Fix** on a private branch when disclosure would put users at risk, otherwise in the open; release the fix as a patch release through the normal automated pipeline.
4. **Disclose** in the release notes (CHANGELOG.md and the GitHub Release), crediting the reporter unless they ask to stay anonymous, within at most 90 days of the report.

## Supported versions

Only the latest minor release line receives fixes; upgrade to the newest release to receive them.

| Version | Supported |
|---|---|
| 0.4.x | ✅ |
| < 0.4 | ❌ |

## Threat model and scope

Apex skills are **instructions, not executable code**. The installed plugin under `plugins/apex/` contains Markdown (`SKILL.md`, `references/`) plus JSON manifests and evals. The skills do not execute code, make network calls, or read credentials on their own; any such action is performed by the host agent under its own permissions.

The repository also contains two dependency-free Python validators that run offline and a developer-run eval harness. The harness uses an offline stub by default, but its `claude-code` client explicitly shells a configured host-agent CLI when selected.

In scope:

- skill or reference content that could lead an agent to take an unintended or unsafe action, including text that tries to override the agent's current task;
- plugin/marketplace manifests with incorrect or unsafe metadata;
- defects in the Python validators or eval harness (unsafe parsing, incorrect gating, or misleading benchmark output).

Out of scope:

- vulnerabilities in the host agent (Claude Code, Codex, or another client) — report those to the respective vendor;
- the user's own environment, repository, or model configuration.

## What you can rely on

- The validators are standard-library only and can be reviewed and run offline.
- Releases are tagged, signed with cosign (keyless Sigstore), and attested with SLSA build provenance; [docs/RELEASING.md](docs/RELEASING.md) shows how to verify an archive.
- The full argument for why these requirements hold, with threat model and trust boundaries, is in [docs/ASSURANCE_CASE.md](docs/ASSURANCE_CASE.md).

## Heuristic content scans

The package validator scans skill and reference text for prompt-injection signatures and high-confidence secret patterns (private keys, cloud and provider tokens). These are **best-effort gates, not guarantees**: paraphrased injections, novel phrasings, encoded payloads, or secrets in unusual formats can evade regular-expression detection. They catch obvious mistakes and lower the floor; they do not replace reviewing a skill before you install it. For background on the underlying risk, see the [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (LLM01: Prompt Injection).
