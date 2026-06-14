# Production Readiness

Treat production behavior, rollout, and recovery as part of the design whenever a change affects a running service, durable state, or operational procedure.

## Reliability Intent

- Define the user-visible behavior that must remain reliable.
- Use measurable service indicators and objectives when reliability matters.
- Avoid aiming for undefined perfection. Balance reliability work with user value and delivery needs.
- Design overload, dependency failure, and degraded behavior explicitly.

## Observability

Ensure operators can answer:

- Is the change working for users?
- What failed, where, and for whom?
- Is impact growing?
- Can the change be rolled back or disabled?

Prefer useful, correlated signals:

- metrics for rates, latency, saturation, and outcomes;
- structured logs for diagnosable events;
- traces for cross-boundary requests;
- alerts tied to actionable user impact.

Avoid secrets, excessive cardinality, noisy alerts, and telemetry without an operational consumer.

## Safe Delivery

- Prefer small, reversible changes.
- Use staged rollout, canary, traffic splitting, feature control, or equivalent when blast radius warrants it.
- Define success and abort signals before rollout.
- Monitor the rollout and stop or roll back on unexpected user impact.
- Keep deployment artifacts identifiable and reproducible.

## Compatibility and State

- Expect old and new versions to coexist during rolling deployment.
- Make readers tolerate old and new data before writers produce new data.
- Use expand-migrate-contract for incompatible schema or protocol evolution.
- Keep rollback safe until the new state is proven and old state is no longer required.
- Verify backfills, partial completion, retries, and resumability.

## Distributed Failure

- Set bounded timeouts for remote work.
- Retry only transient failures, with limits and backoff, after establishing idempotency.
- Prevent retry amplification and unbounded queues.
- Define duplicate, ordering, cancellation, and partial-success semantics.
- Prefer graceful degradation when it preserves useful and honest behavior.

## Recovery

- Define rollback or roll-forward procedure before a risky release.
- Protect backups and verify restoration when data loss is plausible.
- Make destructive operations explicit, authorized, auditable, and recoverable where feasible.
- Learn from incidents by improving systems and controls, not blaming people.

## Foundational Sources

- Google SRE SLO guidance: https://sre.google/workbook/implementing-slos/
- Google SRE production practices: https://sre.google/sre-book/service-best-practices/
- AWS rollback-safe deployments: https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/
