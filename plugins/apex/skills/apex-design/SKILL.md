---
name: apex-design
description: Use this skill when turning a software change or new initiative into an implementable, reviewable plan before building — including a short or one-line request (such as a feature or page asked for in a single sentence) that should be scoped through clarifying questions first. Apply it to feature planning, architecture decisions, technical designs, API or schema evolution, data migrations, service boundaries, build-versus-buy choices, and reliability planning that need explicit requirements, alternatives, risks, contracts, and a sequenced task plan. It can be invoked directly or as a command, and it produces a persistent planning workspace that the implementation, review, and investigation workflows consume. Do not use it when a change is already decided and only needs implementation.
license: MIT
---

# Apex Design

Turn an ambiguous or consequential request into an implementable, reviewable decision and a sequenced plan. Optimize for the required outcomes and constraints, not for a preferred architecture style. Even a one-line request earns a full, deliberate planning pass.

## Workflow

### 1. Frame the decision

- State the problem, desired outcome, scope, non-goals, constraints, and decision owner.
- Separate verified facts, assumptions, and unresolved questions.
- Identify what must be decided now and what can remain reversible.

### 2. Inspect the existing system

- Read repository instructions, relevant code, diagrams, tests, schemas, operations documentation, and recent decisions.
- Map current responsibilities, dependencies, data flow, failure behavior, and operational ownership.
- Explain why the current design does not satisfy the requested outcome before proposing a replacement.

### 3. Clarify with the user

Read [clarifying-questions.md](references/clarifying-questions.md). After discovering everything the repository and request already answer, run an interactive clarifying-question loop on the decisions you cannot infer — audience, primary goal, priorities among competing qualities, constraints, explicit scope and non-goals, and success criteria.

- Ask in small, prioritized batches; offer concrete options with a recommended default.
- State the assumption you will proceed with if a question goes unanswered.
- Record each resolved answer as a numbered decision (`D-01`, `D-02`, …).
- Iterate until the remaining unknowns are safe assumptions with revisit conditions, not open scope.

### 4. Define quality scenarios

Read [quality-attributes.md](references/quality-attributes.md) when a goal is stated as an adjective such as "scalable", "secure", or "maintainable". Convert vague goals into prioritized, measurable scenarios with identifiers (`R-01`, `R-02`, …). Include important failure and abuse scenarios.

### 5. Develop credible alternatives

Read [architecture-tradeoffs.md](references/architecture-tradeoffs.md) when more than one option is credible. Include the current design when retaining it is credible. Compare alternatives against the same outcomes, quality scenarios, constraints, delivery cost, and operational burden.

### 6. Choose and pressure-test

- Recommend one option and state why it wins under the stated priorities.
- Identify tradeoffs, sensitivities, failure modes, irreversible decisions, and assumptions that could invalidate the choice.
- Prefer reversible steps when evidence is weak.

For public interfaces, persistent data, events, or rolling deployments, read [contracts-and-migrations.md](references/contracts-and-migrations.md).

### 7. Make the design executable

Specify enough detail for implementation and review:

- component responsibilities and ownership;
- data and control flow;
- external and internal contracts;
- invariants, validation, and failure behavior;
- security, privacy, and access boundaries;
- observability and operational ownership;
- migration, rollout, rollback or roll-forward;
- verification strategy and acceptance evidence.

Break the work into atomic, dependency-ordered tasks (`T-01`, `T-02`, …), each with the files it touches, a concrete verification, an acceptance condition, and the decisions and requirements it satisfies. Avoid implementation detail that does not affect a decision, contract, or risk.

### 8. Record the decision and write the workspace

Use [decision-record.md](references/decision-record.md) for the decision itself. Then persist the full result as a planning workspace following [planning-workspace.md](references/planning-workspace.md): create `.apex-design/<NNN-slug>/` in the target repository with `brief.md`, `requirements.md`, `design.md`, `plan.md`, and `progress.md`, plus the workspace `README.md` index. Carry the `D-`, `R-`, and `T-` identifiers across the files so the reasoning stays traceable. This workspace is the handoff that the implementation, review, and investigation workflows read.

## Output Standard

A strong design enables another engineer to understand the decision, challenge its assumptions, implement it from the plan, verify it, operate it, and recognize when it should be revisited.

## Method Gotchas

- Discover before you ask: a question whose answer is already in the repository wastes trust; an assumption that should have been a question produces the wrong plan.
- Scope creep hides in vaguely written non-goals; state what you are deliberately not solving as precisely as what you are.
- The current design is a real alternative — evaluate it on the same axes instead of strawmanning it to justify a rewrite.
- A "simple" option that ignores a required quality scenario is not simple, it is incomplete; price the missing work before comparing.
- Reversibility is a feature: when evidence is weak, prefer a cheaper undoable step over a confident one-way decision.
- Most design disagreements are really disagreements about priorities; surface the priority order before debating mechanisms.
- The workspace records the decision; it does not make it. Do not let producing files substitute for the reasoning behind them.

## Worked Example

Request (one line): "Build me a landing page."

1. Frame: the outcome is a page that converts a defined visitor into a defined action; the decision owner is the requester. Reversible to rebuild, but the primary goal shapes everything downstream.
2. Inspect: the repository has an existing component library and brand tokens; record those as facts so they are not re-asked.
3. Clarify: ask the few decisions that change the plan — who the audience is, the single primary call to action, must-have sections, and how success is measured. Record answers as `D-01` (audience), `D-02` (primary CTA: start free trial), `D-03` (launch deadline).
4. Quality scenarios: `R-01` first contentful paint under two seconds on a mid-range phone; `R-02` the CTA is reachable by keyboard and screen reader; abuse scenario `R-03` the contact form resists spam submissions.
5. Alternatives: (a) a static page in the existing framework; (b) a page builder dependency; (c) a bespoke service. Compare on delivery cost, performance, and maintainability.
6. Choose (a): it meets the performance and accessibility scenarios with the existing stack and no new dependency; record the spam-control risk with a control.
7. Executable: tasks `T-01` scaffold the route, `T-02` build the hero and CTA, `T-03` add the form with validation and spam control, each with a concrete verify and acceptance.
8. Workspace: write `.apex-design/001-landing-page/` with the brief, requirements, design, plan, and progress board, carrying the `D-`/`R-`/`T-` identifiers.

## Design Checklist

- [ ] Problem, outcome, scope, non-goals, and decision owner are written down.
- [ ] Everything inferable was discovered before asking, and remaining ambiguity was resolved as numbered decisions.
- [ ] Vague goals are converted into prioritized, measurable quality and abuse scenarios with identifiers.
- [ ] The current design is included as an alternative and compared on the same axes.
- [ ] One option is recommended with an explicit reason it wins under the stated priorities.
- [ ] Contracts, failure behavior, migration, rollback, and verification are specified.
- [ ] The plan is a sequence of atomic tasks, each with files, verify, acceptance, and the decisions and requirements it satisfies.
- [ ] A `.apex-design/<slug>/` workspace persists the brief, requirements, design, plan, and progress with traceable identifiers.
