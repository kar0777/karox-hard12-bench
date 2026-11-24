You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Column lineage for UNION [ALL] BY NAME matches columns by position instead of by name

**Describe the bug**
* `UNION [ALL] BY NAME` (Snowflake, DuckDB, BigQuery) and `UNION ALL CORRESPONDING` (BigQuery) combine queries by column name, not by position. sqllineage treats them like a plain `UNION ALL` and maps the columns of the second query by position, so the column lineage is wrong whenever the queries list their columns in a different order.

**SQL**
```sql
INSERT INTO tgt
SELECT a, b FROM t1
UNION ALL BY NAME
SELECT b, a FROM t2;
```

**To Reproduce**
```shell
sqllineage -f test.sql --dialect=snowflake -l column
```
```
<default>.tgt.a <- <default>.t1.a
<default>.tgt.a <- <default>.t2.b
<default>.tgt.b <- <default>.t1.b
<default>.tgt.b <- <default>.t2.a
```

The output is the same with `--dialect=duckdb` and `--dialect=bigquery`, with `UNION BY NAME` (Snowflake, DuckDB), and with `UNION ALL CORRESPONDING` (BigQuery).

**Expected behavior**
```
<default>.tgt.a <- <default>.t1.a
<default>.tgt.a <- <default>.t2.a
<default>.tgt.b <- <default>.t1.b
<default>.tgt.b <- <default>.t2.b
```

From the Snowflake docs (https://docs.snowflake.com/en/sql-reference/operators-query), columns with the same name are matched, the queries may have a different number of columns, and the result columns are the unique column names from left to right (a column that only appears in a later query is added at the end, and is NULL for the rows of the other queries). DuckDB (https://duckdb.org/docs/stable/sql/query_syntax/setops#union-all-by-name) behaves the same way.

**Python version (available via `python --version`)**
 - 3.10.20

**SQLLineage version (available via `sqllineage --version`):**
 - 1.5.9 (also reproduced on master at 81909d9, sqlfluff 4.4.0)

**Additional context**
With `SELECT *` in the queries and a metadata provider, the expanded columns are also matched by position.

