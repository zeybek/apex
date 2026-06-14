# Decision Record

Use this structure for consequential design decisions. Keep it concise enough to remain useful and detailed enough to make the reasoning auditable.

## Template

### Title and Status

State the decision and mark it proposed, accepted, superseded, or deprecated. Include the date and owners when available.

### Context

Describe the problem, desired outcome, existing system, constraints, scope, non-goals, verified facts, and important assumptions.

### Prioritized Quality Scenarios

List the measurable scenarios that drive the decision and their priority.

### Alternatives

Describe credible alternatives, including retaining the current design when applicable. Compare them against the same criteria.

### Decision

State the selected option first. Explain why it best satisfies the priorities and constraints.

### Consequences

State benefits, costs, tradeoffs, operational burden, and capabilities that are intentionally not provided.

### Risks and Controls

List important failure, security, privacy, compatibility, data, and delivery risks with their controls and residual risk.

### Delivery and Verification

Define implementation stages, migration, compatibility, rollout, rollback or roll-forward, observability, and acceptance evidence.

### Revisit Conditions

State assumptions, measurements, dates, or system changes that should trigger a new decision. Link superseding decisions instead of rewriting history.

## Foundational Sources

- Architecture Decision Records: https://adr.github.io/
- Michael Nygard, "Documenting Architecture Decisions": https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- ISO/IEC/IEEE 42010 architecture description: https://www.iso.org/standard/74393.html
