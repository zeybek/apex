"""Tests for the offline eval harness (stub client; no model calls)."""

import json
from types import SimpleNamespace

import pytest
import run_evals
from eval_clients import get_client
from eval_clients.claude_code import ClaudeCodeClient
from eval_clients.stub import StubClient


def test_get_client_stub():
    assert isinstance(get_client("stub"), StubClient)


def test_get_client_unknown_exits():
    with pytest.raises(SystemExit):
        get_client("nope")


def test_split_is_deterministic_and_stratified():
    cases = [{"query": f"q{i}", "should_trigger": i % 2 == 0} for i in range(20)]
    first = run_evals.split_train_validation(cases, seed=7)
    again = run_evals.split_train_validation(cases, seed=7)
    assert [c["query"] for c in first[0]] == [c["query"] for c in again[0]]
    train, validation = first
    assert len(train) + len(validation) == 20
    assert {c["should_trigger"] for c in validation} == {True, False}


def test_run_trigger_report_shape():
    report = run_evals.run_trigger("apex-review", get_client("stub"), runs=3, seed=1)
    assert report["skill"] == "apex-review"
    assert report["client"] == "stub"
    assert 0.0 <= report["summary"]["validation_pass_rate"] <= 1.0
    assert len(report["per_query"]) == report["summary"]["queries"]
    for row in report["per_query"]:
        assert set(row) == {"query", "should_trigger", "split", "trigger_rate", "passed"}


def test_cmd_trigger_report_only_exit_zero(tmp_path, capsys):
    out = tmp_path / "report.json"
    rc = run_evals.main(
        ["trigger", "--skill", "apex-design", "--client", "stub", "--runs", "1", "--out", str(out)]
    )
    assert rc == 0
    assert json.loads(out.read_text())["skill"] == "apex-design"


def test_cmd_trigger_report_flag_prints_json(capsys):
    rc = run_evals.main(
        ["trigger", "--skill", "apex-design", "--client", "stub", "--runs", "1", "--report"]
    )
    assert rc == 0
    assert '"per_query"' in capsys.readouterr().out


def test_cmd_trigger_threshold_can_gate():
    rc = run_evals.main(
        [
            "trigger",
            "--skill",
            "apex-design",
            "--client",
            "stub",
            "--runs",
            "1",
            "--threshold",
            "0.9",
        ]
    )
    assert rc == 1


@pytest.mark.parametrize(
    "args",
    [
        ["trigger", "--skill", "apex-design", "--runs", "0"],
        ["trigger", "--skill", "apex-design", "--threshold", "1.1"],
        ["output", "--skill", "apex-design", "--samples", "0"],
        [
            "aggregate",
            "--skill",
            "apex-design",
            "--model",
            "m",
            "--date",
            "2026-99-99",
            "--samples",
            "1",
            "--with-skill",
            "with",
            "--baseline",
            "base",
        ],
    ],
)
def test_cli_rejects_invalid_numeric_and_date_values(args):
    with pytest.raises(SystemExit):
        run_evals.main(args)


def test_output_dry_run(capsys):
    rc = run_evals.main(["output", "--skill", "apex-implement", "--client", "stub", "--dry-run"])
    assert rc == 0
    assert "dry-run" in capsys.readouterr().out


def test_output_run_scaffolds_grading(tmp_path):
    out = tmp_path / "wd"
    rc = run_evals.main(
        [
            "output",
            "--skill",
            "apex-review",
            "--client",
            "stub",
            "--samples",
            "2",
            "--out",
            str(out),
        ]
    )
    assert rc == 0
    case_dirs = [p for p in out.iterdir() if p.is_dir()]
    assert case_dirs
    grading = json.loads((case_dirs[0] / "grading.json").read_text())
    assert all(a["result"] is None for a in grading["assertion_results"])
    assert len(json.loads((case_dirs[0] / "timing.json").read_text())) == 2


