# CI-Only Flaky Test

Use `apex-investigate` to bound and explain a test that passes locally but fails intermittently in CI.

## Learning Goal

Treat intermittence as evidence, identify the triggering condition and mechanism, preserve the failing state, and separate mitigation from a durable fix without changing code during diagnosis.

## Run

1. Copy [`workspace/`](workspace/) to a temporary directory.
2. Run `python3 run_ci_matrix.py` in that directory to observe the failure distribution.
3. Start a clean agent session in the temporary workspace with `apex-investigate`.
4. Provide [`prompt.md`](prompt.md) as the task.
5. Run the verifier and evaluate the account with [`rubric.md`](rubric.md):

   ```bash
   python3 examples/apex-investigate/flaky-ci-test/verify.py <temporary-workspace>
   ```

The verifier requires a structured investigation record and confirms the original intermittent mechanism remains reproducible.
