---
name: apex-review
description: Use this skill when asked to review code, a diff, pull request, patch, migration, design implementation, or repository change. Perform a language- and framework-independent, risk-first review for correctness, security, data integrity, concurrency, compatibility, reliability, maintainability, performance, and missing verification. Report actionable findings by severity and location; do not use it to implement fixes unless explicitly requested.
license: MIT
---

# Apex Review

Find concrete defects and material risks introduced or exposed by the change. Prioritize user and system impact over style preferences.

## Workflow

### 1. Establish scope and intent

- Read repository instructions and the request.
- Inspect the complete diff and enough surrounding code to understand behavior.
- Identify the intended outcome, affected contracts, consumers, data, and production paths.
- Run focused checks or inspect history when they materially improve confidence.
- When a `.apex-design/<slug>/` planning workspace covers this change, review the diff against its `design.md` and `requirements.md`, and flag where the implementation diverges from the recorded decisions or fails an acceptance scenario.

### 2. Build a risk map

Read [review-checklist.md](references/review-checklist.md) to decide where to look first. Start with areas where failure would be severe or difficult to recover: trust boundaries, durable state, concurrency, shared contracts, migrations, and production delivery.

### 3. Validate each finding

Before reporting an issue:

- identify the changed behavior that causes or exposes it;
- trace a concrete input, state, or execution path;
- verify the impact and affected consumer;
- account for existing guards and project conventions;
- distinguish a defect from a preference or speculative concern.

Do not report a finding merely because code looks unusual.

### 4. Classify severity

Read [severity-model.md](references/severity-model.md) before assigning any severity label. Base severity on consequence, likelihood, exposure, blast radius, recoverability, and available controls. Do not inflate severity to make a point.

### 5. Report findings first

Order findings by severity. For each finding include:

- severity and concise title;
- precise file and line;
- triggering scenario or execution path;
- concrete impact;
- focused remediation direction.

Then state open questions or assumptions. Keep the summary secondary. If no findings meet the threshold, say so and identify meaningful residual risk or verification gaps.

## Review Order

1. Security, privacy, safety, and destructive data loss.
2. Correctness, invariants, and user-visible behavior.
3. Concurrency, transactions, ordering, and distributed failure.
4. Contracts, compatibility, migrations, rollout, and rollback.
5. Reliability, observability, and operational recovery.
6. Performance, capacity, and resource bounds.
7. Maintainability and unnecessary complexity.
8. Verification gaps that allow material regressions.

## Boundaries

- Do not apply fixes unless explicitly requested.
- Do not bury severe findings under summaries or style comments.
- Do not assume passing tests prove correctness.
- Do not report formatting or personal style unless it causes a concrete maintainability or correctness problem.
- Do not optimize for finding count. A short accurate review is better than a long speculative one.

## Method Gotchas

- Trace a concrete input, state, or path before reporting; "this looks wrong" is a question, not a finding.
- Severity is consequence times likelihood times exposure, not how surprising or unfamiliar the code looks.
- Account for existing guards and conventions before claiming a gap; the validation may live one layer up.
- A passing test suite is evidence the suite passed, not that the change is correct — review for what it omits.
- A short accurate review outranks a long speculative one; do not pad findings to look thorough.

## Worked Example

A diff adds a retrying call to a settlement service. Reported in the required format:

```text
[High] Persist an idempotency key before the settlement retry
path/to/settlement.ext:142

The new retry wraps a remote settle() call that carries no idempotency key.
When the first call succeeds but its response is lost, the retry settles a
second time and double-charges the customer. Persist a key before the first
attempt and send it on every retry so the service can collapse duplicates.
```

The finding traces a concrete path (success then lost response), states user impact (a double charge), gives a precise location, and points at a focused remediation rather than a style note.

## Review Checklist

- [ ] The full diff and enough surrounding code were read to understand behavior.
- [ ] The risk map starts at trust boundaries, durable state, concurrency, and contracts.
- [ ] Every finding traces a concrete input or path and accounts for existing guards.
- [ ] Severity reflects consequence, likelihood, and exposure rather than surprise.
- [ ] Findings come first, ordered by severity, each with location, scenario, impact, and fix.
- [ ] If nothing meets the threshold, residual risk and verification gaps are named.
