# Evaluation Rubric

A strong result:

- states the outcome, constraints, non-goals, assumptions, and decision owner;
- converts availability and auditability into measurable quality scenarios;
- compares retaining the modular monolith, stronger in-process isolation, and service extraction on consistent criteria;
- addresses data ownership, transaction boundaries, failure behavior, migration, rollback, operations, and team capability;
- establishes whether billing is a distinct context with its own vocabulary (invoice, payment attempt, reconciliation) and treats the shared customer and order tables as a boundary leak to be named and translated, not silently unified;
- names who confirms the billing and audit rules (domain expert) separately from who signs off on the decision;
- recommends one option with explicit reasons, risks, controls, and revisit conditions;
- chooses a reversible first step when evidence does not justify immediate extraction.
