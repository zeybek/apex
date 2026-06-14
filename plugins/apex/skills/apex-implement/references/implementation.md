# Implementation Judgment

## Fit the Existing System

- Read local instructions and inspect neighboring code before choosing a style.
- Use the repository's framework, helpers, error model, logging conventions, test infrastructure, and module boundaries when they remain sound.
- Keep changes close to the component that owns the behavior.
- Avoid introducing a second way to solve the same problem without a migration reason.

## Select the Solution

Choose the option that:

1. satisfies the observable requirement;
2. preserves applicable safety and contracts;
3. is easy to verify and operate;
4. has the lowest justified lifecycle cost;
5. introduces the least accidental complexity.

Prefer:

- deletion over replacement when behavior is unnecessary;
- standard and native facilities over custom mechanisms when they meet the required semantics;
- boring, explicit code over compressed or clever code;
- direct implementation over speculative generalization;
- reversible decisions over one-way decisions.

Do not confuse fewer lines with lower complexity. Optimize for the effort needed to understand, change, verify, deploy, and recover the system.

## Add Abstractions Deliberately

Add an abstraction when at least one is true:

- multiple real consumers need the same stable behavior;
- it isolates a volatile external dependency or policy;
- it makes an important invariant enforceable;
- it removes meaningful duplication without obscuring differences;
- it matches an established architecture boundary.

Avoid:

- interfaces with one implementation and no boundary value;
- configuration for values that are not expected to vary;
- factories, wrappers, or layers that only rename another call;
- generic frameworks built for imagined future use.

## Manage Dependencies

Before adding a dependency, evaluate:

- correctness and security value compared with custom code;
- maintenance activity, ownership, license, and supply-chain risk;
- transitive dependencies and runtime footprint;
- compatibility and upgrade strategy;
- whether an existing dependency or platform feature already covers the need.

Use established libraries for complex protocols, parsing, cryptography, serialization, and security-sensitive behavior. A short custom implementation is not automatically safer or cheaper.

## Preserve Contracts

Treat these as contracts when consumers can depend on them:

- APIs, command-line behavior, error forms, events, schemas, file formats;
- configuration names and defaults;
- timing, ordering, idempotency, and retry semantics;
- user workflows and accessibility behavior;
- operational procedures and telemetry relied on during incidents.

Inspect consumers before changing a contract. Prefer backward-compatible evolution and explicit deprecation.

## Handle Boundaries and Failure

- Validate untrusted data at the trust boundary.
- Preserve useful error context without exposing secrets.
- Fail explicitly when continuing would corrupt state or mislead callers.
- Use fallback only when it has defined semantics and is observable.
- Keep cleanup, cancellation, timeout, and partial-failure behavior coherent.
- Make operations idempotent before adding automatic retries.

## Concurrency and State

- State invariants before changing concurrent or transactional behavior.
- Identify ownership, atomicity boundaries, ordering, and duplicate delivery.
- Prefer database or platform constraints for invariants they can enforce.
- Do not assume a check followed by a write is atomic.
- Test or reason about competing actors, retries, crashes, and partial success.

## Performance

- Do not optimize without a requirement, measurement, or clear complexity risk.
- Protect obvious scalability boundaries such as unbounded work, memory, queues, fan-out, and repeated remote calls.
- Measure representative workloads before claiming improvement.
- State the tradeoff when accepting a known performance ceiling.

## Change Discipline

- Keep the diff focused on the requested behavior and required supporting work.
- Separate mechanical refactors from behavior changes when practical.
- Update documentation when the source code cannot communicate the operational or user-facing contract.
- Leave the codebase at least as understandable as before.

## Foundational Sources

- IEEE SWEBOK software construction topics: https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics
- Google Engineering Practices: https://google.github.io/eng-practices/
- Martin Fowler, Refactoring catalog: https://refactoring.com/
