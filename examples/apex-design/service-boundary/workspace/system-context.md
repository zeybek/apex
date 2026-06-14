# System Context

The company runs a modular monolith deployed to three application instances behind a load balancer. PostgreSQL is the system of record. Orders, invoices, payment attempts, and customer accounts currently share one database and deployment pipeline.

Billing responsibilities are concentrated in one application module but share transaction helpers and customer tables with orders. The module calls a managed payment provider synchronously and writes an append-only payment-attempt table.

Current behavior:

- checkout availability target: 99.9%;
- billing reconciliation target: complete by 08:00 each business day;
- peak traffic: 40 order submissions per second;
- deployments: twice per week, rolling across the three instances;
- incidents: two billing defects in the last quarter required manual SQL correction;
- audit requests require reconstructing who changed an invoice and why.

Team and constraints:

- twelve application engineers and two platform engineers;
- no dedicated billing team yet;
- limited experience operating asynchronous workflows and distributed transactions;
- six-month deadline for improved audit evidence;
- no planned database split this quarter;
- payment-provider contract and public checkout API must remain unchanged.
