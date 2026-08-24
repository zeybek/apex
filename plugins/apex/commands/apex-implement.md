---
description: Execute a planned .apex-design/<slug>/ workspace (or a directly described change) and keep its progress board current.
argument-hint: "initiative slug, or the change to implement"
---

Use the apex-implement skill to carry out the work described by:

$ARGUMENTS

If a `.apex-design/<slug>/` planning workspace applies — named in the arguments, or the unfinished one under `.apex-design/`:

1. Read its `brief.md`, `glossary.md`, `requirements.md`, `design.md`, and `plan.md` in full before changing any code. If the brief is still `drafting`, restate the decision digest and confirm it with the decision owner before the first task.
2. Implement the plan's tasks in dependency order, using the glossary's terms. Run each task's `verify` and confirm its `done` condition before marking it complete.
3. Update `progress.md` as you go — task status, outcomes, blockers, and current position — not only at the end.
4. If a task cannot be done as written, or the design proves wrong, surface the divergence and update the plan and decisions explicitly rather than silently building something else.

If no workspace applies, implement the change directly with the skill's normal risk-based workflow. Close out by stating what changed, what was verified and how, any residual risk, and the two or three things the owner must understand to change it safely.
