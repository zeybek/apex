# Task

Our order worker is double-charging customers. Two workers can grab the same unprocessed order, call the payment API, then mark it processed, so the card gets hit twice.

Fix only this defect using the existing in-memory store and test patterns. Preserve retry after a payment failure, add a regression test for competing workers, run the available checks, and report verification plus residual risk. Do not redesign unrelated modules.
