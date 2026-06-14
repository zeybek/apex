# Finding Severity

Report only actionable defects or material risks. Severity reflects impact and urgency, not code style or reviewer confidence alone.

## Critical

A likely or readily exploitable issue that can cause catastrophic impact, such as broad compromise, severe safety harm, irreversible widespread data loss, or complete failure of a critical system.

Expected action: block release and remediate immediately.

## High

A concrete issue that can cause serious security, privacy, correctness, availability, financial, or data-integrity impact for important users or systems. It may have broad exposure, weak controls, or difficult recovery.

Expected action: block the change until addressed unless an accountable owner explicitly accepts and controls the risk.

## Medium

A real defect with meaningful but limited impact, or one requiring specific conditions. Recovery is practical and blast radius is bounded, but the issue should be fixed before normal release when feasible.

Expected action: address in the change or explicitly track with a justified plan.

## Low

A narrow, low-impact issue that is still concrete and worth correcting. It does not materially threaten the primary outcome.

Expected action: fix when cost-effective. Do not use Low for personal preferences.

## Not a Finding

Do not report:

- style preferences without concrete impact;
- speculative risks without a plausible execution path;
- pre-existing unrelated defects unless the change worsens or exposes them;
- optional improvements presented as required fixes;
- concerns already prevented by verified controls.

## Severity Factors

Assess:

- consequence to users, data, systems, and obligations;
- likelihood and ease of triggering;
- attacker or user exposure;
- blast radius and affected criticality;
- detectability and time to detection;
- recoverability and reversibility;
- strength of existing prevention and mitigation.

Use the highest credible consequence when likelihood is meaningful. Lower severity when strong verified controls substantially reduce exposure or impact.

## Finding Format

Use:

```text
[High] Prevent duplicate settlement during retry
path/to/file.ext:123

When the remote call succeeds but the process exits before recording success,
the retry issues the settlement again because the operation has no idempotency
key. This can charge a customer twice. Persist an idempotency key before the
call and reuse it across retries.
```

Keep the title imperative and specific. Explain the triggering scenario and impact before suggesting remediation.

## Foundational Sources

- FIRST Common Vulnerability Scoring System (CVSS): https://www.first.org/cvss/
- NIST SP 800-30, Guide for Conducting Risk Assessments: https://csrc.nist.gov/pubs/sp/800/30/r1/final
- OWASP Risk Rating Methodology: https://owasp.org/www-community/OWASP_Risk_Rating_Methodology