def test_output_refuses_to_overwrite_existing_results(tmp_path, capsys):
    out = tmp_path / "wd"
    args = ["output", "--skill", "apex-review", "--client", "stub", "--out", str(out)]
    assert run_evals.main(args) == 0
    grading_path = next(path for path in out.glob("*/grading.json"))
    grading_path.write_text("human grading", encoding="utf-8")

    assert run_evals.main(args) == 2
    assert grading_path.read_text(encoding="utf-8") == "human grading"
    assert "output directory is not empty" in capsys.readouterr().err


def _write_results(dirpath, cases, mode, result, samples=1):
    for case in cases:
        case_id = case["id"]
        case_dir = dirpath / case_id
        case_dir.mkdir(parents=True)
        (case_dir / "grading.json").write_text(
            json.dumps(
                {
                    "id": case_id,
                    "mode": mode,
                    "assertion_results": [
                        {"assertion": assertion, "result": result, "evidence": ""}
                        for assertion in case["assertions"]
                    ],
                }
            )
        )
        (case_dir / "timing.json").write_text(
            json.dumps([{"duration_ms": 100, "total_tokens": 50}] * samples)
        )


def test_aggregate_from_completed_gradings(tmp_path):
    with_dir, base_dir = tmp_path / "with", tmp_path / "base"
    cases = run_evals.load_output_cases("apex-design")
    _write_results(with_dir, cases, "with-skill", True)
    _write_results(base_dir, cases, "baseline", False)
    out = tmp_path / "bench.json"
    rc = run_evals.main(
        [
            "aggregate",
            "--skill",
            "apex-design",
            "--model",
            "m",
            "--date",
            "2026-06-14",
            "--with-skill",
            str(with_dir),
            "--baseline",
            str(base_dir),
            "--out",
            str(out),
        ]
    )
    assert rc == 0
    bench = json.loads(out.read_text())
    assert bench["with_skill"]["assertion_pass_rate"] == 1.0
    assert bench["baseline"]["assertion_pass_rate"] == 0.0
    assert bench["with_skill"]["duration_ms"] == len(cases) * 100
    assert bench["baseline"]["total_tokens"] == len(cases) * 50


def test_aggregate_rejects_incomplete_grading(tmp_path, capsys):
    with_dir, base_dir = tmp_path / "with", tmp_path / "base"
    cases = run_evals.load_output_cases("apex-design")
    _write_results(with_dir, cases, "with-skill", True)
    _write_results(base_dir, cases, "baseline", False)
    grading_path = with_dir / cases[0]["id"] / "grading.json"
    grading = json.loads(grading_path.read_text())
    grading["assertion_results"][0]["result"] = None
    grading_path.write_text(json.dumps(grading))

    rc = run_evals.main(
        [
            "aggregate",
            "--skill",
            "apex-design",
            "--model",
            "m",
            "--date",
            "2026-06-14",
            "--with-skill",
            str(with_dir),
            "--baseline",
            str(base_dir),
        ]
    )

    assert rc == 2
    assert "is not graded" in capsys.readouterr().err


def test_aggregate_metrics_counts_each_assertion_and_all_timings(tmp_path):
    cases = [
        {"id": "one", "assertions": ["a"]},
        {"id": "three", "assertions": ["b", "c", "d"]},
    ]
    _write_results(tmp_path, cases, "with-skill", False, samples=2)
    grading_path = tmp_path / "one" / "grading.json"
    grading = json.loads(grading_path.read_text())
    grading["assertion_results"][0]["result"] = True
    grading_path.write_text(json.dumps(grading))

    metrics = run_evals._aggregate_metrics(tmp_path, cases, "with-skill", samples=2)

    assert metrics == {"assertion_pass_rate": 0.25, "duration_ms": 400, "total_tokens": 200}


def test_claude_code_client_rejects_failed_command(monkeypatch):
    monkeypatch.setattr(
        "eval_clients.claude_code.subprocess.run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1, stderr="failed", stdout=""),
    )

    with pytest.raises(RuntimeError, match="exited with status 1"):
        ClaudeCodeClient().run("prompt")


def test_main_requires_subcommand():
    with pytest.raises(SystemExit):
        run_evals.main([])
