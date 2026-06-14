---
name: apex-design
description: Use this skill when designing or evaluating a non-trivial software change before implementation. Apply it to architecture decisions, technical designs, API or schema evolution, data migrations, service boundaries, build-versus-buy choices, and reliability planning that require explicit requirements, alternatives, risks, contracts, and operational tradeoffs. Do not use it when the user only wants implementation of an already-decided change.
license: MIT
---

# Apex Design

Turn an ambiguous or consequential change into an implementable, reviewable decision. Optimize for the required outcomes and constraints, not for a preferred architecture style.

## Workflow

### 1. Frame the decision

- State the problem, desired outcome, scope, non-goals, constraints, and decision owner.
- Separate verified facts, assumptions, and unresolved questions.
- Identify what must be decided now and what can remain reversible.

### 2. Inspect the existing system

- Read repository instructions, relevant code, diagrams, tests, schemas, operations documentation, and recent decisions.
- Map current responsibilities, dependencies, data flow, failure behavior, and operational ownership.
- Explain why the current design does not satisfy the requested outcome before proposing a replacement.

### 3. Define quality scenarios

Read [quality-attributes.md](references/quality-attributes.md) when a goal is stated as an adjective such as "scalable", "secure", or "maintainable". Convert those vague goals into prioritized, measurable scenarios. Include important failure and abuse scenarios.

### 4. Develop credible alternatives

Read [architecture-tradeoffs.md](references/architecture-tradeoffs.md) when more than one option is credible. Include the current design when retaining it is credible. Compare alternatives against the same outcomes, quality scenarios, constraints, delivery cost, and operational burden.

### 5. Choose and pressure-test

- Recommend one option and state why it wins under the stated priorities.
- Identify tradeoffs, sensitivities, failure modes, irreversible decisions, and assumptions that could invalidate the choice.
- Prefer reversible steps when evidence is weak.

For public interfaces, persistent data, events, or rolling deployments, read [contracts-and-migrations.md](references/contracts-and-migrations.md).

### 6. Make the design executable

Specify enough detail for implementation and review:

- component responsibilities and ownership;
- data and control flow;
- external and internal contracts;
- invariants, validation, and failure behavior;
- security, privacy, and access boundaries;
- observability and operational ownership;
- migration, rollout, rollback or roll-forward;
- verification strategy and acceptance evidence.

Avoid implementation detail that does not affect a decision, contract, or risk.

### 7. Record the decision

Use [decision-record.md](references/decision-record.md). Lead with the recommendation, then document context, alternatives, consequences, delivery plan, risks, and revisit conditions. Do not conceal uncertainty.

## Output Standard

A strong design enables another engineer to understand the decision, challenge its assumptions, implement it, verify it, operate it, and recognize when it should be revisited.

## Method Gotchas

- Scope creep hides in vaguely written non-goals; state what you are deliberately not solving as precisely as what you are.
- The current design is a real alternative — evaluate it on the same axes instead of strawmanning it to justify a rewrite.
- A "simple" option that ignores a required quality scenario is not simple, it is incomplete; price the missing work before comparing.
- Reversibility is a feature: when evidence is weak, prefer a cheaper undoable step over a confident one-way decision.
- Most design disagreements are really disagreements about priorities; surface the priority order before debating mechanisms.

## Worked Example

Request: "Make the order-submission endpoint safe to retry."

1. Frame: the outcome is at-most-once settlement under client and network retries; the non-goal is changing pricing logic. The decision is reversible at the API layer but not once data is stored.
2. Quality scenario: "When a client sends the same submission twice within an hour, the system settles it once and returns the original result." Abuse scenario: a replayed request must not create a second charge.
3. Alternatives: (a) deduplicate by a natural key such as customer plus cart hash; (b) require a client-supplied idempotency key persisted before the downstream call; (c) keep current behavior and document the risk.
4. Choose (b): the natural key collides for legitimately distinct orders, and "do nothing" fails the abuse scenario, so the idempotency key wins under the at-most-once priority.
5. Pressure-test: the key store is now on the critical path, so its unavailability must fail closed rather than silently allow duplicates. Record this as a risk with a control.
6. Record: one decision record capturing the at-most-once priority, the three alternatives, and a revisit condition ("reconsider if submission volume makes the key store a bottleneck").

## Design Checklist

- [ ] Problem, outcome, scope, non-goals, and decision owner are written down.
- [ ] Vague goals are converted into prioritized, measurable quality and abuse scenarios.
- [ ] The current design is included as an alternative and compared on the same axes.
- [ ] One option is recommended with an explicit reason it wins under the stated priorities.
- [ ] Contracts, failure behavior, migration, rollback, and verification are specified.
- [ ] Irreversible decisions, key risks, and revisit conditions are recorded, not hidden.
