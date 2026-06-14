# Quality Attribute Scenarios

Architecture quality is contextual. Do not optimize every quality equally or use labels such as "fast", "reliable", and "secure" without defining observable behavior.

## Write Measurable Scenarios

Describe each important scenario with:

1. **Source:** who or what initiates the stimulus.
2. **Stimulus:** request, change, failure, attack, or operating condition.
3. **Environment:** normal operation, peak load, degraded dependency, rollout, incident, or another relevant state.
4. **Artifact:** the affected system, component, data, or process.
5. **Response:** the expected behavior.
6. **Measure:** a threshold that determines success.

Example:

> During a regional dependency outage, authenticated users can still read previously stored records, with stale state clearly identified, and 99% of responses complete within two seconds.

## Consider Relevant Qualities

- **Correctness and integrity:** invariants, calculations, consistency, and prevention of loss, corruption, or duplication.
- **Reliability and resilience:** availability, degradation, fault containment, recovery time, and recovery point.
- **Security and privacy:** authorization, confidentiality, integrity, auditability, data minimization, and abuse resistance.
- **Performance and capacity:** latency, throughput, resource use, growth, and overload behavior.
- **Maintainability and changeability:** effort, risk, and lead time for likely changes.
- **Compatibility and interoperability:** old/new coexistence, external consumers, protocols, and data formats.
- **Usability and accessibility:** task success, understandable errors, keyboard access, assistive technology, and user control.
- **Operability and observability:** diagnosis, alerting, rollout, recovery, and ownership.
- **Safety and compliance:** unacceptable outcomes, controls, evidence, and regulatory obligations.

## Prioritize

- Rank scenarios by business importance and technical risk.
- State conflicts explicitly; improving one quality may weaken another.
- Define minimum acceptable thresholds before comparing alternatives.
- Distinguish current requirements from speculative future possibilities.
- Identify assumptions that need experiments, prototypes, or measurements.

## Foundational Sources

- SEI Quality Attribute Workshops: https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/
- SEI Architecture Tradeoff Analysis Method: https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/
- WCAG 2.2: https://www.w3.org/WAI/WCAG22/Understanding/intro
