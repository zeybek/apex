# Architecture

Apex is a documentation-shaped product with a small amount of tooling around it. This page describes the pieces, how they relate, and the flows that connect them, so a reader can reason about a change before making it.

## What the project produces

The deliverable is the **portable plugin package** under `plugins/apex/`:

```text
plugins/apex/
  skills/<name>/SKILL.md          the skill: frontmatter (name, description) + workflow
  skills/<name>/references/*.md   on-demand depth, loaded only when SKILL.md says to
  skills/<name>/evals/            trigger-evals.json and evals.json for that skill
  commands/*.md                   Claude Code slash-command wrappers (distribution-side phrasing only)
  hooks/hooks.json                SessionStart and Stop hooks (Claude Code and Codex)
  hooks/*.py                      the hook scripts: standard-library, read-only
  agents/*.md                     read-only reviewer and investigator subagents (Claude Code)
  .claude-plugin/plugin.json      Claude Code packaging metadata
  .codex-plugin/plugin.json       Codex packaging metadata and install-surface UI text
```

Everything a host agent loads is Markdown or JSON, except the two hook scripts, which are standard-library Python that read the workspace and `git status` and print text. Nothing in the package makes network calls or reads credentials; whatever an agent does with the instructions happens under the host's own permissions. That fact drives the security model in [ASSURANCE_CASE.md](ASSURANCE_CASE.md).

The four skills — `apex-design`, `apex-implement`, `apex-review`, `apex-investigate` — share one artifact: the `.apex-design/<NNN-slug>/` **planning workspace** that `apex-design` writes into a user's repository and the other three read (brief, glossary, requirements, design, plan, progress). It is the only coupling between skills, and it is a documented file layout rather than code. The hooks read the same layout: `apex_session_context.py` renders the active initiative's digest, glossary, position, and next task into context at session start, and `apex_stop_guard.py` refuses to end a turn that changed code while an in-progress initiative's `progress.md` stayed untouched. The two agents preload `apex-review` and `apex-investigate` and run them with file-editing tools removed.

## Distribution surfaces

The same `plugins/apex/skills/` directory backs every client:

- **Claude Code** installs the package through `.claude-plugin/marketplace.json` at the repository root.
- **Codex** installs it through `.agents/plugins/marketplace.json`.
- **Other Agent-Skills clients** copy or symlink the skill directories into their discovery path ([../adapters/README.md](../adapters/README.md)).
- **Releases** ship `apex-X.Y.Z.tar.gz`, a tarball of `plugins/apex`, signed and attested (see [RELEASING.md](RELEASING.md)).

Client manifests carry distribution metadata only and never duplicate skill instructions; `scripts/validate_distribution.py` enforces that they agree with each other and with the release manifest.

## Tooling (not shipped)

```text
scripts/
  validate_package.py        skill structure, frontmatter, size limits, link targets,
                             platform-neutral wording, prompt-injection and secret
                             signatures, eval-file shape          (standard library only)
  validate_distribution.py   plugin manifests, marketplace catalogs, version agreement
  run_evals.py               eval harness: trigger / output / aggregate subcommands
  eval_clients/              pluggable clients for the harness
    base.py                  EvalClient interface and InvocationResult
    stub.py                  deterministic offline client used by CI and tests
    claude_code.py           shells the real `claude` CLI for actual measurements
schemas/                     JSON Schemas for eval files, trigger reports, benchmarks
tests/                       pytest suite for the validators, harness, and examples
examples/                    per-skill walkthroughs with rubrics and, where possible, verifiers
benchmarks/                  committed with-skill-versus-baseline runs (schema-checked)
```

The two validators are deliberately dependency-free so they can be reviewed and run offline by anyone evaluating the package. The eval harness is developer tooling; nothing at runtime imports it.

## Flows

**Authoring a skill change.** Edit `SKILL.md`/`references/`/`evals/` → `make validate` (both validators) → `make validate-official` (the reference `skills-ref` validator, pinned to a commit) → pull request → CI (validators on Python 3.10–3.13, pytest + ruff + mypy, eval-schema checks, an offline eval-harness smoke run, markdownlint, CodeQL) → squash merge.

**Evaluating a skill.** `run_evals.py trigger` measures activation accuracy from `trigger-evals.json` with a deterministic train/validation split; `run_evals.py output` runs `evals.json` cases with and without the skill and scaffolds grading files; `run_evals.py aggregate` rolls human- or model-graded results into a `benchmarks/` file. The `stub` client makes the whole path runnable with no model, which is what CI exercises.

**Releasing.** Conventional Commits on `main` → Release Please opens a release pull request that bumps `.release-please-manifest.json` and both plugin manifests and regenerates `CHANGELOG.md` → merging it tags `vX.Y.Z` → the release workflow validates the tag against the manifests, builds the tarball, attests build provenance, signs with cosign, and attaches the archive, signature, certificate, and provenance bundle to the GitHub Release.

## Boundaries and invariants

- Skill text is language- and framework-agnostic; stack-specific material lives only under `examples/`.
- `SKILL.md` stays under 500 lines and roughly 5,000 tokens; depth goes into `references/`, one level deep, with explicit `Read <file> when <condition>` triggers.
- Skill and reference text must not contain prompt-injection signatures or credentials; the validator rejects both.
- Manifest versions and the release manifest must agree; CI and the release workflow both check it.
- Runtime validators import only the standard library.
