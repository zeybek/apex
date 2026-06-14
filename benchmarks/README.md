# Benchmarks

Each file here records one real evaluation run for a single skill, comparing the skill against a baseline on a pinned model. Benchmarks turn the manual protocol in [../evals/README.md](../evals/README.md) into a committed, auditable result that demonstrates whether a skill earns its context cost.

## File format

Name each file `<skill>/<model>-<date>.json` — one subdirectory per skill — and make it conform to [../schemas/benchmark.schema.json](../schemas/benchmark.schema.json). Every number must come from an actual recorded run, never an estimate. Record the client and model versions so the result is reproducible.

A file looks like this:

```json
{
  "skill": "apex-implement",
  "client": "client name and version",
  "model": "model name and version",
  "date": "2026-06-14",
  "samples": 5,
  "with_skill": { "assertion_pass_rate": 0.0, "duration_ms": 0, "total_tokens": 0 },
  "baseline": { "assertion_pass_rate": 0.0, "duration_ms": 0, "total_tokens": 0 }
}
```

`assertion_pass_rate` covers all assertions across every case. `duration_ms` and `total_tokens` are totals across every case and sample.

## Adding a benchmark

1. Run `scripts/run_evals.py output` for the skill once in `--mode with-skill` and once in `--mode baseline` (see [../evals/README.md](../evals/README.md)).
2. Fill every `grading.json` scaffold (a human or LLM judge), then run `scripts/run_evals.py aggregate … --out benchmarks/<skill>/<model>-<date>.json`. Aggregation fails if any expected case, assertion grade, mode, or timing sample is missing or inconsistent.
3. Confirm it validates: `uvx check-jsonschema --schemafile schemas/benchmark.schema.json benchmarks/<skill>/<file>.json`.

No benchmark is committed yet: a credible result requires running the protocol on a chosen pinned model, which is environment- and model-dependent. This directory and its schema are the place to record that run when it is performed.
