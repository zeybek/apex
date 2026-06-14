# Evaluation Rubric

A strong result:

- reproduces both passing and failing runs instead of labeling the test generically flaky;
- identifies `PYTHONHASHSEED` as the changing condition;
- connects unordered set iteration to the unstable primary-region result;
- bounds the affected behavior to `select_primary`;
- separates pinning a hash seed as mitigation from explicit region priority as the durable fix;
- proposes a multi-seed or equivalent regression check as prevention;
- preserves the original evidence and does not change production or test code during diagnosis.
