# Risk Model

Use risk to determine engineering rigor. Do not use file count, line count, or task wording as a proxy for impact.

## Assess Risk Dimensions

Evaluate each dimension before implementation:

| Dimension | Lower risk | Higher risk |
|---|---|---|
| Blast radius | Local behavior | Shared library, platform, many users |
| Reversibility | Easy revert, no state change | Irreversible or costly recovery |
| Criticality | Convenience behavior | Auth, money, safety, core workflow |
| Exposure | Internal trusted input | Public or adversarial input |
| Persistence | Ephemeral computation | Durable data or schema change |
| Concurrency | Single actor | Races, ordering, distributed coordination |
| Compatibility | Private implementation | Public API, event, config, data format |
| Operability | No production effect | Deployment, capacity, alerting, on-call |
| Uncertainty | Existing proven pattern | Novel behavior or unclear requirements |

Use the highest meaningful dimension, not an average, to set the baseline.

## Risk Levels

### Low

Characteristics:

- Local, reversible, and easy to observe.
- No persistent state, public contract, or trust-boundary effect.
- Failure has limited impact.

Expected rigor:

- Focused implementation.
- Existing unit or component checks.
- Lint, type, build, or equivalent repository checks where relevant.

### Medium

Characteristics:

- Shared code, external integration, configuration, or persistence.
- Moderate blast radius or non-trivial failure behavior.
- Compatibility or operational behavior may change.

Expected rigor:

- Explicit acceptance criteria and affected-contract review.
- Boundary, negative, and integration verification.
- Failure-path and rollback consideration.
- Documentation or observability updates when behavior changes.

### High

Characteristics:

- Security, privacy, money, safety, destructive operations, public contracts, durable migrations, concurrency, distributed consistency, or broad rollout.
- Hard-to-reverse decisions or severe failure impact.

Expected rigor:

- Explicit threat, failure-mode, and compatibility analysis.
- Strong automated evidence at relevant boundaries.
- Migration and rollback or roll-forward plan.
- Production observability and staged rollout plan.
- Clearly stated residual risk and unresolved assumptions.

## Escalation Triggers

Treat the change as high risk when any of these apply:

- It can lose, corrupt, duplicate, or expose data.
- It changes authorization, authentication, cryptography, or secret handling.
- It changes a public API, event schema, persisted format, or protocol.
- It introduces retries, asynchronous work, locks, transactions, or caching.
- It changes a destructive command or automated production action.
- It cannot be safely reverted after deployment.
- Its correctness depends on timing, ordering, or multiple system versions.

## Handling Uncertainty

- Investigate discoverable facts before asking the user.
- State assumptions when evidence is unavailable.
- Prefer reversible implementation when uncertainty remains.
- Do not reduce rigor merely because a change appears syntactically small.

## Foundational Sources

- IEEE SWEBOK: https://www.computer.org/education/bodies-of-knowledge/software-engineering
- NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
- SEI ATAM: https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/
