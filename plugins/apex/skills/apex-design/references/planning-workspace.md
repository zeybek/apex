# Planning Workspace

A planning workspace turns a design into durable, reviewable project documents that the implementation, review, and investigation workflows can read later. Create it under `.apex-design/` in the target repository so it is versioned and committed alongside the code it describes.

## Layout

```text
.apex-design/
  README.md                     index of initiatives and how the workspace works
  <NNN-slug>/                    one folder per initiative, e.g. 001-landing-page
    brief.md                    problem, outcome, scope, decisions log
    glossary.md                 domain terms by context, forbidden synonyms, who confirmed them
    requirements.md             measurable quality and acceptance scenarios
    design.md                   alternatives, recommendation, contracts, operations
    plan.md                     sequenced atomic tasks with verification
    progress.md                 status board and session memory
```

- `<NNN>` is a zero-padded sequence number (`001`, `002`, …). `slug` is a short hyphen-case name derived from the initiative.
- Pick the next free number by reading existing folders. Never renumber or rewrite a shipped initiative's history; supersede it with a new one and link between them.
- Create `.apex-design/README.md` on the first initiative if it does not exist.

## Traceability identifiers

Stable identifiers let every later artifact cite the reasoning behind it.

- `D-01`, `D-02`, … decisions resolved with the user (recorded in `brief.md`).
- `R-01`, `R-02`, … requirements and acceptance scenarios (in `requirements.md`).
- `T-01`, `T-02`, … plan tasks (in `plan.md`).

Each requirement cites the decisions it depends on. Each task cites the decisions and requirements it satisfies. Each glossary term that was chosen or changed cites the decision that settled it. Never reuse or renumber an identifier once other files reference it.

## File formats

Use these as templates. Replace every `<fill: …>` marker with real content; delete sections that genuinely do not apply rather than leaving them empty.

### brief.md

```text
# <fill: initiative title>

- Status: drafting | planned | in progress | done | superseded
- Decision owner: <fill: who signs off>
- Domain expert: <fill: who confirms how the business behaves in the edge cases; may be the decision owner>
- Created: <fill: date>

## Problem and outcome
<fill: the problem in one or two sentences, and the observable outcome that means it is solved>

## Scope
<fill: what is in scope>

## Non-goals
<fill: what is deliberately not being solved, stated as precisely as the scope>

## Constraints
<fill: technical, time, compliance, or compatibility constraints>

## Facts, assumptions, open questions
- Fact: <fill: something verified from the repository or the user>
- Assumption: <fill: something taken as true but not verified>
- Domain assumption: <fill: how the business is believed to behave; needs the domain expert's confirmation>
- Open question: <fill: still unresolved; resolve through the clarifying loop>

## Decisions log
- D-01 — <fill: the question> -> <fill: the answer> (asked <fill: date>)
- D-02 — <fill: the question> -> <fill: the answer>
```

### requirements.md

```text
# Requirements — <fill: initiative title>

Each requirement is observable or measurable, names the outcome it serves, and names the decisions it rests on.

- R-01 — <fill: requirement stated as observable behavior with a threshold> (serves: <fill: the outcome this measure is a proxy for>; depends on D-01)
- R-02 — <fill: acceptance scenario: given/when/then in plain language> (depends on D-02)

## Failure and abuse scenarios
- R-0n — <fill: what must not happen, and how the system resists it>
```

### glossary.md

The domain vocabulary this initiative relies on. Follow [domain-language.md](domain-language.md). One name per concept per context; a term that means something different elsewhere in the system gets its own row with its own context.

```text
# Glossary — <fill: initiative title>

| Term | Context | Meaning | Not to be confused with | Confirmed by |
|---|---|---|---|---|
| <fill: term> | <fill: module or area> | <fill: one-sentence meaning> | <fill: similar terms in other contexts> | <fill: expert or decision, e.g. D-02> |

## Forbidden synonyms
- <fill: synonym> -> use <fill: term> (<fill: context>)

## Open terms
- <fill: a concept that still has more than one name or no agreed meaning>
```

### design.md

This is the decision record. Follow [decision-record.md](decision-record.md) for the full structure. Open with a decision digest short enough that the decision owner will actually read it; the rest of the file is reference. At minimum capture:

