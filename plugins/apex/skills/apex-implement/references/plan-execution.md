# Plan Execution

When a planning workspace exists for the work — a `.apex-design/<slug>/` folder produced by the design workflow — implement against it and keep it current. The workspace is the contract; the code is the result.

## Adopt the workspace

1. If the user names an initiative, use it. Otherwise list `.apex-design/` and pick the one whose progress board is unfinished, or confirm with the user when several are in flight.
2. Read `brief.md`, `glossary.md`, `requirements.md`, `design.md`, and `plan.md` in full before changing any code. The brief gives intent and decisions, the glossary gives the names to use, requirements give acceptance, the design gives contracts and risks, and the plan gives the ordered tasks. A lighter workspace may omit files by design; the brief says which and why.
3. Check the brief's status. If it is still `drafting`, the decision owner has not confirmed the plan: restate the decision digest and the glossary in a few lines and confirm them before the first task, unless the owner already confirmed them in this session. Do not implement a plan nobody has agreed to.
4. Treat the recorded decisions (`D-`), requirements (`R-`), and tasks (`T-`) as the source of truth for scope. Work the plan, not a remembered version of the request.

## Execute the tasks

- Implement tasks in dependency order. Respect each task's `depends on` and do not start a task whose predecessors are not done.
- For each task, run its `verify` check and confirm its `done` condition before marking it complete. A task without its verification run is not done.
- Keep each task's change focused on what that task describes. Apply the same engineering rigor the rest of this skill requires — inspect callers, classify risk, preserve contracts, handle failure at boundaries.
- Use the glossary's terms in code, tests, and telemetry. When a task needs a term the glossary lacks, add it to the glossary with the decision that settled it rather than inventing a local name.
- Confirm each finished task still satisfies the requirements it cites; an implementation that drifts from `R-` acceptance is incomplete even if the code runs.

## Keep progress current

Update `progress.md` as you go, not only at the end:

- Move each task through pending, in progress, done, or blocked, and note the outcome or evidence.
- Record the current position so a future session can resume without re-reading everything.
- Capture decisions made or changed during implementation, and add them to the brief's decisions log when they alter intent.
- When a task is blocked, write what blocks it and what would unblock it, rather than silently skipping ahead.

## When the plan is wrong

The plan is a hypothesis about how to reach the outcome; implementation is where it meets reality.

- If a task cannot be done as written, or a better sequence emerges, surface the divergence and update the plan and decisions explicitly. Do not quietly implement something other than the plan.
- If new requirements or risks appear, add them with fresh identifiers and reflect them in the affected tasks.
- If the discovered cost or risk invalidates the chosen design, stop and route the decision back through design rather than forcing the plan through.

## Close out

- Reconcile the finished work against the requirements and the plan: every task done, every cited requirement met, divergences recorded.
- Write the owner handoff in `progress.md`: the two or three things a person must understand to change or operate this safely. Passing verification is not the same as the owner understanding why it works.
- State what changed, what was verified and how, and any residual risk — the same close-out the rest of this skill requires, now anchored to the workspace.

## Foundational Sources

- Incremental delivery and working software: https://martinfowler.com/articles/planning-extreme-programming.html
- IEEE 12207 software implementation process: https://standards.ieee.org/ieee/12207/5672/
