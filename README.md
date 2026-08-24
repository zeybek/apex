# Apex

[![CI](https://github.com/zeybek/apex/actions/workflows/ci.yml/badge.svg)](https://github.com/zeybek/apex/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/zeybek/apex/badge)](https://securityscorecards.dev/viewer/?uri=github.com/zeybek/apex)
[![Release](https://img.shields.io/github/v/release/zeybek/apex?sort=semver)](https://github.com/zeybek/apex/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/13227/badge)](https://www.bestpractices.dev/projects/13227)

Apex gives your coding agent senior-engineering judgment for designing, implementing, reviewing, and investigating software changes. It ships as open [Agent Skills](https://agentskills.io/) that are language- and framework-agnostic and run in any skills-compatible agent — with ready-to-install plugins for Claude Code and Codex.

Four focused skills activate only when the task calls for them, alongside two planning-workspace hooks, two read-only agents, and an optional always-on engineering constitution. Repository: [github.com/zeybek/apex](https://github.com/zeybek/apex).

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

Or install the skills directly with the [GitHub CLI](https://cli.github.com/) (`gh skill`, in preview), which targets Claude Code, Codex, Cursor, Gemini CLI, and many other agents:

```bash
# All four skills into the current project
gh skill install zeybek/apex --all

# Or for a specific agent, at user scope (available everywhere)
gh skill install zeybek/apex --all --agent claude-code --scope user
```

Or with the [skills.sh](https://www.skills.sh/) CLI:

```bash
npx skills add zeybek/apex
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

## Commands and the planning workspace

In Claude Code, each skill is also a slash command, so a single-line request can drive the full workflow:

| Command | What it does |
|---|---|
| `/apex-design <request>` | Ask clarifying questions, settle the domain vocabulary, and write a committed `.apex-design/<slug>/` planning workspace — even from a one-line brief |
| `/apex-implement [slug]` | Execute the plan task by task, verify each, and keep its progress board current |
| `/apex-progress [slug]` | Report status across `.apex-design/` initiatives: done, in progress, blocked, and what is next |
| `/apex-review <target>` | Risk-first review, checked against the initiative's recorded design and requirements when present |
| `/apex-investigate <symptom>` | Diagnose a failure to a root cause, using the recorded design as the intended-behavior baseline |

`/apex-design` turns even "build me a landing page" into a deliberate plan: it discovers what the repository already answers, asks only the decisions it cannot infer, and persists a `.apex-design/<NNN-slug>/` folder with a brief, glossary, requirements, design, plan, and progress board, scaled to the risk of the work. Stable identifiers — `D-` decisions, `R-` requirements, `T-` tasks — connect the reasoning across files, and the glossary pins the domain terms (per context, with forbidden synonyms) that every later file and the generated code must use. The design opens with a short decision digest that the decision owner confirms before implementation starts, so the plan is something the team has read rather than an artifact the agent produced. `/apex-implement` then executes that plan, keeps the progress board current, and closes with an owner handoff — the few things a person must understand to change the result safely — while review and investigation read the same workspace as shared context. The workspace is committed alongside the code as living project documentation.

Other skills-compatible clients drive the same workflow through skill activation rather than slash commands; the resulting `.apex-design/` workspace is identical.

## Hooks: the workspace follows you into every session

Two small hooks keep the `.apex-design/` workspace alive across sessions. Both are standard-library Python scripts shipped in `plugins/apex/hooks/`, read-only, offline, and silent when there is no workspace.

| Hook | When | What it does |
|---|---|---|
| `apex_session_context.py` | `SessionStart` (new, resumed, cleared, or compacted session) | Prints the active initiative's decision digest, glossary (the names to use, the synonyms to avoid), decision owner and domain expert, current position, and next pending task, so the agent starts with the team's model in context instead of rediscovering it. |
| `apex_stop_guard.py` | `Stop` | If an initiative is `in progress`, the working tree changed outside `.apex-design/`, and that initiative's `progress.md` was not touched, it blocks the stop once with a reason, so the progress board and owner handoff get written before the turn ends. It never blocks twice in a row, never blocks outside a git repository, and never writes. |

Claude Code runs plugin hooks once the plugin is enabled; Codex asks you to review and trust each plugin hook before it runs (see [adapters/README.md](adapters/README.md)). Both hooks need `python3` on `PATH`; without it they exit quietly.

## Agents: review and diagnosis in an isolated context

Two subagents (Claude Code) run the review and investigation workflows in a separate context that cannot edit files:

| Agent | Preloads | Tools |
|---|---|---|
| `apex:apex-reviewer` | `apex-review` | Read, Grep, Glob, Bash (read-only use) — no Write or Edit |
| `apex:apex-investigator` | `apex-investigate` | Read, Grep, Glob, Bash (read-only use) — no Write or Edit |

Delegate to them when you want a review that does not share the implementing session's assumptions, or a diagnosis kept separate from the fix. Their reports come back as findings or an evidence chain for the main session (or `/apex-implement`) to act on.

## Examples

[`examples/`](examples/README.md) contains one client-neutral walkthrough for each skill. The implement and investigate walkthroughs include small standard-library workspaces plus deterministic verifier scripts, so you can exercise the workflow without changing the canonical example files.

## Design principles

- Optimize for correct, useful, maintainable software and safe delivery.
- Prefer the simplest solution only after requirements and risk controls are satisfied.
- Scale rigor with blast radius, reversibility, criticality, exposure, persistence, concurrency, compatibility, operability, and uncertainty.
- Treat security, privacy, testing, observability, migrations, rollout, and recovery as engineering work, not optional follow-up.
- Preserve project conventions and contracts unless evidence justifies changing them.
- Model the domain before the mechanism: use the project's vocabulary, keep separately named concepts separate, involve the people who know the business, and leave the owners understanding the result rather than only holding a document about it.

## Always-on constitution

`AGENTS.md` is a compact engineering constitution that sits outside the skill specification. Merge it into your client's always-on instruction file (`AGENTS.md`, `CLAUDE.md`, or equivalent) when its rules should apply to every task, independently of whether the skills are active. See [adapters/README.md](adapters/README.md) for per-client setup.

## Packaging

The same `plugins/apex/skills/` directory backs every client; the client-specific manifests carry distribution metadata only and never duplicate skill instructions.

- `plugins/apex/` — the portable plugin package (`SKILL.md`, `references/`, and `evals/` per skill);
- `plugins/apex/commands/` — Claude Code slash-command wrappers (`/apex-design`, `/apex-implement`, `/apex-progress`, `/apex-review`, `/apex-investigate`) that pass arguments to the matching skill; they carry distribution-side phrasing only and never duplicate skill instructions;
- `plugins/apex/hooks/` — `hooks.json` plus the two standard-library hook scripts, loaded by Claude Code and Codex;
- `plugins/apex/agents/` — the read-only reviewer and investigator subagents (Claude Code);
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

The dependency-free validators check skill structure, frontmatter constraints, local references, progressive-disclosure limits, platform-neutral content, eval schemas, hook definitions (known events, command-only, every command runs a script that ships with the plugin), agent frontmatter, plugin manifests, and marketplace catalogs. To also validate the core format against the official reference implementation (requires network access):

```bash
make validate-official
```

This pins a specific `skills-ref` commit for reproducibility. `skills-ref` is a reference implementation rather than a production validator, so the local checks remain the stable package gate.

## Security

Apex skills are instructions, not executable code. The only executable parts of the installed plugin are the two hook scripts under `plugins/apex/hooks/`: standard-library Python that reads the working directory's `.apex-design/` and `git status`, prints text, makes no network calls, and reads no credentials; the package validator rejects any hook that is not a command running a script shipped inside the plugin. The repository also contains two dependency-free offline validators and a developer-run eval harness that can explicitly invoke a configured agent client. The package validator scans skill and reference text for prompt-injection signatures, so instruction content cannot quietly redirect an agent. See [SECURITY.md](SECURITY.md) for how to report an issue, [docs/ASSURANCE_CASE.md](docs/ASSURANCE_CASE.md) for the threat model and the argument that the security requirements hold, and [docs/RELEASING.md](docs/RELEASING.md) for how to verify a signed, provenance-attested release.

## Project documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — what the package, the tooling, and the release pipeline consist of and how they connect.
- [docs/CODE_REVIEW.md](docs/CODE_REVIEW.md) — what every change is reviewed for and what makes it acceptable.
- [GOVERNANCE.md](GOVERNANCE.md) — roles, decision making, and access continuity.
- [ROADMAP.md](ROADMAP.md) — what the project intends to do and not do.

## Foundations

The engineering guidance is consistent with established software-engineering practice rather than derived from any single methodology. Each reference file lists the specific sources it draws on under its "Foundational Sources" section — including IEEE SWEBOK, NIST SSDF, OWASP ASVS, SEI quality-attribute methods, Google SRE, WCAG, the strategic patterns of Domain-Driven Design (Ubiquitous Language, Bounded Context), and Naur's theory-building view of programming, among others. The packaging and evaluation approach follows the [Agent Skills specification](https://agentskills.io/specification.md), [best practices](https://agentskills.io/skill-creation/best-practices.md), and [evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills.md).
