# Releasing Apex

Releases are automated with [Release Please](https://github.com/googleapis/release-please). You do not bump versions or write release notes by hand; you merge Conventional-Commit changes and then merge the release pull request it prepares. This runbook complements the contributor rules in [../CONTRIBUTING.md](../CONTRIBUTING.md).

## How it works

1. Land changes on `main` with [Conventional Commit](https://www.conventionalcommits.org/) messages. `feat:` drives a minor bump, `fix:` a patch, and `feat!:` or a `BREAKING CHANGE:` footer a major.
2. Release Please keeps an open release pull request that bumps `.release-please-manifest.json` and both plugin manifests (`plugins/apex/.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`), and regenerates `CHANGELOG.md` from the commit history.
3. Review that pull request. Edit its changelog entry directly if you want richer notes than the commit subjects provide.
4. Merge the release pull request. Release Please then creates the `vX.Y.Z` tag and the GitHub Release.
5. The same workflow validates the tag against the manifests, builds a provenance-attested `apex-X.Y.Z.tar.gz`, and uploads it to the release.

The manifests are kept in sync automatically; `make validate` additionally checks that `.release-please-manifest.json` matches the plugin manifest version, and the release workflow checks the tag against it.

## Conventional Commit types

- `feat:` — a new or expanded skill, validator gate, or capability (minor).
- `fix:` — a corrected validator, manifest, or skill defect (patch).
- `docs:`, `refactor:`, `perf:` — surfaced in the changelog where relevant.
- `ci:`, `build:`, `chore:`, `test:` — hidden from the changelog.
- Append `!` or a `BREAKING CHANGE:` footer for an incompatible change (major).

## Submit to marketplaces

These steps require maintainer accounts and are done by hand:

- Claude Code: run `claude plugin validate` against the repository, then submit the marketplace entry to the community plugin catalog following its current contribution guide.
- Codex: register the marketplace in the corresponding Codex community catalog.

Add the published install path to the README once a listing is live.

## Branch protection

Configure these in the GitHub repository settings (UI, not a file):

- Require the `CI` workflow checks to pass before merging to `main`.
- Require at least one review; ownership is enforced by [../.github/CODEOWNERS](../.github/CODEOWNERS).
- Restrict direct pushes to `main` to maintainers so releases always flow through the release pull request.
