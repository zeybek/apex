# Assurance Case

This page argues why Apex meets its security requirements. It states what the project promises, the threat model and trust boundaries those promises are made against, the secure-design principles applied, how common implementation weaknesses are prevented, and the evidence behind each claim. It complements [SECURITY.md](../SECURITY.md) (how to report) and [ARCHITECTURE.md](ARCHITECTURE.md) (what the pieces are).

## 1. Security requirements

What a user of Apex can rely on:

- **R1 — Instructions, plus two inspectable hooks.** The installed package (`plugins/apex/`) is Markdown and JSON except for two standard-library hook scripts. The skills and agents contain no executable code; the hooks read the working directory's `.apex-design/` and `git status`, print text, make no network calls, write nothing, and read no credentials. Any other action taken while a skill is loaded is taken by the host agent under the host's own permissions.
- **R2 — No task hijack via package content.** Skill and reference text must not contain instructions that redirect an agent away from the user's task or exfiltrate data.
- **R3 — No secrets in the package or repository.**
- **R4 — Authentic releases.** A release archive can be verified to have been built by this repository's release workflow from a tagged commit, unmodified.
- **R5 — Reviewable tooling.** The validators anyone runs to check the package are standard-library-only and can be read and executed offline.
- **R6 — Hardened delivery pipeline.** The path from a contributor's change to a published release resists tampering by a compromised dependency, action, or token.

## 2. Threat model

**Assets.** The skill text loaded into users' agents; the release artifacts; the repository's ability to publish; the maintainers' credentials.

**Adversaries.**

- A contributor (or a compromised contributor account) who submits skill text that subverts agents (prompt injection through instruction content).
- An attacker who tampers with a release archive or substitutes one in transit.
- A compromised upstream dependency or GitHub Action that runs inside CI or the release workflow.
- An attacker who obtains a maintainer credential or a workflow token.

**Out of scope.** Vulnerabilities in host agents (Claude Code, Codex, other clients) and in the user's own repository, model, or environment. These are reported to the respective vendor.

## 3. Trust boundaries

| Boundary | Inside | Outside | Controls at the boundary |
|---|---|---|---|
| Package content → host agent | `plugins/apex/**` Markdown and JSON | Host agent, user's repository, model | R1: no code in skills or agents. R2: validator injection scan (skills, references, agents, hooks) + human review of every change. |
| Hook scripts → host process | `plugins/apex/hooks/*.py` run by the host on `SessionStart` and `Stop` | User's working directory, git repository | Standard library only; read-only (`.apex-design/`, `git status`); output limited to text; validator rejects hooks that are not commands running shipped scripts; CI lint, strict types, and tests; Codex additionally requires the user to trust the hook definition. |
| Pull request → `main` | Reviewed, CI-verified squash commits | Any contributor, Dependabot | Ruleset: pull requests only, squash merge, no force-push or deletion; full CI required in practice; CODEOWNERS review. |
| `main` → release | Release Please PR, tag, release workflow | GitHub Actions runtime, third-party actions | Least-privilege `permissions`; every action pinned to a full commit SHA; Release Please PR merged by a maintainer; tag ruleset blocks deletion and rewrite. |
| Release workflow → artifact | Tarball built from the tagged tree | Consumers downloading over HTTPS | Sigstore keyless signature (cosign), GitHub build-provenance attestation (SLSA), provenance bundle attached; tag-to-manifest version check before build. |
| Dev tooling → PyPI | Hash-pinned `requirements-dev.txt` | Package index, transitive dependencies | `pip install --require-hashes`; Dependabot with a 7-day cooldown; alerts and security updates enabled. |
| Maintainer account → repository | Two maintainers with admin rights | Everyone else | GitHub 2FA on maintainer accounts; secret scanning with push protection; private vulnerability reporting for inbound reports. |

## 4. Secure design principles applied

