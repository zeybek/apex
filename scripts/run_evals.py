#!/usr/bin/env python3
"""Dependency-light eval harness for apex skills.

Dev tooling — NOT a runtime validator, never imported by the validators, and
never required to install or run the package. Subcommands:

  trigger    measure skill activation accuracy from evals/trigger-evals.json
  output     run output-eval cases (with-skill or baseline) and scaffold grading
  aggregate  roll completed gradings into a benchmark.json

The `stub` client runs fully offline and deterministically (CI + tests). The
`claude-code` client shells the real CLI for actual measurements.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

from eval_clients import available_clients, get_client

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "plugins" / "apex" / "skills"
TRIGGER_THRESHOLD = 0.5  # a positive query must fire on at least half its runs


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed


def probability(value: str) -> float:
    parsed = float(value)
    if not 0 <= parsed <= 1:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return parsed


def iso_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a valid YYYY-MM-DD date") from exc
    if parsed.isoformat() != value:
        raise argparse.ArgumentTypeError("must use YYYY-MM-DD format")
    return value


def available_skills() -> list[str]:
    return sorted(path.name for path in SKILLS_ROOT.iterdir() if path.is_dir())


def _read_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _emit(obj, out) -> str:
    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    if out:
        path = Path(out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return text


def load_trigger_cases(skill: str) -> list[dict]:
    return _read_json(SKILLS_ROOT / skill / "evals" / "trigger-evals.json")


def load_output_cases(skill: str) -> list[dict]:
    return _read_json(SKILLS_ROOT / skill / "evals" / "evals.json")["evals"]


def split_train_validation(cases, seed, validation_fraction=0.4):
    """Deterministic, stratified train/validation split, stable across runs/clients."""

    def order_key(case):
        return hashlib.sha256(f"{seed}:{case['query']}".encode()).hexdigest()

    train, validation = [], []
    for label in (True, False):
        group = sorted((c for c in cases if bool(c.get("should_trigger")) is label), key=order_key)
        n_val = round(len(group) * validation_fraction)
        validation.extend(group[:n_val])
        train.extend(group[n_val:])
    return train, validation


def run_trigger(skill, client, runs=3, seed=13):
    cases = load_trigger_cases(skill)
    _, validation = split_train_validation(cases, seed)
    validation_queries = {c["query"] for c in validation}
    per_query = []
    for case in cases:
        query = case["query"]
        should = bool(case.get("should_trigger"))
        fired = sum(client.run(query, skill=skill, with_skill=True).activated for _ in range(runs))
        rate = fired / runs
        per_query.append(
            {
                "query": query,
                "should_trigger": should,
                "split": "validation" if query in validation_queries else "train",
                "trigger_rate": round(rate, 4),
                "passed": (rate >= TRIGGER_THRESHOLD) == should,
            }
        )

    def pass_rate(split):
        items = [p for p in per_query if p["split"] == split]
        return round(sum(p["passed"] for p in items) / len(items), 4) if items else 0.0

    return {
        "skill": skill,
        "client": client.name,
        "runs": runs,
        "seed": seed,
        "split": {
            "train": [p["query"] for p in per_query if p["split"] == "train"],
            "validation": sorted(validation_queries),
        },
        "per_query": per_query,
        "summary": {
            "train_pass_rate": pass_rate("train"),
            "validation_pass_rate": pass_rate("validation"),
            "queries": len(cases),
            "runs_total": len(cases) * runs,
        },
    }


def cmd_trigger(args):
    client = get_client(args.client)
    report = run_trigger(args.skill, client, runs=args.runs, seed=args.seed)
    if args.threshold is not None:
        report["threshold"] = args.threshold
    if args.out or args.report:
        text = _emit(report, args.out)
        if args.report:
            sys.stdout.write(text)
    summary = report["summary"]
    print(
        f"[{args.skill}] trigger via {client.name}: validation pass "
        f"{summary['validation_pass_rate']}, train {summary['train_pass_rate']} "
        f"({summary['queries']} queries x {args.runs} runs)"
    )
    if args.threshold is not None and summary["validation_pass_rate"] < args.threshold:
        print(f"  below threshold {args.threshold}", file=sys.stderr)
        return 1
    return 0


def cmd_output(args):
    cases = load_output_cases(args.skill)
    if args.dry_run:
        print(
            f"[{args.skill}] output dry-run: {len(cases)} case(s) x {args.samples} sample(s), "
            f"mode '{args.mode}', client '{args.client}'"
        )
        for case in cases:
            print(f"  - {case['id']}: {len(case['assertions'])} assertion(s)")
        return 0

    client = get_client(args.client)
    if args.out:
        out_dir = Path(args.out)
    else:
        out_dir = ROOT / "evals" / "results" / f"{args.skill}-{args.mode}"
    if out_dir.is_dir() and any(out_dir.iterdir()):
        raise ValueError(
            f"output directory is not empty: {out_dir}; choose a new path to preserve prior results"
        )
    for case in cases:
        case_dir = out_dir / str(case["id"])
        case_dir.mkdir(parents=True, exist_ok=True)
        timings, texts = [], []
        for _ in range(args.samples):
            res = client.run(case["prompt"], skill=args.skill, with_skill=args.mode == "with-skill")
            timings.append({"total_tokens": res.total_tokens, "duration_ms": res.duration_ms})
            texts.append(res.raw)
        _emit(timings, case_dir / "timing.json")
        (case_dir / "output.txt").write_text("\n---\n".join(texts) + "\n", encoding="utf-8")
        _emit(
            {
                "id": case["id"],
                "mode": args.mode,
                "assertion_results": [
                    {"assertion": a, "result": None, "evidence": ""} for a in case["assertions"]
                ],
            },
            case_dir / "grading.json",
        )
    print(
        f"[{args.skill}] output: ran {len(cases)} case(s) x {args.samples} sample(s) "
        f"({args.mode}) -> {out_dir} — grading scaffolds await a human/LLM judge"
    )
    return 0


def _aggregate_metrics(results_dir, cases, expected_mode, samples):
    root = Path(results_dir)
    if not root.is_dir():
        raise ValueError(f"results directory does not exist: {root}")

    passed = 0
    assertion_count = 0
    timings = []
    for case in cases:
        case_id = str(case["id"])
        case_dir = root / case_id
        if not case_dir.is_dir():
            raise ValueError(f"{root}: missing result directory for case {case_id!r}")

        grading_path = case_dir / "grading.json"
        if not grading_path.is_file():
            raise ValueError(f"{grading_path}: missing grading file")
        grading = _read_json(grading_path)
        if not isinstance(grading, dict):
            raise ValueError(f"{grading_path}: root must be an object")
        if grading.get("id") != case_id:
            raise ValueError(f"{grading_path}: id must be {case_id!r}")
        if grading.get("mode") != expected_mode:
            raise ValueError(f"{grading_path}: mode must be {expected_mode!r}")

        results = grading.get("assertion_results")
        expected_assertions = case["assertions"]
        if not isinstance(results, list) or len(results) != len(expected_assertions):
            raise ValueError(
                f"{grading_path}: expected {len(expected_assertions)} assertion result(s)"
            )
        for index, (result, assertion) in enumerate(zip(results, expected_assertions, strict=True)):
            if not isinstance(result, dict) or result.get("assertion") != assertion:
                raise ValueError(
                    f"{grading_path}: assertion result {index} does not match eval case"
                )
            if not isinstance(result.get("result"), bool):
                raise ValueError(f"{grading_path}: assertion result {index} is not graded")
            assertion_count += 1
            passed += result["result"]

        timing_path = case_dir / "timing.json"
        if not timing_path.is_file():
            raise ValueError(f"{timing_path}: missing timing file")
        case_timings = _read_json(timing_path)
        if not isinstance(case_timings, list) or len(case_timings) != samples:
            raise ValueError(f"{timing_path}: expected {samples} timing sample(s)")
        if not all(isinstance(item, dict) for item in case_timings):
            raise ValueError(f"{timing_path}: every timing sample must be an object")
        timings.extend(case_timings)

    metrics = {"assertion_pass_rate": round(passed / assertion_count, 4)}
    for field in ("duration_ms", "total_tokens"):
        values = [timing.get(field) for timing in timings]
        if field == "duration_ms":
            complete = all(
                isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0
                for value in values
            )
        else:
            complete = all(
                isinstance(value, int) and not isinstance(value, bool) and value >= 0
                for value in values
            )
        if values and complete:
            metrics[field] = sum(values)
    return metrics


def cmd_aggregate(args):
    cases = load_output_cases(args.skill)
    benchmark = {
        "skill": args.skill,
        "client": args.client,
        "model": args.model,
        "date": args.date,
        "samples": args.samples,
        "with_skill": _aggregate_metrics(args.with_skill, cases, "with-skill", args.samples),
        "baseline": _aggregate_metrics(args.baseline, cases, "baseline", args.samples),
    }
    if args.notes:
        benchmark["notes"] = args.notes
    text = _emit(benchmark, args.out)
    if args.report and not args.out:
        sys.stdout.write(text)
    print(
        f"[{args.skill}] benchmark: with_skill "
        f"{benchmark['with_skill']['assertion_pass_rate']} vs baseline "
        f"{benchmark['baseline']['assertion_pass_rate']}"
    )
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="apex skill eval harness (dev tooling).")
    sub = parser.add_subparsers(dest="command", required=True)
    skills = available_skills()

    trigger = sub.add_parser("trigger", help="measure skill activation accuracy")
    trigger.add_argument("--skill", required=True, choices=skills)
    trigger.add_argument("--client", default="stub", choices=available_clients())
    trigger.add_argument("--runs", type=positive_int, default=3)
    trigger.add_argument("--seed", type=int, default=13)
    trigger.add_argument("--threshold", type=probability, default=None)
    trigger.add_argument("--out")
    trigger.add_argument("--report", action="store_true", help="print the full JSON report")
    trigger.set_defaults(func=cmd_trigger)

    output = sub.add_parser("output", help="run output-eval cases / scaffold grading")
    output.add_argument("--skill", required=True, choices=skills)
    output.add_argument("--client", default="stub", choices=available_clients())
    output.add_argument("--mode", default="with-skill", choices=["with-skill", "baseline"])
    output.add_argument("--samples", type=positive_int, default=1)
    output.add_argument("--dry-run", action="store_true")
    output.add_argument("--out")
    output.set_defaults(func=cmd_output)

    aggregate = sub.add_parser("aggregate", help="roll gradings into a benchmark.json")
    aggregate.add_argument("--skill", required=True, choices=skills)
    aggregate.add_argument("--client", default="claude-code")
    aggregate.add_argument("--model", required=True)
    aggregate.add_argument("--date", required=True, type=iso_date)
    aggregate.add_argument("--samples", type=positive_int, default=1)
    aggregate.add_argument("--with-skill", required=True, dest="with_skill")
    aggregate.add_argument("--baseline", required=True)
    aggregate.add_argument("--notes")
    aggregate.add_argument("--out")
    aggregate.add_argument("--report", action="store_true")
    aggregate.set_defaults(func=cmd_aggregate)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
