---
description: Run a risk-first review of a change, checking it against its .apex-design/<slug>/ design and requirements when one exists.
argument-hint: "diff, pull request, or area to review"
---

Use the apex-review skill to review:

$ARGUMENTS

When a `.apex-design/<slug>/` planning workspace covers the change, review the diff against its `design.md` and `requirements.md` in addition to the standard risk-first checks, and flag where the implementation diverges from the recorded decisions or fails an acceptance scenario.

Report findings first, ordered by severity, each with a precise location, the triggering scenario, the concrete impact, and a focused remediation direction. Do not apply fixes unless explicitly asked.
