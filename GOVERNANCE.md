# Governance

Apex is a small, single-maintainer open-source project. This document states how decisions are made so contributors know what to expect.

## Maintainer

The project is maintained by Ahmet Zeybek ([@zeybek](https://github.com/zeybek)), who is the code owner ([.github/CODEOWNERS](.github/CODEOWNERS)) and has final say on what is merged and released.

## How changes are made

- Changes land on `main` via [Conventional Commits](https://www.conventionalcommits.org/); the maintainer may self-merge.
- Every change must pass CI — validators, tests, official skills-ref, and schema checks. See [CONTRIBUTING.md](CONTRIBUTING.md).
- Skill content stays language- and framework-agnostic; the runtime validators stay standard-library only.
- Releases are automated by Release Please and tagged `vX.Y.Z`; tags created through the release workflow are verified by GitHub. See [docs/RELEASING.md](docs/RELEASING.md).

## Decisions

- Routine changes: maintainer's discretion, guided by the [ROADMAP](ROADMAP.md) and the project's portability and dependency-free constraints.
- Larger or contested changes: discussed in an issue before implementation.
- The project is open to additional maintainers as it grows; express interest in an issue.

## Branch protection

`main` is protected by a ruleset that blocks force-pushes and branch deletion. Once the project adopts a pull-request-only flow, the maintainer can additionally enable "require status checks to pass" and "require linear history"; these are intentionally left off while a single maintainer pushes directly, so they do not block routine work.

## Conduct and security

All participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Report vulnerabilities privately per [SECURITY.md](SECURITY.md).
