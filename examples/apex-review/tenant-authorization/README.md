# Tenant Authorization Review

Use `apex-review` to identify a concrete cross-tenant authorization defect while avoiding speculative style findings.

## Learning Goal

Report the highest-impact actionable defect first, with a precise location, triggering path, impact, and focused remediation direction.

## Run

1. Copy [`workspace/`](workspace/) to a temporary directory.
2. Start a clean agent session in that directory with `apex-review`.
3. Provide [`prompt.md`](prompt.md) as the task.
4. Evaluate the review with [`rubric.md`](rubric.md).

This walkthrough is judgment-based and has no mechanical verifier.
