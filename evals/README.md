# Evaluation Guide

Use evaluation to determine whether a skill improves results enough to justify its context, time, and complexity cost. Format validation alone does not prove skill quality.

This guide describes the evaluation protocol and the included dependency-light runner. The runner executes prompts and scaffolds grading, but output assertions still require a human or LLM judge. `make validate` checks only eval-file structure and counts, not output quality.

## Evaluation Files

Each skill contains:

- `evals/trigger-evals.json`: prompts labeled with whether the skill should activate;
- `evals/evals.json`: realistic output-quality tasks, expected outcomes, and assertions.

The eval format is package-local rather than part of the Agent Skills specification.

## Trigger Evaluation

1. Install the skill in the target client.
2. Run every query in a clean session and observe whether the client loads the skill.
3. Repeat each query at least three times because activation is nondeterministic.
4. Record trigger rate for each query.
5. Investigate missed positive prompts and false-positive near misses.
6. Revise descriptions using a train subset, then choose the best version using a held-out validation subset.

Do not optimize descriptions against every query. Preserve unseen prompts for a final generalization check.

## Output Evaluation

For every case in `evals/evals.json`:

1. Run the prompt in a clean session with the skill.
2. Run the same prompt without the skill or with the previous skill version.
3. Grade every assertion using concrete evidence from the output and execution trace.
4. Compare pass rate, human preference, elapsed time, and token use.
5. Remove instructions that add cost without improving results.
6. Generalize fixes from recurring failures; do not patch only the eval prompt.

Use deterministic scripts for mechanical assertions when practical. Use a blinded human or model judge for qualities that cannot be checked mechanically.

## Result Record

Committed benchmark records conform to `schemas/benchmark.schema.json` and include:

```json
{
  "skill": "apex-implement",
  "client": "client and version",
  "model": "model and version",
  "date": "2026-06-14",
  "samples": 5,
  "with_skill": {
    "assertion_pass_rate": 0.0,
    "duration_ms": 0,
    "total_tokens": 0
  },
  "baseline": {
    "assertion_pass_rate": 0.0,
    "duration_ms": 0,
    "total_tokens": 0
  }
}
```

`assertion_pass_rate` covers all assertions across every case. `duration_ms` and `total_tokens` are totals across every case and sample. Evaluation results are environment- and model-dependent; do not present one client's result as proof of universal behavior.

## Running the harness

`scripts/run_evals.py` is a dependency-light runner (standard library only; dev tooling, never imported by the validators). It has an offline `stub` client — deterministic, no model, used by CI to prove the harness works — and a `claude-code` client for real measurements.

Trigger accuracy (activation):

```bash
# offline smoke (no model) — exercises the runner, not real accuracy
python3 scripts/run_evals.py trigger --skill apex-design --client stub

# real measurement against a configured client
python3 scripts/run_evals.py trigger --skill apex-design --client claude-code --runs 3 \
  --out evals/results/apex-design-trigger.json
```

The runner splits the queries 60/40 train/validation (deterministic, stratified by label), runs each query `--runs` times, and reports per-query trigger rates plus train and validation pass rates — a positive query passes when it fires on at least half its runs. It is report-only unless you pass `--threshold`. The report conforms to [`schemas/trigger-report.schema.json`](../schemas/trigger-report.schema.json).

Output quality (with-skill vs baseline):

```bash
python3 scripts/run_evals.py output --skill apex-design --client claude-code --mode with-skill \
  --out evals/results/apex-design-with
python3 scripts/run_evals.py output --skill apex-design --client claude-code --mode baseline \
  --out evals/results/apex-design-base
```

Run each mode in the matching environment (skill installed for `with-skill`; uninstalled or the previous version for `baseline`). The runner records a `timing.json` per case and writes a `grading.json` **scaffold** with every assertion `result: null`. A human or LLM judge fills every grading — apex's assertions are judgment calls and are never auto-scored. Aggregation rejects missing cases, incomplete gradings, mode mismatches, and timing-sample mismatches. It calculates the pass rate across all assertions and includes total elapsed milliseconds and tokens when every sample reports them. Then aggregate into a committed benchmark:

```bash
python3 scripts/run_evals.py aggregate --skill apex-design --model "<model>" --date <YYYY-MM-DD> \
  --with-skill evals/results/apex-design-with --baseline evals/results/apex-design-base \
  --out benchmarks/apex-design/<model>-<date>.json \
  --notes "single client/model; not a universal claim"
```

`evals/results/` and `benchmarks/workspaces/` are gitignored scratch; only the curated `benchmarks/<skill>/<model>-<date>.json` files are committed.

The output command refuses to write into a non-empty result directory so reruns cannot silently overwrite completed grading. Use a new `--out` path for each run.
