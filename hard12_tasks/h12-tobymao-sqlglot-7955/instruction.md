You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Python executor INTERSECT ALL and EXCEPT ALL discard multiplicity

**Before you file an issue**

- The defect is reproduced on current `main` commit `33de21fc21cdc05755a2de39318b292c10ccec0f`.
- The relevant path is SQLGlot's dialect-independent Python executor, so separate read and write dialect settings do not apply.
- Refreshed open and closed issue, pull-request, source-history, and release searches found no exact duplicate.

**Fully reproducible code snippet**

```python
from sqlglot.executor import execute

left = [{"v": 1}, {"v": 1}, {"v": 1}]
right = [{"v": 1}, {"v": 1}]
tables = {"x": left, "y": right}
print(execute("SELECT v FROM x INTERSECT ALL SELECT v FROM y", tables=tables).rows)
print(execute("SELECT v FROM x EXCEPT ALL SELECT v FROM y", tables=tables).rows)
```

`INTERSECT ALL` returns one row instead of two, and `EXCEPT ALL` returns no rows instead of one. The corresponding DISTINCT forms are controls and correctly return set-like output.

**Expected behavior**

`ALL` operations must preserve multiset cardinality.

**Root cause**

`PythonExecutor.set_operation` converts both inputs to Python sets for `INTERSECT` and `EXCEPT`, regardless of the planner's `distinct` flag.

**Proposed correction**

Use counted row consumption for `ALL` and stable first-occurrence set behavior for `DISTINCT`.

**Validation**

The isolated local correction has a positive regression, DISTINCT controls, and a passing 21-test executor suite. The validated correction is available in linked pull request #7955.

**Official documentation**

- SQLGlot optimizer and executor API: https://sqlglot.com/sqlglot.html
- Repository contribution guide: https://github.com/tobymao/sqlglot/blob/main/CONTRIBUTING.md

