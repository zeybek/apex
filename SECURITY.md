# Security Policy

## Reporting a vulnerability

Please do not open a public issue for security problems. Email **me@zeybek.dev** with a description, reproduction steps, and the potential impact. Expect an acknowledgement within a few business days, and a coordinated disclosure timeline of at most 90 days from the report.

## Supported versions

| Version | Supported |
|---|---|
| 0.1.x | ✅ |
| < 0.1 | ❌ |

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
- Releases are tagged; build provenance is attached to release artifacts where the CI supports it.

## Heuristic content scans

The package validator scans skill and reference text for prompt-injection signatures and high-confidence secret patterns (private keys, cloud and provider tokens). These are **best-effort gates, not guarantees**: paraphrased injections, novel phrasings, encoded payloads, or secrets in unusual formats can evade regular-expression detection. They catch obvious mistakes and lower the floor; they do not replace reviewing a skill before you install it. For background on the underlying risk, see the [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) (LLM01: Prompt Injection).
