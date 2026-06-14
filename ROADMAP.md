# Roadmap

Direction for Apex, subject to change based on need and feedback. This is a priority order, not a schedule — dates are intentionally omitted.

## Now

- **Proof-of-value:** commit real, single-environment benchmarks (with-skill versus baseline) per skill, produced by the eval harness (`scripts/run_evals.py`).
- Keep the four skills — design, implement, review, investigate — sharp and well-evaluated.

## Next

- Pursue the OpenSSF Best Practices badge (self-certification at bestpractices.dev), complementing the OpenSSF Scorecard and CodeQL scanning that already run in CI.
- Per-skill usage walkthroughs as adoption grows.

## Later / under consideration

- Additional language-agnostic skills, only when the harness shows a new one earns its context.
- Listing in a community plugin marketplace (currently self-hosted by choice).
- An automated regression gate over committed benchmarks.

## Non-goals

- Stack- or framework-specific skill content — portability is the product.
- Runtime dependencies in the validators — they stay standard-library only.
- Supply-chain or governance machinery disproportionate to a Markdown plus small-validator package.