- **Economy of mechanism / least functionality.** The product is text. The only executables that ship are two small read-only hook scripts; the validators and eval harness stay in the repository (R1, R5).
- **Least privilege.** Workflow tokens default to `contents: read`; `contents: write`, `id-token: write`, and `attestations: write` are granted only to the release job that needs them. Maintainer admin rights are held by exactly two people (R6).
- **Fail-safe defaults.** The validators reject a skill on any structural, injection, or secret finding; CI blocks on warnings; the release workflow refuses a tag whose version disagrees with the manifests (R2, R3, R4).
- **Complete mediation.** Every change to `main` passes through the same pull-request path and the same CI; there is no bypass actor on the ruleset (R6).
- **Open design.** All controls are in the repository and documented; verification of a release needs only public tooling ([RELEASING.md](RELEASING.md), "Verifying a release") (R4, R5).
- **Defense in depth on content.** Injection and secret scans are regular-expression floors; reviewer judgment is the ceiling; the host agent's own permission model is the backstop (R2).
- **Separation of privilege for supply chain.** Dependencies are pinned by hash or commit, proposed by Dependabot only after a cooldown, verified against upstream before merge, and monitored by Dependabot alerts, CodeQL, and OpenSSF Scorecard (R6).

## 5. Common implementation weaknesses and how they are prevented

| Weakness class | Relevance | Prevention |
|---|---|---|
| Prompt injection via instruction content (OWASP LLM01) | Highest: the product is instructions | Validator scan for override/exfiltration phrasing across skills, references, agents, and hooks; explicit review checklist item; `SECURITY.md` documents the limits of the scan. |
| Hook abuse (a hook that runs arbitrary or external commands) | Hooks execute on the user's machine | `hooks.json` may contain only `command` hooks whose command runs a script shipped under the plugin root; scripts are stdlib-only and read-only; Codex requires explicit user trust. |
| Unsafe parsing / injection in tooling | Validators parse YAML-like frontmatter and JSON | Standard-library `json` only; frontmatter parsed with a bounded regular expression; no `eval`, no shell string construction; `subprocess` used without a shell and with explicit `check`. |
| Path traversal in link validation | Validators resolve relative links | References escaping the skill directory or deeper than one level are rejected. |
| Committed secrets | Any repository | Validator secret-pattern scan; GitHub secret scanning with push protection. |
| Dependency confusion / tampered packages | Dev tooling | Hash-pinned requirements enforced at install; actions pinned to commit SHAs. |
| Tampered or spoofed releases | Distribution | Keyless signature bound to this repository's workflow identity; provenance attestation; documented verification. |
| Lint/type classes of bugs | Tooling | ruff with a broad rule set, `mypy --strict` on `scripts/`, CodeQL on every change. |

## 6. Evidence

- `scripts/validate_package.py` — injection and secret signatures, link and size limits, hook and agent definitions; `tests/test_validate_package.py`.
- `plugins/apex/hooks/*.py` — read-only hook scripts; `tests/test_hooks.py` covers parsing, context rendering, and every stop-guard decision path.
- `.github/workflows/ci.yml` — validators on four Python versions, pytest, ruff check and format, mypy, skills-ref, schema checks, harness smoke run, markdownlint.
- `.github/workflows/codeql.yml`, `.github/workflows/scorecard.yml` — continuous static analysis and posture scoring; results in the repository's Security tab.
- `.github/workflows/release.yml` — tag validation, provenance attestation, cosign signing, provenance bundle upload.
- `.github/dependabot.yml` — grouped updates with a 7-day cooldown; `requirements-dev.txt` generated with `--generate-hashes`.
- Repository settings — pull-request-only ruleset on `main`, tag ruleset, secret scanning and push protection, private vulnerability reporting, Dependabot alerts and security updates.
- Badges — OpenSSF Scorecard and OpenSSF Best Practices, linked from the README.

## 7. Residual risks

- The injection scan is heuristic; paraphrased or encoded instructions can evade it. Mitigated by review, not eliminated.
- A single maintainer can still self-merge when the second is unavailable; two-person review is the norm, not a hard gate.
- Release verification depends on Sigstore and GitHub infrastructure being trustworthy.
- Skills influence agent behavior; a well-formed but poorly judged instruction is a quality problem review must catch, not something a scanner can.

This case is revisited whenever the threat model, the release pipeline, or the validators change (see [CODE_REVIEW.md](CODE_REVIEW.md), "Security review triggers").
