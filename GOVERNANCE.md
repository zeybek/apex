# Governance

Apex is a small open-source project with two maintainers. This document states who holds which role, how decisions are made, and how the project continues if a maintainer becomes unavailable, so contributors know what to expect.

## Roles

| Role | Who | Responsibilities |
|---|---|---|
| Lead maintainer | Ahmet Zeybek ([@zeybek](https://github.com/zeybek)) | Sets direction ([ROADMAP.md](ROADMAP.md)), reviews and merges changes, cuts releases, triages issues, handles security reports per [SECURITY.md](SECURITY.md), and has the final say on contested changes. |
| Backup maintainer | Fatih Yaman ([@fatihy101](https://github.com/fatihy101)) | Holds the same repository rights (admin). Reviews changes, may merge and release, and takes over every lead-maintainer duty if the lead is unavailable. |
| Contributor | Anyone | Proposes changes through pull requests per [CONTRIBUTING.md](CONTRIBUTING.md), reports bugs and vulnerabilities, participates under the [Code of Conduct](CODE_OF_CONDUCT.md). |

Both maintainers are listed in [.github/CODEOWNERS](.github/CODEOWNERS) and are requested on every pull request. Review expectations are in [docs/CODE_REVIEW.md](docs/CODE_REVIEW.md).

## Access continuity

The project must be able to keep accepting changes, closing issues, and shipping releases if any one person is unavailable. Both maintainers therefore hold admin access to the repository, both can merge the Release Please pull request that produces a release, and every release step is automated in the repository's workflows with no per-person secret: signing is keyless and provenance is attested by the workflow identity, so no private key lives with an individual. Vulnerability reports arrive through GitHub's private vulnerability reporting, visible to both maintainers, in addition to the lead maintainer's email in SECURITY.md.

## How changes are made

- Changes land on `main` only through pull requests with [Conventional Commit](https://www.conventionalcommits.org/) titles, squash-merged. A maintainer's change is reviewed by the other maintainer when available; self-merge is permitted only after CI passes and the review checklist has been applied explicitly (see [docs/CODE_REVIEW.md](docs/CODE_REVIEW.md)).
- Every change must pass CI — validators, tests, official skills-ref, and schema checks. See [CONTRIBUTING.md](CONTRIBUTING.md).
- Skill content stays language- and framework-agnostic; the runtime validators stay standard-library only.
- Releases are automated by Release Please and tagged `vX.Y.Z`; tags created through the release workflow are verified by GitHub. See [docs/RELEASING.md](docs/RELEASING.md).

## Decisions

- Routine changes: maintainers' discretion, guided by the [ROADMAP](ROADMAP.md) and the project's portability and dependency-free constraints.
- Larger or contested changes: discussed in an issue before implementation; the lead maintainer decides if the maintainers disagree.
- The project is open to additional maintainers as it grows; express interest in an issue. A new maintainer is added by the lead maintainer after sustained, reviewed contributions.

## Branch and tag protection

`main` is governed by a ruleset with no bypass actors: changes arrive only through pull requests (squash merge), and force-pushes and branch deletion are blocked. Tags are protected against deletion and rewriting. Requiring status checks in the ruleset is planned once the release pull requests run CI (they are currently opened with the workflow token, which does not trigger it); until then the full CI suite is required by review policy rather than by the ruleset.

## Conduct and security

All participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Report vulnerabilities privately per [SECURITY.md](SECURITY.md).
