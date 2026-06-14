# Route Contract

`get_invoice` serves authenticated customers from multiple organizations.

- A user may read invoices owned by their own organization.
- A user must not learn whether another organization's invoice exists.
- `invoice_id` values are sequential integers and are visible in customer-facing URLs.
- Authentication is handled by `require_login`.
