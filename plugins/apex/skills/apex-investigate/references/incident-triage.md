# Incident Triage

Reduce harm first, then diagnose. Triage is deciding the response under uncertainty, not finding the root cause.

## Assess and Classify

- Determine scope, severity, and trajectory: who and what is affected, how badly, and whether impact is stable, growing, or recovering.
- Classify severity by consequence and reach, not by how surprising the failure is.
- Identify whether the system is safe-but-degraded or actively losing data, money, or safety margin.

## Stabilize

- Prefer the fastest safe mitigation: roll back the most recent change, disable the implicated feature, fail over, shed or throttle load, or restore a known-good state.
- Mitigate before the cause is fully understood when impact is ongoing; understanding can follow safely once harm is bounded.
- Avoid mitigations that destroy evidence unless stopping harm requires it; snapshot first when you can.

## Coordinate

- Name an incident owner who decides and a scribe who records the timeline.
- Communicate impact and status to affected stakeholders in plain terms: what is known, what is being done, and when the next update will come.
- Keep one source of truth for the current state.

## Preserve Evidence

- Capture logs, metrics, traces, queue and cache state, and configuration as they were during the incident.
- Record exact timestamps, versions, and the sequence of actions taken — including mitigations that did not work.

## Hand Off to Root-Cause

- Once impact is bounded, continue to diagnosis with the preserved evidence; mitigation is not a root cause.
- Track the durable fix and prevention separately from the incident's resolution.

## Foundational Sources

- Google SRE — Managing Incidents: https://sre.google/sre-book/managing-incidents/
- Google SRE — Emergency Response: https://sre.google/sre-book/emergency-response/
- NIST SP 800-61, Computer Security Incident Handling Guide: https://csrc.nist.gov/pubs/sp/800/61/r2/final
