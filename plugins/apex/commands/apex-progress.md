---
description: Report the status of planning workspaces under .apex-design/ — tasks done, in progress, blocked, and what is next.
argument-hint: "optional initiative slug"
---

Report progress for the planning workspace(s) under `.apex-design/`.

$ARGUMENTS

Steps:

1. If an initiative slug is given, use it; otherwise summarize every initiative under `.apex-design/`, most recently active first.
2. For each initiative, read its `progress.md` and `plan.md` and report: the current position, counts of pending / in progress / done / blocked tasks, the next actionable task, and any open blockers or decisions.
3. Keep this a faithful status report — do not implement anything or change files. If a board looks stale relative to the code, say so rather than guessing.
