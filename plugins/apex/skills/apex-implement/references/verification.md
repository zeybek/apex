# Risk-Based Verification

Verification must provide credible evidence for the changed behavior and its important failure modes. Test count and coverage percentage are supporting signals, not the objective.

## Build an Evidence Plan

For each changed behavior, identify:

- the claim being made;
- the cheapest reliable evidence for that claim;
- the important negative or failure case;
- the contract or invariant that must not regress.

Prefer deterministic automated evidence close to the behavior. Add broader tests when integration, configuration, runtime, or deployment behavior is part of the claim.

## Select Verification by Risk

### Low-risk change

- Run the narrowest relevant existing test.
- Run repository-standard static checks affected by the edit.
- Inspect the resulting diff.

### Medium-risk change

- Add or update focused regression tests.
- Verify boundaries, invalid input, and relevant failure behavior.
- Run integration or component checks for affected consumers.
- Verify generated artifacts, configuration, or documentation when applicable.

### High-risk change

- Verify invariants, authorization, data integrity, concurrency, and rollback.
- Test old/new compatibility for contracts and migrations.
- Exercise partial failures, retries, duplicate delivery, and recovery where relevant.
- Validate operational signals and staged rollout assumptions.

## Test Design Rules

- Test observable behavior, contracts, and invariants rather than incidental implementation.
- Make a defect fix fail before the fix when feasible.
- Cover meaningful partitions and edge cases, not arbitrary value volume.
- Keep tests deterministic, isolated enough to diagnose, and readable as usage examples.
- Use real dependencies at the boundary where mocks would hide integration behavior.
- Avoid broad end-to-end tests when a smaller test proves the same claim more reliably.
- Do not delete valuable tests merely to reduce maintenance effort.

## Verification Layers

Use the layers that match the change:

- Static evidence: formatting, linting, type checking, schema validation, dependency or security scanning.
- Unit evidence: pure logic, invariants, state transitions.
- Component evidence: module behavior with realistic collaborators.
- Integration evidence: database, network, filesystem, queue, protocol, or external service contracts.
- System evidence: critical user workflows and production-like behavior.
- Operational evidence: telemetry, rollout, rollback, load, and recovery.

## Interpret Results

- Read failures and determine whether they reveal a defect, stale expectation, environment problem, or unrelated existing issue.
- Never report a command as passing without checking its exit status and useful output.
- State what was not run and why.
- Do not claim absence of bugs. State the evidence gathered and remaining risk.

## Foundational Sources

- IEEE SWEBOK testing topics: https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics
- Google Engineering Practices: https://google.github.io/eng-practices/review/
- Google SRE production practices: https://sre.google/sre-book/service-best-practices/
