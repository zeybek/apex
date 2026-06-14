# Apex

[![CI](https://github.com/zeybek/apex/actions/workflows/ci.yml/badge.svg)](https://github.com/zeybek/apex/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/zeybek/apex/badge)](https://securityscorecards.dev/viewer/?uri=github.com/zeybek/apex)
[![Release](https://img.shields.io/github/v/release/zeybek/apex?sort=semver)](https://github.com/zeybek/apex/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
<!-- OpenSSF Best Practices: register the repo at https://www.bestpractices.dev
     (sign in with GitHub, then add github.com/zeybek/apex), replace NNNN with the
     assigned project ID, and uncomment the badge below.
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/NNNN/badge)](https://www.bestpractices.dev/projects/NNNN)
-->

Apex gives your coding agent senior-engineering judgment for designing, implementing, reviewing, and investigating software changes. It ships as open [Agent Skills](https://agentskills.io/) that are language- and framework-agnostic and run in any skills-compatible agent — with ready-to-install plugins for Claude Code and Codex.

Four focused skills activate only when the task calls for them, alongside an optional always-on engineering constitution. Repository: [github.com/zeybek/apex](https://github.com/zeybek/apex).

## Install

Install the published package for your client:

```bash
# Claude Code
claude plugin marketplace add zeybek/apex
claude plugin install apex@apex

# Codex
codex plugin marketplace add zeybek/apex
codex plugin add apex@apex
```

For local development, point the marketplace at a path instead of `zeybek/apex`, then install with the same `apex@apex` commands:

```bash
claude plugin marketplace add <repository-path>
codex plugin marketplace add <repository-path>
```

Using another skills-compatible agent (Cursor, OpenCode, Gemini CLI, and others)? See [adapters/README.md](adapters/README.md) for discovery paths and copy/symlink installation.

## Skills

| Skill | Use it to |
|---|---|
| `apex-design` | Make architecture, API, schema, migration, and build-versus-buy decisions |
| `apex-implement` | Implement features, fixes, refactors, migrations, and production changes end to end |
| `apex-review` | Run risk-first reviews with actionable findings by severity |
| `apex-investigate` | Diagnose incidents, regressions, flaky failures, and unknown-cause bugs before fixing |

Each skill is a `SKILL.md` workflow under `plugins/apex/skills/`; deeper guidance lives in `references/` and loads only when relevant. Keeping the workflows separate keeps each one focused and lets only the relevant skill enter context.

## Examples

[`examples/`](examples/README.md) contains one client-neutral walkthrough for each skill. The implement and investigate walkthroughs include small standard-library workspaces plus deterministic verifier scripts, so you can exercise the workflow without changing the canonical example files.

## Design principles

- Optimize for correct, useful, maintainable software and safe delivery.
- Prefer the simplest solution only after requirements and risk controls are satisfied.
- Scale rigor with blast radius, reversibility, criticality, exposure, persistence, concurrency, compatibility, operability, and uncertainty.
- Treat security, privacy, testing, observability, migrations, rollout, and recovery as engineering work, not optional follow-up.
- Preserve project conventions and contracts unless evidence justifies changing them.

## Always-on constitution

`AGENTS.md` is a compact engineering constitution that sits outside the skill specification. Merge it into your client's always-on instruction file (`AGENTS.md`, `CLAUDE.md`, or equivalent) when its rules should apply to every task, independently of whether the skills are active. See [adapters/README.md](adapters/README.md) for per-client setup.

## Packaging

The same `plugins/apex/skills/` directory backs every client; the client-specific manifests carry distribution metadata only and never duplicate skill instructions.

- `plugins/apex/` — the portable plugin package (`SKILL.md`, `references/`, and `evals/` per skill);
- `plugins/apex/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — Claude Code packaging and marketplace;
- `plugins/apex/.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` — Codex packaging and marketplace.

Codex install-surface UI metadata (display name, descriptions, default prompts) lives in the `.codex-plugin/plugin.json` `interface` block, not in the skill folders.

## Evaluation

Every skill ships its own evals:

- `evals/trigger-evals.json` — realistic positive and near-miss negative prompts for activation accuracy;
- `evals/evals.json` — output-quality scenarios with expected outcomes and observable assertions.

Run them in clean sessions and compare `with_skill` against a `baseline` (no skill, or a previous version). The repository includes a dependency-light runner for prompt execution, activation measurement, and grading scaffolds; output-quality grading remains manual. [evals/README.md](evals/README.md) describes the protocol, and recorded comparison runs belong in [benchmarks/](benchmarks/README.md).

## Validation

```bash
make validate
```

The dependency-free validators check skill structure, frontmatter constraints, local references, progressive-disclosure limits, platform-neutral content, eval schemas, plugin manifests, and marketplace catalogs. To also validate the core format against the official reference implementation (requires network access):

```bash
make validate-official
```

This pins a specific `skills-ref` commit for reproducibility. `skills-ref` is a reference implementation rather than a production validator, so the local checks remain the stable package gate.

## Security

Apex skills are instructions, not executable code. The installed plugin is Markdown and JSON and does not execute code, make network calls, or read credentials on its own. The repository also contains two dependency-free offline validators and a developer-run eval harness that can explicitly invoke a configured agent client. The package validator scans skill and reference text for prompt-injection signatures, so instruction content cannot quietly redirect an agent. See [SECURITY.md](SECURITY.md) for the threat model and how to report an issue.

## Foundations

The engineering guidance is consistent with established software-engineering practice rather than derived from any single methodology. Each reference file lists the specific sources it draws on under its "Foundational Sources" section — including IEEE SWEBOK, NIST SSDF, OWASP ASVS, SEI quality-attribute methods, Google SRE, and WCAG, among others. The packaging and evaluation approach follows the [Agent Skills specification](https://agentskills.io/specification.md), [best practices](https://agentskills.io/skill-creation/best-practices.md), and [evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills.md).
