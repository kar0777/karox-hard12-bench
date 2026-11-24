You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Snowflake -> DuckDB: DATE_TRUNC on a DATE returns a TIMESTAMP

**Fully reproducible code snippet**

`DATE_TRUNC` on a `DATE` returns a `DATE` in Snowflake but a `TIMESTAMP` in DuckDB, and the Snowflake to DuckDB transpilation passes the call through unchanged. Checked on `main` (feb0e08) with DuckDB 2.0.0:

```python
import duckdb, sqlglot

sql = sqlglot.transpile("SELECT DATE_TRUNC('MONTH', CAST('2024-05-09' AS DATE))", read="snowflake", write="duckdb")[0]
print(sql)  # SELECT DATE_TRUNC('MONTH', CAST('2024-05-09' AS DATE))

con = duckdb.connect()
print(con.execute(sql).fetchall(), con.description[0][1])
# [(datetime.datetime(2024, 5, 1, 0, 0),)] TIMESTAMP
```

On Snowflake the same query returns `datetime.date(2024, 5, 1)` as a `DATE` (checked on a live account, 10.38). The same applies to `TRUNC(<date>, 'MONTH')`, and to a time part on a date: `DATE_TRUNC('HOUR', <date>)` returns the date unchanged as a `DATE`.

Expected, when the argument is known to be a `DATE`: `SELECT CAST(DATE_TRUNC('MONTH', CAST('2024-05-09' AS DATE)) AS DATE)` or equivalent.

**Official Documentation**

- Snowflake DATE_TRUNC: "The returned value is the same type as the input value." https://docs.snowflake.com/en/sql-reference/functions/date_trunc
- DuckDB `date_trunc(part, date)` returns `TIMESTAMP`: https://duckdb.org/docs/stable/sql/functions/date

