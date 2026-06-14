# Architecture Tradeoffs

Choose architecture from context and measurable priorities. Architecture is a set of consequential decisions, not a catalog of fashionable patterns.

## Establish Context

Capture:

- desired outcomes and prioritized quality scenarios;
- existing system shape, constraints, ownership, and operational capability;
- expected scale and change patterns;
- regulatory, security, privacy, and data obligations;
- delivery timeline, migration constraints, and available expertise.

## Generate Alternatives

- Include the smallest credible option and retaining the current design.
- Add materially different options, not cosmetic variations.
- Use prototypes or measurements when feasibility or performance is uncertain.
- Avoid rejecting an option only because it lacks novelty.

## Compare Consistently

For each alternative, assess:

| Area | Questions |
|---|---|
| Outcome | Does it solve the stated problem? |
| Quality | Which prioritized scenarios improve or degrade? |
| Risk | What can fail, and how severe is the consequence? |
| Reversibility | Can the decision be changed incrementally? |
| Delivery | What is the implementation and migration path? |
| Operations | What must be deployed, observed, secured, and recovered? |
| Cost | What is the total lifecycle cost? |
| Team fit | Can the owners build and operate it effectively? |

## Common Tradeoffs

- **Build versus buy:** control and fit versus maintenance and supply-chain dependence.
- **Single deployable versus distributed system:** local simplicity and strong transactions versus independent scaling, ownership, and failure domains.
- **Synchronous versus asynchronous interaction:** immediate feedback and simpler flow versus decoupling, buffering, and eventual completion.
- **Consistency versus availability under failure:** define required semantics; do not use slogans as a decision.
- **Flexibility versus simplicity:** pay for variation only when it is real.
- **Performance versus maintainability:** optimize measured bottlenecks while preserving understandable behavior.

## Pressure-Test the Recommendation

- Trace normal, peak, degraded, recovery, and abuse scenarios.
- Identify single points of failure and correlated failure.
- Examine retries, duplicates, ordering, timeouts, cancellation, and partial success.
- Check old/new compatibility during rollout and rollback.
- State the assumptions and thresholds that would reverse the decision.
- Identify operational load and ownership, not only implementation cost.

## Foundational Sources

- SEI Architecture Tradeoff Analysis Method: https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/
- IEEE SWEBOK: https://www.computer.org/education/bodies-of-knowledge/software-engineering
