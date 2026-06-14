---
name: apex-implement
description: Use this skill when implementing software changes end to end with language- and framework-independent senior engineering judgment. Apply it to features, bug fixes, refactors, debugging, integrations, migrations, configuration, dependencies, executing a planned `.apex-design/<slug>/` workspace, and production-facing code work that requires inspecting the existing system, controlling risk, preserving contracts, and verifying results. Do not use it for review-only or design-only requests.
license: MIT
---

# Apex Implement

Implement the requested outcome while controlling engineering risk. Treat simplicity as a selection rule after correctness, safety, contracts, and operability are satisfied.

## Workflow

### 1. Establish the change contract

- Translate the request into observable behavior and acceptance evidence.
- Discover missing context from repository instructions, code, tests, configuration, schemas, and history before asking questions.
- Separate facts, assumptions, and unresolved decisions.
- Identify explicit non-goals to prevent scope drift.

### 2. Adopt an existing plan workspace

When a `.apex-design/<slug>/` workspace exists for this work, it is the contract. Read [plan-execution.md](references/plan-execution.md), then read its `brief.md`, `requirements.md`, `design.md`, and `plan.md` before changing code. Implement the plan's tasks in dependency order, run each task's `verify` and confirm its `done` condition, and keep `progress.md` current as you go. If a task cannot be done as written or the design proves wrong, surface the divergence and update the plan and decisions explicitly rather than quietly building something else.

### 3. Inspect before deciding

- Trace the relevant behavior from entry point to side effects.
- Find established patterns, ownership boundaries, test commands, and release conventions.
- Inspect callers and consumers before changing a shared interface.
- Work with the current architecture unless it prevents a correct solution.

For defects, incidents, flaky behavior, or unclear failures, read [debugging.md](references/debugging.md) and establish the cause before choosing a fix.

### 4. Classify risk

Read [risk-model.md](references/risk-model.md) before changing anything beyond a local, reversible edit. Increase rigor when the change touches trust boundaries, sensitive data, persistent state, concurrency, distributed behavior, public contracts, migrations, or production delivery.

### 5. Design the smallest coherent change

- Prefer a local fix when the problem is local.
- Prefer existing project patterns, standard facilities, and already-approved dependencies.
- Add an abstraction only for demonstrated duplication, a stable domain boundary, or multiple real consumers.
- Include necessary validation, error handling, compatibility, observability, migration, and rollback behavior in the design.

Read [implementation.md](references/implementation.md) when choosing between more than one reasonable approach. Read [security-privacy.md](references/security-privacy.md) whenever data, identity, permissions, untrusted input, secrets, or dependencies are involved.

### 6. Implement end to end

- Keep the diff focused and internally consistent.
- Preserve externally observable behavior unless the change explicitly alters it.
- Make invalid states harder to represent or commit.
- Handle failures at the boundary with enough context for recovery and diagnosis.
- Do not hide uncertainty behind comments, broad exception handling, or silent fallback.

### 7. Verify with proportional evidence

Read [verification.md](references/verification.md) when deciding how much evidence the change needs. Start with focused checks, then broaden based on risk and blast radius. Inspect failures; do not merely run commands. Add regression evidence for defects and contract evidence for changed boundaries.

For deployment, migration, reliability, or distributed-system changes, also read [production-readiness.md](references/production-readiness.md).

### 8. Close the loop

State:

- what behavior changed;
- why the chosen approach fits the existing system;
- what was verified and the results;
- any unverified assumptions, limitations, or residual risk;
- when a plan workspace drove the work, that `progress.md` reflects the final task status, outcomes, and any recorded divergences.

Do not present optional future work as required work. Do not claim completion while required verification or implementation remains.

## Method Gotchas

- Reproduce before you fix: a change without a failing check that it turns green is a guess, not a fix.
- Read the callers before you touch a shared interface; the signature you are "cleaning up" is somebody's contract.
- A broad catch-all around the failing path usually hides the defect you were asked to fix — narrow it.
- Passing tests prove the tests passed, not that the change is correct; ask what they do not cover.
- "Temporary" fallbacks and silent defaults outlive every deadline; give them defined semantics or remove them.

## Worked Example

Request: "The list endpoint sometimes returns duplicate items across pages."

1. Contract: the same total set, no duplicates across pages, and stable order; the non-goal is changing the response schema.
2. Inspect: the query orders by a non-unique timestamp, so rows sharing a timestamp shift between pages as new rows arrive. Trace one concrete sequence that produces a duplicate.
3. Risk: a read-path defect with bounded blast radius, but it touches the public pagination contract, so preserve the response shape.
4. Smallest change: order by the timestamp plus a unique tiebreaker and page on that composite cursor instead of a numeric offset, which makes both the order and the cursor stable.
5. Verify: add a regression check that pages through rows sharing a timestamp and asserts the union has no duplicates; run it red before the fix and green after.
6. Close: behavior changed for pagination ordering only, verified by the new regression check; the residual risk is clients depending on offset paging, noted as a compatibility follow-up.

## Implementation Checklist

- [ ] The request is expressed as observable behavior with acceptance evidence.
- [ ] Callers and consumers of any changed interface were inspected first.
- [ ] Risk was classified and rigor scaled to trust boundaries, state, and contracts.
- [ ] The diff is the smallest coherent change and preserves unrelated behavior.
- [ ] A failing check was made to pass, and failures were inspected rather than only rerun.
- [ ] The close-out states what changed, what was verified, and any residual risk.
