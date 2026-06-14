# Security and Privacy

Apply security and privacy throughout the change, not as a final checklist. Increase depth based on exposure, data sensitivity, and consequence.

## Quick Threat Review

Identify:

- assets and sensitive data;
- actors and trust boundaries;
- entry points and privileged operations;
- attacker-controlled inputs and dependencies;
- abuse cases, failure impact, and existing controls.

For high-risk changes, make threats, mitigations, and residual risk explicit.

## Security Rules

- Authenticate identity before relying on it.
- Authorize every protected operation at the authoritative boundary.
- Default to least privilege and deny by default.
- Validate syntax, semantics, size, and allowed operations for untrusted input.
- Use parameterized or structured APIs instead of constructing commands, queries, or markup from strings.
- Use established cryptographic libraries and approved algorithms. Do not invent cryptographic protocols.
- Keep secrets out of source, logs, errors, telemetry, and client-visible data.
- Protect sensitive data in transit and at rest according to its risk.
- Bound resource consumption to reduce denial-of-service exposure.
- Preserve auditability for security-relevant actions without logging secrets.
- Treat dependency and build provenance as part of the security boundary.

## Privacy Rules

- Identify what personal or sensitive data is collected, why it is needed, who receives it, and how long it is retained.
- Minimize collection and retention to the stated purpose.
- Avoid exposing sensitive data through logs, analytics, debugging, caches, or error messages.
- Preserve deletion, correction, consent, and access obligations when relevant.
- Evaluate whether new data processing changes user expectations or legal obligations.

## Review Triggers

Require stronger analysis when changing:

- authentication, authorization, sessions, credentials, or account recovery;
- file upload, deserialization, command execution, templates, or redirects;
- tenant isolation, administrative actions, or privilege boundaries;
- personal, financial, health, location, or secret data;
- cryptography, tokens, signing, random generation, or key management;
- dependencies, build pipelines, release artifacts, or provenance.

## Evidence

Use applicable evidence such as:

- authorization and isolation tests;
- negative and abuse-case tests;
- dependency and secret scanning;
- threat-model review;
- security control verification;
- audit and redaction checks.

## Foundational Sources

- NIST Secure Software Development Framework: https://csrc.nist.gov/pubs/sp/800/218/final
- OWASP Application Security Verification Standard: https://owasp.org/www-project-application-security-verification-standard/
- NIST Privacy Framework: https://www.nist.gov/privacy-framework
