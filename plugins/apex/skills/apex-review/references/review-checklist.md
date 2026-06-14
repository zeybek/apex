# Risk-First Review Checklist

Use this checklist as prompts, not as a requirement to comment on every area. Follow the behavior and focus on risks relevant to the change.

## Intent and Scope

- Does the change satisfy the requested behavior?
- Is required end-to-end work missing?
- Did unrelated behavior change accidentally?
- Does the implementation fit ownership and established local patterns?

## Correctness and Data

- Are invariants preserved across success, failure, retry, and cancellation?
- Can data be lost, corrupted, duplicated, exposed, or left inconsistent?
- Are boundary values, absent values, invalid states, and error paths correct?
- Are transactions and state transitions atomic where required?
- Does cleanup preserve evidence or state needed for recovery?

## Security and Privacy

- Are authentication and authorization enforced at the authoritative boundary?
- Is untrusted input validated for syntax, semantics, size, and allowed action?
- Can commands, queries, templates, redirects, or paths be injected?
- Are secrets or sensitive data exposed through logs, errors, telemetry, or clients?
- Are privilege, tenant isolation, dependency, and supply-chain risks changed?
- Is collection, retention, or sharing of personal data justified and bounded?

## Concurrency and Distributed Behavior

- Can competing actors violate an invariant?
- Is a check followed by a write incorrectly assumed to be atomic?
- Are duplicate delivery, retries, ordering, idempotency, timeouts, and partial success handled?
- Can retry or fan-out amplify load or create unbounded work?
- Do old and new versions behave correctly while coexisting?

## Contracts and Compatibility

- Does the change alter an API, schema, event, file format, configuration, error, timing, ordering, or user workflow contract?
- Were callers, consumers, generated artifacts, and documentation updated?
- Is compatibility preserved or is the migration explicit?
- Can rollout be stopped, rolled back, or safely rolled forward?

## Reliability and Operations

- Are important failures visible and diagnosable?
- Are logs, metrics, traces, and alerts useful, bounded, and free of secrets?
- Are dependencies, overload, degradation, and recovery behavior defined?
- Are destructive or irreversible actions protected and auditable?
- Is operational ownership clear?

## Performance and Resources

- Does work, memory, storage, queueing, fan-out, or network usage remain bounded?
- Is there avoidable repeated I/O or an algorithmic regression on a hot path?
- Are performance claims supported by representative evidence?
- Could a cache introduce staleness, invalidation, privacy, or consistency defects?

## Maintainability

- Is the solution more complex than the demonstrated requirement?
- Does a new abstraction represent a stable boundary or only rename behavior?
- Does the change introduce a second competing pattern?
- Are errors, naming, and module boundaries understandable to future owners?
- Is broad cleanup obscuring the behavior change?

## Verification

- Do tests prove the changed behavior and important failure modes?
- Would the test fail for the regression it claims to cover?
- Are contract, migration, authorization, concurrency, and recovery risks tested at the appropriate boundary?
- Were important checks omitted or results misinterpreted?
- Are tests deterministic and meaningful rather than coupled to incidental implementation?

## User Interface and Accessibility

- Are loading, empty, error, success, and recovery states coherent?
- Are keyboard operation, focus, labels, contrast, and assistive technology behavior preserved?
- Are destructive actions and irreversible consequences clear?

## Foundational Sources

- Google Engineering Practices: https://google.github.io/eng-practices/review/
- NIST Secure Software Development Framework: https://csrc.nist.gov/pubs/sp/800/218/final
- OWASP Application Security Verification Standard: https://owasp.org/www-project-application-security-verification-standard/
- WCAG 2.2: https://www.w3.org/WAI/WCAG22/Understanding/intro
