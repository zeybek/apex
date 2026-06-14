---
name: apex-investigate
description: Use this skill when investigating a failure whose cause is not yet known — a production incident or outage, a regression, an intermittent or flaky failure, a performance degradation, corrupted or surprising data, or a bug report you must diagnose before fixing. Apply it to triage severity and mitigation, gather and preserve evidence, form and test hypotheses, bisect and localize the cause across components and time, read logs, metrics, and traces, confirm a root cause by mechanism, and record findings in a blameless writeup. Do not use it when the change is already understood and only needs implementation (use apex-implement) or when reviewing a proposed change (use apex-review).
license: MIT
---

# Apex Investigate

Find the cause of an unknown failure and decide the right response. Separate stopping the harm (mitigation) from understanding the mechanism (root cause); do not let one stand in for the other.

## Workflow

### 1. Triage and stabilize

- Establish impact: who and what is affected, severity, blast radius, and whether the failure is stable, growing, or recovering.
- Decide whether to mitigate now — roll back, disable a feature, fail over, shed or throttle load, restore a known-good state — before diagnosing. For active incidents, reducing harm comes first.
- Preserve evidence before it is lost: snapshot logs, metrics, traces, and queue or cache state before restarting or cleaning up.
- Name an owner and one place to record the timeline.

For active incidents and outages, read [incident-triage.md](references/incident-triage.md).

### 2. Define the failure precisely

- State expected versus actual behavior in observable terms.
- Capture the affected inputs, users, environment, version, timing, and frequency.
- Establish when it started and what changed around that time: deploys, configuration, data, dependencies, or traffic.
- Distinguish a new failure from a long-standing one that was only just noticed.

### 3. Reproduce and bound

Read [evidence-and-bisection.md](references/evidence-and-bisection.md) when the cause is not obvious from the definition.

- Build the smallest reliable reproduction you can; if you cannot reproduce, treat that as uncertainty, not resolution.
- Determine what the failure depends on: data, configuration, version, timing, load, ordering, identity, or environment.
- Compare a working case against a failing one and bisect the difference — across code history, component boundaries, deployments, data partitions, or time.

### 4. Read the signals

Read [signals-and-telemetry.md](references/signals-and-telemetry.md) when logs, metrics, or traces are involved.

- Follow one real failing request or event end to end across logs, traces, and metrics.
- Correlate by time, identifier, and deployment; align clocks and account for sampling and aggregation.
- Distinguish a symptom (errors, high latency) from its driver (saturation, contention, a poison input, a failing dependency).

### 5. Form and test hypotheses

- List plausible causes that fit the current evidence; rank them by likelihood and by cost to test.
- Test the highest-information, lowest-cost distinction first; change one variable at a time.
- Prefer evidence that can disprove a hypothesis over evidence that merely confirms it.
- Record what each test rules in or out so the path stays auditable.

### 6. Confirm the cause by mechanism

A confirmed root cause connects four things: the trigger, the violated invariant or defective behavior, why existing controls did not prevent or detect it, and the observed impact. Do not stop at a label such as "race condition", "bad data", or "flaky"; explain the mechanism and show the evidence chain.

### 7. Decide the response and verify

- Separate the immediate mitigation, the durable fix, and the prevention or detection improvements.
- Hand the durable fix to implementation with the mechanism, the reproduction, and the affected scope. Building the fix is apex-implement's job.
- Verify the mitigation actually reduced impact, and define how you will confirm the durable fix addresses the mechanism, not just the symptom.

### 8. Capture what was learned

Write a short blameless account: timeline, impact, root cause as a mechanism, what helped and what slowed the investigation, and concrete prevention or detection follow-ups with owners. Focus on systemic causes, not individual blame.

## Method Gotchas

- Mitigation is not diagnosis: a rollback stops the harm but does not tell you why — keep investigating after the bleeding stops.
- "Cannot reproduce" is a state of uncertainty, not a resolution; record the conditions you have not yet ruled out.
- Correlation on a dashboard is a lead, not a cause; a spike that lines up in time still needs a mechanism connecting it to the failure.
- The first plausible cause is a hypothesis, not a verdict — look for the evidence that would disprove it.
- A label like "flaky", "transient", or "bad data" is where the investigation starts, not where it ends.
- The change that exposed a latent bug is not always the change that introduced it.

## Worked Example

Report: "Checkout error rate jumped from 0.1% to 4% at 14:05 and is still elevated."

1. Triage: ongoing and revenue-affecting, so mitigate first. The 14:00 deploy is the prime suspect; roll it back. Errors fall to 0.3% by 14:20 — harm reduced, but not zero, so the rollback is mitigation, not proof of cause.
2. Define: HTTP 500 on POST /checkout, only for carts containing a gift card; started 14:05; about 4% of checkouts, matching the gift-card fraction.
3. Reproduce and bound: a cart with a gift card reproduces the 500 reliably; without one it succeeds. The dependency is "gift card present."
4. Signals: tracing one failing request shows a timeout calling the balance service, whose p99 latency went from 40ms to 30s at 14:05.
5. Hypotheses: (a) our deploy changed the balance call; (b) the balance service itself degraded. Cheapest test first — the balance service's own dashboard shows its regression began at 14:05 with its own deploy, not ours.
6. Mechanism: the balance deploy added a synchronous external call with no timeout; under load it exhausted its thread pool, so callers timed out and checkout returned 500. Our 14:00 deploy was coincidental.
7. Response: our rollback only partially masked it; the durable fix lives in the balance service (timeout plus bulkhead). Hand off with the mechanism and reproduction.
8. Learn: detection gap — we alerted on checkout 500s but not on the dependency's latency. Add a dependency-latency alert and a client-side timeout as defense in depth.

## Investigation Checklist

- [ ] Impact and severity are established, and harm is mitigated before deep diagnosis when the failure is ongoing.
- [ ] Evidence (logs, metrics, traces, failing-state snapshot) is preserved before anything is restarted or cleaned up.
- [ ] The failure is defined in observable terms with its start time and what changed around it.
- [ ] The failure is bounded to the dimensions it depends on, via a reproduction or differential comparison.
- [ ] More than one hypothesis was tested, cheapest discriminating test first, changing one variable at a time.
- [ ] The root cause is stated as a mechanism with an evidence chain, not a label.
- [ ] Mitigation, durable fix, and prevention are separated, and findings are captured blamelessly.

## Output Standard

A strong investigation lets another engineer follow the evidence chain from trigger to impact, reproduce the failure, trust the root cause as a mechanism rather than a label, and act on a clear separation of mitigation, fix, and prevention.
