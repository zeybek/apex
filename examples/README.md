# Examples

These client-neutral walkthroughs demonstrate what each Apex skill should do on a bounded scenario. They are development and learning assets, not part of the distributed plugin under `plugins/apex/`.

| Skill | Walkthrough | Evidence |
|---|---|---|
| `apex-design` | [Service boundary decision](apex-design/service-boundary/README.md) | Decision rubric |
| `apex-implement` | [Duplicate order charge](apex-implement/duplicate-job/README.md) | Executable verifier |
| `apex-investigate` | [CI-only flaky test](apex-investigate/flaky-ci-test/README.md) | Executable verifier |
| `apex-review` | [Tenant authorization review](apex-review/tenant-authorization/README.md) | Review rubric |

## Scenario Layout

Each scenario keeps the prompt and evaluator material outside the agent workspace:

```text
scenario/
├── README.md
├── prompt.md
├── rubric.md
├── verify.py       # present when behavior can be checked mechanically
└── workspace/
```

- `prompt.md` is the task to give the agent.
- `workspace/` is the only directory the agent should inspect or change.
- `rubric.md` is evaluator guidance. Do not load it into the agent session.
- `verify.py` checks observable behavior without revealing a required implementation.

## Running A Walkthrough

Copy the workspace before invoking an agent so the canonical fixture remains unchanged:

```bash
scenario=examples/apex-implement/duplicate-job
workdir=$(mktemp -d)
cp -R "$scenario/workspace/." "$workdir/"
```

Start a clean agent session in `$workdir`, invoke the named Apex skill, and provide the contents of `prompt.md`. For executable scenarios, run the verifier from the repository root afterward:

```bash
python3 "$scenario/verify.py" "$workdir"
```

The canonical implement and investigate workspaces intentionally fail their verifier before the exercise.
