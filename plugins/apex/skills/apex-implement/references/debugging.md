# Evidence-Driven Debugging

Debug to establish cause, not merely to make the visible symptom disappear. Keep investigation separate from remediation until the evidence supports a specific explanation.

## Define the Failure

- Describe expected and actual behavior in observable terms.
- Capture the affected users, inputs, environment, timing, and frequency.
- Establish when the failure began and what changed around that time.
- Preserve useful evidence before restarting, cleaning state, or modifying the system.

## Reproduce and Bound

- Create the smallest reliable reproduction when feasible.
- Determine whether the failure depends on data, configuration, version, timing, load, ordering, identity, or environment.
- Compare working and failing cases.
- Narrow the failure across component, deployment, and dependency boundaries.
- Treat inability to reproduce as uncertainty, not proof that the issue is resolved.

## Form and Test Hypotheses

- List plausible causes supported by current evidence.
- Test the highest-information, lowest-cost distinction first.
- Change one meaningful variable at a time.
- Use logs, traces, metrics, debuggers, queries, history, and controlled experiments as appropriate.
- Prefer evidence that can disprove a hypothesis.
- Record discoveries that affect the final explanation.

## Establish Root Cause

A useful root-cause explanation connects:

1. the triggering conditions;
2. the defective behavior or violated invariant;
3. why existing controls did not prevent or detect it;
4. the observed user or system impact.

Do not stop at labels such as "race condition", "bad data", or "human error". Explain the mechanism.

## Remediate the Class of Failure

- Fix the violated invariant or incorrect boundary behavior, not only one observed input.
- Add a regression test that fails for the original mechanism when feasible.
- Consider whether related paths share the same defect.
- Add prevention, detection, containment, or recovery controls proportional to impact.
- Remove temporary diagnostics that are unsafe or noisy; retain useful observability.

## Verify the Explanation and Fix

- Reproduce the failure before the fix when feasible.
- Show that the fix prevents the same mechanism.
- Run broader checks based on blast radius.
- Verify that the remediation does not introduce compatibility, performance, security, or operational regressions.
- State uncertainty and remaining risk when the cause cannot be fully proven.

## Foundational Sources

- David J. Agans, "Debugging: The Nine Indispensable Rules": https://debuggingrules.com/
- Google SRE postmortem and root-cause practices: https://sre.google/sre-book/postmortem-culture/
- IEEE SWEBOK software maintenance topics: https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics
