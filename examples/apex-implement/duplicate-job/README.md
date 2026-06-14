# Duplicate Order Charge

Use `apex-implement` to fix a concurrency defect without redesigning unrelated code.

## Learning Goal

Establish the single-charge invariant across competing workers, preserve retry after payment failure, add focused regression evidence, and report residual risk.

## Run

1. Copy [`workspace/`](workspace/) to a temporary directory.
2. Confirm the starting defect:

   ```bash
   python3 examples/apex-implement/duplicate-job/verify.py <temporary-workspace>
   ```

3. Start a clean agent session in the temporary workspace with `apex-implement`.
4. Provide [`prompt.md`](prompt.md) as the task.
5. Run the verifier again and evaluate the close-out with [`rubric.md`](rubric.md).

The verifier checks behavior, not a specific locking or idempotency implementation.
