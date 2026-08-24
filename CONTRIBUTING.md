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
- Keep hooks read-only and standard-library only: a hook may read the workspace and `git status` and print text, nothing else, and `hooks.json` may only run scripts shipped under `plugins/apex/hooks/` (the validator enforces this).
- Keep `SKILL.md` under 500 lines and push depth into `references/`, loaded with explicit `Read <file> when <condition>` triggers.
- Reference links must be one level deep and resolve.
- Add tests with the change: new or changed behavior in `scripts/` or `plugins/apex/hooks/` must come with tests in `tests/` (run `make test`), and a new or changed skill must come with its `evals/` cases. CI runs the full test suite, `ruff`, and `mypy` on every pull request and blocks on warnings; a change that lowers coverage or introduces a warning is not ready to merge.

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
- Sign off every commit (`git commit -s`). The `Signed-off-by:` trailer certifies the [Developer Certificate of Origin 1.1](https://developercertificate.org/): that you wrote the change or have the right to submit it under the MIT license. Pull requests whose human-authored commits lack the trailer are not merged.
- Keep changes focused; separate skill-content changes from tooling changes.
- Write a clear description and fill in the pull request template checklist.
- Maintainers review via `CODEOWNERS` against [docs/CODE_REVIEW.md](docs/CODE_REVIEW.md); expect a validation run on every PR.
