# Contributing to Apex

Thanks for your interest in improving Apex. This project is a portable [Agent Skills](https://agentskills.io/) package, so contributions are held to two non-negotiable constraints: skills stay **language- and framework-agnostic**, and the validators stay **dependency-free** at runtime.

By participating you agree to our [Code of Conduct](CODE_OF_CONDUCT.md). To report a security issue, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Development setup

You need Python 3.10+ and `make`. The validators use only the standard library; no install step is required to run them. For the official format check you also need [uv](https://docs.astral.sh/uv/) (`uvx`).

```bash
git clone https://github.com/zeybek/apex
cd apex
make validate            # package + distribution validators (dependency-free)
make validate-official   # official skills-ref validation (needs network + uvx)
```

## Before you open a pull request

- Run `make validate` and `make validate-official`; both must pass.
- Keep every skill body language- and framework-agnostic. Small stack-specific walkthroughs may live under `examples/`, outside the distributed plugin, when they demonstrate a skill without becoming skill instructions.
- Keep `SKILL.md` under 500 lines and push depth into `references/`, loaded with explicit `Read <file> when <condition>` triggers.
- Reference links must be one level deep and resolve.

## Changing or adding a skill

Each skill under `plugins/apex/skills/<name>/` is a self-contained unit:

- `SKILL.md` — frontmatter (`name` matching the folder, `description` stating what and when) plus the workflow;
- `references/` — detailed, on-demand guidance;
- `evals/trigger-evals.json` — at least 20 activation prompts, balanced positive and negative;
- `evals/evals.json` — at least three output-quality cases, each with at least three observable assertions.

A new skill is not complete until its evals exist and `make validate` passes. See [evals/README.md](evals/README.md) for the evaluation protocol and [adapters/README.md](adapters/README.md) for per-client installation.

## Versioning and releases

This project follows [Semantic Versioning](https://semver.org/), and releases are automated with [Release Please](https://github.com/googleapis/release-please). You do not bump versions or edit `CHANGELOG.md` by hand: Release Please derives the next version from [Conventional Commit](https://www.conventionalcommits.org/) messages, opens a release pull request that bumps both plugin manifests and the changelog together, and tags the release when that pull request is merged.

`make validate` enforces that both plugin manifests and `.release-please-manifest.json` carry the same valid semantic version. See [docs/RELEASING.md](docs/RELEASING.md) for the full release and marketplace-submission runbook.

## Commit and PR conventions

- Use [Conventional Commit](https://www.conventionalcommits.org/) subjects (`feat:`, `fix:`, `docs:`, `ci:`, …) so Release Please can version and changelog the change.
- Keep changes focused; separate skill-content changes from tooling changes.
- Write a clear description and fill in the pull request template checklist.
- Maintainers review via `CODEOWNERS`; expect a validation run on every PR.
