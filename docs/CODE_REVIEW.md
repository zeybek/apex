# Code Review

Every change to `main` arrives as a pull request and is reviewed against the same standard, whether the author is a maintainer, a contributor, or a bot. This page states what review must establish, how it is conducted, and what is required for a change to be acceptable.

## Who reviews

- The code owners in [`.github/CODEOWNERS`](../.github/CODEOWNERS) are requested automatically on every pull request. Either maintainer may review and merge.
- Review by a person other than the author is the goal. While the project has two maintainers, a change by one maintainer is reviewed by the other whenever they are available; a maintainer may self-merge a change only after the full CI suite has passed and the review checklist below has been applied to their own change explicitly, and the pull request says so.
- Dependency updates from Dependabot are reviewed like any other change (see the Dependabot section).

## What must be checked

Review is risk-first. The reviewer reads the whole diff plus enough surrounding context to understand the behavior, then checks, in this order:

1. **Intent.** The change does what its title and description say, nothing more. Scope creep, unrelated cleanup, and drive-by refactors are sent back.
2. **Skill content** (`plugins/apex/skills/**`):
   - stays language- and framework-agnostic, and contains no client or vendor names in the portable core;
   - keeps `SKILL.md` under the size limits and pushes depth into `references/` with explicit read triggers;
   - uses the vocabulary the skill already uses; a renamed or merged concept needs a stated reason;
   - contains no text that could redirect an agent away from its task (the validator's injection scan is a floor, not the check);
   - ships eval changes alongside behavior changes: new or changed instructions get trigger and output cases.
3. **Tooling** (`scripts/`, `tests/`, `schemas/`): correctness of the gate being changed, tests that fail before and pass after, no new runtime dependencies in the validators, types and lint clean under the strict configuration.
4. **Supply chain** (`.github/workflows/**`, `requirements-dev.*`, `dependabot.yml`): actions pinned to full commit SHAs with a version comment, least-privilege `permissions`, hash-pinned Python requirements, no secrets or tokens in logs.
   - **Hooks and agents** (`plugins/apex/hooks/**`, `plugins/apex/agents/**`) are the parts that run on or steer a user's machine: hook scripts stay standard-library and read-only (workspace files and `git status` only, text output only), `hooks.json` runs only shipped scripts, and agent prompts keep file-editing tools disallowed. Any widening of that surface is a security-review trigger.
5. **Docs and manifests**: README, adapters, and manifests still describe what the package does; version fields are never edited by hand.
6. **Security review triggers**: any change to SECURITY.md, the validators' scan patterns, release signing or attestation, or branch and tag rules gets an explicit note in the review that the threat model in [ASSURANCE_CASE.md](ASSURANCE_CASE.md) still holds.

## What is required to be acceptable

- All CI checks green: validators on every supported Python version, pytest, ruff (check and format), mypy, the official skills-ref validation, eval-schema checks, the eval-harness smoke run, markdownlint, and CodeQL.
- A Conventional Commit title, because it becomes the squash-merge commit subject and drives versioning.
- The pull request template checklist filled in truthfully.
- For skill changes: `make validate` and `make validate-official` pass, and the eval files were extended, not just kept valid.
- For fixes: a regression test or eval case that reproduces the original problem.
- Findings are stated as findings — location, triggering scenario, impact, and a remediation direction — in the same form the `apex-review` skill prescribes. Style preferences are not blocking.

## Dependabot pull requests

Automated updates are trusted only after verification: the pinned commit is confirmed to be the upstream tag's commit, the release is a stable (non-prerelease) release older than the configured cooldown, Python package hashes match the PyPI digests, major bumps are checked against the upstream release notes for breaking changes that apply to this repository, and CI is green on the rebased branch. Grouped updates (for example the CodeQL actions) must be merged as a group.

## Records

Review happens in the pull request; the discussion, the CI results, and the merge form the record. Decisions that change project direction are referenced from [GOVERNANCE.md](../GOVERNANCE.md) or the [ROADMAP](../ROADMAP.md).
