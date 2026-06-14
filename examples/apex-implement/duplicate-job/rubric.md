# Evaluation Rubric

A strong result:

- states the invariant that one order produces at most one successful charge;
- prevents two worker instances sharing the store from charging the same order;
- leaves an order retryable when the payment call fails;
- adds a deterministic competing-worker regression test;
- keeps the public example API and unrelated behavior stable;
- reports commands run, evidence inspected, and any residual risk around external payment idempotency.