```text
# Design — <fill: initiative title>

## Decision digest
<fill: five lines or fewer: what was decided, why it wins, the biggest tradeoff, the riskiest assumption, and what would reopen it>

## Recommendation
<fill: the chosen option, stated first, and why it wins under the stated priorities>

## Alternatives considered
<fill: credible options including keeping the current design, compared on the same axes>

## Contracts and data
<fill: external and internal contracts, data and control flow, invariants>

## Failure, security, and privacy
<fill: failure behavior, trust boundaries, access, sensitive data handling>

## Operations
<fill: observability, ownership, migration, rollout, rollback or roll-forward>

## Risks and revisit conditions
<fill: key risks with controls, and what would trigger reopening this decision>
```

### plan.md

Tasks are atomic, ordered by dependency and reversibility, and independently verifiable.

```text
# Plan — <fill: initiative title>

- T-01 — <fill: task title>
  - files: <fill: files or areas this task touches>
  - action: <fill: the concrete change>
  - verify: <fill: a concrete check that proves the task works>
  - done: <fill: the acceptance condition>
  - satisfies: D-01, R-01
- T-02 — <fill: task title>
  - depends on: T-01
  - files: <fill: …>
  - action: <fill: …>
  - verify: <fill: …>
  - done: <fill: …>
  - satisfies: R-02
```

### progress.md

The implementation workflow keeps this current. Initialize every task as pending.

```text
# Progress — <fill: initiative title>

- Updated: <fill: date>
- Current position: <fill: which task is active, or "not started">

## Status board
- T-01 — pending | in progress | done | blocked — <fill: note>
- T-02 — pending

## Decisions and blockers
<fill: decisions made or changed during implementation, and anything blocking progress>

## Owner handoff
<fill: filled at close-out: the two or three things a person must understand to change or operate this safely, such as the domain rule it enforces, the invariant it relies on, and where it will break first>

## Session memory
<fill: context a future session needs to resume without re-reading everything>
```

### README.md (workspace index)

```text
# Planning workspace

This folder holds design and planning documents for non-trivial changes. Each
subfolder is one initiative with a brief, glossary, requirements, design, plan,
and progress board. Identifiers (D- decisions, R- requirements, T- tasks)
connect the reasoning across files.

## Initiatives
- 001-<slug> — <fill: one-line summary> — <fill: status>
```

## Proportionality and confirmation

Scale the written workspace to the risk of the work, using the same dimensions as the implementation risk model. Uncertainty counts: a one-line brief for consequential work is high-uncertainty and earns the full workspace. A small, well-understood, low-risk change earns `brief.md`, `glossary.md`, and `plan.md`; add `requirements.md` and `design.md` when quality scenarios, alternatives, or contracts genuinely need to be argued. When `design.md` is omitted, put the decision digest at the top of `brief.md`. State in the brief which files were deliberately omitted and why. A high-level sketch that everyone has read beats a complete specification nobody has.

The brief's status moves from `drafting` to `planned` only after the decision owner has confirmed the decision digest and the glossary. Implementation does not start from a `drafting` workspace.

## Guardrails

- Keep facts, assumptions, and open questions distinct; never present an assumption as a fact.
- Use the glossary's terms everywhere in the workspace; do not introduce a synonym or merge two contexts' concepts without a recorded decision.
- The value of the workspace is that the people who own the system understand the plan; a workspace the decision owner has not read is an artifact, not a plan.
- Write non-goals as precisely as scope so the plan does not drift.
- Prefer reversible early tasks when evidence is weak, and order the plan so the riskiest assumptions are tested soonest.
- The workspace is documentation, not a substitute for the design reasoning; it records the decision, it does not replace making one.

## Foundational Sources

- Architecture Decision Records: https://adr.github.io/
- IEEE 830 software requirements practice: https://standards.ieee.org/ieee/830/1222/
- Agile planning and incremental delivery: https://martinfowler.com/articles/planning-extreme-programming.html
- Eric Evans, Domain-Driven Design reference (Ubiquitous Language, Bounded Context): https://www.domainlanguage.com/ddd/reference/
