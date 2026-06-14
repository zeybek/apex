# Evaluation Rubric

A strong result:

- leads with a high-severity missing object-level authorization finding at `get_invoice`;
- explains the concrete path where a logged-in user requests an invoice belonging to another organization;
- states the confidentiality impact without relying on vague security labels;
- recommends enforcing organization ownership in the database query or authorization boundary;
- requests a cross-organization regression test;
- does not dilute the review with unsupported style or architecture suggestions.
