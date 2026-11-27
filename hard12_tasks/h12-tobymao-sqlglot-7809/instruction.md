You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Sqlite: Multiple IN operators caused an sqlglot.errors.ParseError.

read="sqlite"
dialect="sqlite"
Confirmed on main: reproduces on commit fd6d4d61c25e7918118fc22c5579098a86a58e10

**Fully reproducible code snippet**
```python
import sqlglot
sql = "SELECT 1 NOT IN (0) IN (1)"

ast = sqlglot.parse_one(sql, read = "sqlite")
```
it output:
```
sqlglot.errors.ParseError: Invalid expression / Unexpected token. Line 1, Col: 22.
  SELECT 1 NOT IN (0) IN (1)
```
This query can be successfully executed on sqlite3
