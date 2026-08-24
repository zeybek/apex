# Domain Language

Software fails more often because the team misunderstood the problem than because the code was wrong. Before designing a mechanism, establish what the domain concepts are, what they are called, and who can confirm how they behave. The vocabulary is the interface between the people who know the business, the engineers, and the agent that generates the code: an imprecise term produces a confidently wrong implementation that compiles and passes its tests.

## Discover the Language Already in Use

- Collect the names the repository already uses for the concepts in the request: module, type, table, column, event, endpoint, configuration, and user-facing label names, plus documentation.
- Collect the names the request and the people involved use in conversation. Where the code and the conversation disagree, record both; that gap is where implementation errors originate.
- Record what you found as facts in the brief. Ask about a term only when the repository and the request cannot settle it.

## One Name per Concept per Context

- Within one part of the system, use exactly one name for each concept and use it everywhere: documents, requirements, tasks, code, tests, and telemetry.
- When two areas use the same word for different things, or different words for the same thing, do not unify them. Treat them as separate contexts with their own vocabulary and translate explicitly at the seam. A "customer" in billing (a payer with invoices) and a "customer" in support (a profile with tickets) are different concepts that happen to share a word.
- Apparent duplication is not a reason to merge concepts. Merging two concepts because they share a name or a shape silently couples parts of the domain that change for different reasons.
- Prefer a domain term over a generic one (`item`, `data`, `record`, `info`, `manager`) whenever the concept has a name.

## Record the Glossary

Persist the agreed terms in the planning workspace's `glossary.md` (see [planning-workspace.md](planning-workspace.md)): the term, the context it belongs to, its meaning, what it must not be confused with, and who confirmed it. List forbidden synonyms so a later change cannot reintroduce "client" for "customer" by accident. Keep it short: a glossary nobody reads is worse than none.

## Protect the Language During Change

- Do not introduce a synonym for an existing term, rename a domain concept, or generalize two concepts into one without a recorded decision (`D-`) and, when the meaning is a business matter, the domain expert's confirmation.
- When an implementation needs a term the glossary lacks, add it to the glossary and cite the decision rather than inventing a local name in code.
- Watch for drift during review: technical terms replacing business terms, generic names where a domain term exists, and abstractions that erase a distinction the business relies on. Drift is quiet, compounds across changes, and is expensive to reverse once stakeholders and code no longer describe the same thing.

## Involve the People Who Know the Domain

- Name the domain expert, the person who can confirm how the business actually behaves in the edge cases, separately from the decision owner who signs off. They may be the same person; write both down.
- List the domain assumptions the design rests on and mark which still need the expert's confirmation. Treat plausible behavior inferred from code or general knowledge as an assumption, not a fact.
- The purpose of this work is that the people who will own the system understand the domain well enough to judge whether the plan is right. A glossary and a design document record that understanding; they do not replace it.

## Measures Serve Outcomes

A measurable requirement is a proxy for an outcome. Reducing memory use is not the same as reducing cost; raising test count is not the same as reducing defects. Record the outcome each measure serves so optimizing the proxy cannot quietly miss the goal.

## Foundational Sources

- Eric Evans, Domain-Driven Design reference (Ubiquitous Language, Bounded Context, knowledge crunching): https://www.domainlanguage.com/ddd/reference/
- Peter Naur, "Programming as Theory Building": https://pages.cs.wisc.edu/~remzi/Naur.pdf
- Margaret-Anne Storey, "From Technical Debt to Cognitive and Intent Debt": https://arxiv.org/abs/2603.22106
- "How AI Impacts Skill Formation" (randomized trial on assisted coding and comprehension): https://arxiv.org/abs/2601.20245
- Miłosz Smółka, "Domain-Driven Design matters more when AI writes your code": https://threedots.tech/post/ddd-and-ai-coding/
- Dennis Traub, "Your agent keeps using that word": https://dev.to/aws/your-agent-keeps-using-that-word--4g36
