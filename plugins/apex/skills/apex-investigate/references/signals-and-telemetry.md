# Signals and Telemetry

Read logs, metrics, and traces to locate a failure without being misled by aggregation.

## Follow One Real Case

- Trace a single failing request or event end to end across services using a correlation or trace identifier.
- Anchor the investigation in one concrete failure before generalizing from dashboards.

## Use the Three Signals Together

- Metrics show that something is wrong and when: request rate, errors, duration, and saturation.
- Traces show where time and failures occur along a request's path.
- Logs show why at a specific step; prefer structured, correlated logs over free text.

## Avoid Aggregation Traps

- Averages hide tails; read percentiles and the distribution, not just the mean.
- Sampling means absence of evidence is not evidence of absence; know your sampling rate.
- Align clocks and time zones across systems before correlating by timestamp.
- A symptom metric such as latency or error rate is not its driver; look for saturation, contention, a poison input, or a failing dependency behind it.

## Correlate Change with Effect

- Overlay deploys, configuration changes, and traffic shifts onto the failure timeline.
- Correlation in time is a lead, not a conclusion; require a mechanism that connects the change to the failure.

## Foundational Sources

- Google SRE — Monitoring Distributed Systems (the four golden signals): https://sre.google/sre-book/monitoring-distributed-systems/
- OpenTelemetry documentation: https://opentelemetry.io/docs/
- Brendan Gregg — The USE Method: https://www.brendangregg.com/usemethod.html
