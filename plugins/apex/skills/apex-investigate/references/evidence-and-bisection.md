# Evidence and Bisection

Narrow an unknown failure to its cause by systematically ruling out what it is not.

## Reproduce

- Build the smallest input, state, and environment that reliably triggers the failure.
- If the failure is intermittent, find what raises its probability — load, ordering, specific data, timing — and reproduce under that condition.
- Treat a non-reproduction as missing information, not a fix; list the conditions you have not controlled for.

## Bound the Failure

Determine which dimension the failure depends on by comparing working and failing cases along one axis at a time:

- code version (between a known-good and a known-bad revision);
- component or service boundary;
- deployment, host, region, or environment;
- data: a specific record, partition, shape, or volume;
- configuration and feature flags;
- timing, concurrency, ordering, and load;
- identity, permissions, and tenant.

## Bisect Efficiently

- Halve the search space with each test; choose the split that rules out the most.
- Change one variable per test and hold the others fixed.
- Use history bisection (a binary search over commits or deploys) when the failure correlates with a change in time.
- Record what each step rules in or out, so the path is auditable and you do not retest the same thing.

## Differential Analysis

- Compare a passing and a failing trace side by side; the first point where they diverge bounds the cause.
- Compare against the last known-good state: what changed in code, data, configuration, dependencies, or environment.

## Foundational Sources

- David J. Agans, "Debugging: The Nine Indispensable Rules": https://debuggingrules.com/
- Git bisect documentation: https://git-scm.com/docs/git-bisect
- Brian Kernighan and Rob Pike, "The Practice of Programming": https://www.cs.princeton.edu/~bwk/tpop.webpage/
