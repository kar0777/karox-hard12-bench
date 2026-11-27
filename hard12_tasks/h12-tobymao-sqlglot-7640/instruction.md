You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Sqlite ParseError: Invalid expression / Unexpected token. for WINDOW

## Fully reproducible code snippet
When I'm trying to parse the query below, a error occurs:
```python
import sqlglot
sql = """SELECT 1 WINDOW a AS (PARTITION BY fake_column);"""
ast = sqlglot.parse_one(sql, read = "sqlite")
print(ast.sql())
```
error messages:
```
sqlglot.errors.ParseError: Invalid expression / Unexpected token. Line 1, Col: 17.
  SELECT 1 WINDOW a AS (PARTITION BY fake_column);
```
