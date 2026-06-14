# Clarifying Questions

A short or one-line request ("build me a landing page", "add notifications") rarely contains enough to plan well. Resolve the genuine ambiguity through a focused question loop before committing to a design — but discover first, so you only ask what the repository and request cannot answer.

## Discover before asking

1. Read repository instructions, existing code, configuration, schemas, tests, and recent history.
2. Answer every question you can from that evidence, and record those answers as facts in the brief.
3. Ask the user only about decisions that remain genuinely undetermined and that would change the plan.

Asking what you could have read erodes trust; guessing what you should have asked produces the wrong plan. Aim between the two.

## Run the loop

- Ask in small, prioritized batches, starting with the decisions that most change scope, cost, or risk.
- Prefer concrete options with a recommended default over open prompts; a user can react to "A, B, or C — I would lean B because …" faster than to "what do you want?".
- State the assumption you will proceed with if a question is left unanswered, so silence still moves the plan forward.
- Record each resolved answer as a numbered decision (`D-01`, `D-02`, …) in `brief.md`, with the question and the answer.
- Stop when the remaining unknowns are small enough to be assumptions with named revisit conditions, not open scope. Do not interrogate past the point of usefulness.

## What to ask about

- **Audience and context:** who uses this, on what devices or environments, and what they are trying to accomplish.
- **Primary goal and success:** the single most important outcome, the call to action or key result, and how success is measured.
- **Scope and non-goals:** what is explicitly included now, what is deferred, and what is deliberately excluded.
- **Priorities and tradeoffs:** which quality matters most when two conflict — speed, cost, reliability, accessibility, security, or time to ship.
- **Constraints:** existing stack and conventions, deadlines, budget, compliance, branding, and data handling obligations.
- **Inputs and integrations:** required data, upstream and downstream systems, authentication, and third-party services.
- **Content and states:** the real content, plus empty, loading, error, partial, and abuse states the result must handle.
- **Acceptance:** the concrete conditions under which the user would call the work done.

## What not to do

- Do not ask questions whose answers are already in the repository or the request.
- Do not ask for decisions you can safely defer; record them as assumptions with a revisit condition instead.
- Do not bundle ten questions at once; batch and prioritize so the user can answer without fatigue.
- Do not let the loop run forever — converge on enough certainty to plan, not on perfect certainty.

## Foundational Sources

- Requirements elicitation, SWEBOK Guide: https://www.computer.org/education/bodies-of-knowledge/software-engineering
- INVEST criteria for well-formed scope: https://www.agilealliance.org/glossary/invest/
- Karl Wiegers, "Software Requirements" elicitation practice: https://www.karlwiegers.com/
