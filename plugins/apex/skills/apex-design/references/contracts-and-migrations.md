# Contracts and Migrations

Treat evolution as a period in which multiple versions, states, and consumers may coexist. Deployment is not an atomic replacement unless proven otherwise.

## Identify Contracts

Include all behavior consumers may rely on:

- APIs, commands, errors, schemas, events, protocols, and file formats;
- configuration names, defaults, and feature controls;
- ordering, timing, idempotency, retry, and consistency semantics;
- user workflows, accessibility behavior, and operational procedures.

Classify consumers, owners, compatibility commitments, and deprecation paths.

## Compatibility Rules

- Prefer additive, backward-compatible changes.
- Make readers tolerate old and new forms before writers emit new forms.
- Preserve semantic behavior, not only syntactic validity.
- Version only when compatibility cannot be maintained.
- Define deprecation signals, migration support, and removal criteria.
- Test representative old and new producers and consumers together.

## Use Expand-Migrate-Contract

1. **Expand:** introduce compatible schema, API, event, or code capable of handling old and new forms.
2. **Migrate:** move data and consumers incrementally; observe progress and correctness.
3. **Contract:** remove old behavior only after usage and rollback dependence have ended.

## Design Data Migrations

- Preserve invariants throughout the migration, not only at the end.
- Make backfills bounded, observable, resumable, and idempotent.
- Define behavior for partial completion, retries, concurrent writes, and failure recovery.
- Validate counts, integrity, and application behavior before cleanup.
- Keep backups and restoration evidence when destructive loss is plausible.
- Prefer roll-forward when rollback cannot safely restore the previous data representation.

## Design API and Event Evolution

- Distinguish absence, defaults, and explicit values.
- Avoid changing the meaning of an existing field.
- Define unknown-field, duplicate, ordering, and delivery behavior.
- Coordinate contract changes with consumers rather than assuming adoption.
- Measure remaining old-version usage before removal.

## Foundational Sources

- AWS rollback-safe deployments: https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/
- Microsoft REST API Guidelines: https://github.com/microsoft/api-guidelines
