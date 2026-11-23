You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Postgres: Incorrect generation of CURRENT_TIME and CURRENT_TIMESTAMP with optional precision

**Before you file an issue**

- Read dialect: `postgres`
- Write dialect: `postgres`
- Reproduced with SQLGlot 30.32.0 and on `main` at `b812ff95afa2ab7ab925f95edd5d97c4b761cec9`.

**Fully reproducible code snippet**

```python
from sqlglot import parse_one

for sql in ("SELECT CURRENT_TIME", "SELECT CURRENT_TIMESTAMP(3)"):
    print(parse_one(sql, read="postgres").sql(dialect="postgres"))
```

Actual output:

```sql
SELECT CURRENT_TIME()
SELECT CURRENT_TIMESTAMP
```

Expected output:

```sql
SELECT CURRENT_TIME
SELECT CURRENT_TIMESTAMP(3)
```

PostgreSQL rejects empty parentheses after `CURRENT_TIME`. Dropping `(3)` from `CURRENT_TIMESTAMP(3)` also changes the result, since PostgreSQL rounds the fractional seconds to the requested precision when one is specified.

**Official Documentation**

[PostgreSQL: Current Date/Time](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT)

Generated with Codex.

