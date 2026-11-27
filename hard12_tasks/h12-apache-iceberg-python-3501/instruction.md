You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Binary StartsWith visitors compare bytes as strings

Several `StartsWith` / `NotStartsWith` visitors appear to compare binary values by converting them with `str(...)`, which gives incorrect byte-prefix behavior.

Examples:

```text
StartsWith("x", b"a") on b"aa" -> False  # expected True
NotStartsWith("x", b"a") on b"aa" -> True # expected False
```

This also affects planning paths:

```text
inclusive metrics for a file containing only b"aa":
StartsWith("x", b"a") -> False  # unsafe skip
```

Manifest evaluation for binary `StartsWith` can also raise `TypeError` when comparing decoded `bytes` bounds to a `str` prefix.

Relevant code: `pyiceberg/expressions/visitors.py` starts-with handling in expression, manifest, metrics, and residual visitors.
