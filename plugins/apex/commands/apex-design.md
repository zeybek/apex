---
description: Plan a change or new initiative end to end — ask clarifying questions, then write a committed .apex-design/<slug>/ planning workspace.
argument-hint: "what to design or build, even one line"
---

Use the apex-design skill to plan the following request, even if it is a single line:

$ARGUMENTS

Run the full design workflow:

1. Frame the problem, desired outcome, scope, non-goals, constraints, and decision owner.
2. Inspect the repository first and record what it already answers as facts, so you do not ask what you could read.
3. Ask clarifying questions for the decisions you cannot infer — audience, primary goal, priorities among competing qualities, constraints, scope, and success criteria. Ask in small prioritized batches with a recommended default, and record each answer as a numbered decision (`D-01`, `D-02`, …). Iterate until the plan is unambiguous.
4. Derive measurable requirements (`R-…`), compare credible alternatives on the same axes, recommend one with the reason it wins, and break the work into atomic, dependency-ordered tasks (`T-…`), each with the files it touches, a concrete verify, an acceptance condition, and the decisions and requirements it satisfies.
5. Persist everything as a planning workspace in `.apex-design/<NNN-slug>/` — `brief.md`, `requirements.md`, `design.md`, `plan.md`, `progress.md` — plus the workspace `README.md` index, carrying the `D-`/`R-`/`T-` identifiers so the implementation, review, and investigation workflows can consume it.

Produce and confirm the plan; do not start writing production code from this command. Hand execution to `/apex-implement`.
