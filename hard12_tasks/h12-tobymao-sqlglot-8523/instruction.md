You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

SQLGlot translates Spark concat_ws on an array into array stringification


#### Before you file an issue

- [x] Read dialect specified: `sqlglot.parse_one(query, read="spark")`.
- [x] Write dialect specified: `ast.sql(dialect="duckdb")`.
- [x] Issue still exists on `main`, checked on October 5, 2026 at
      commit [`50d7ce4`](https://github.com/tobymao/sqlglot/commit/50d7ce4a9808aed6beb4127c4f60d309219c664d).

#### Fully reproducible code snippet

```python
import duckdb
import sqlglot

print("SQLGlot:", sqlglot.__version__)
print("DuckDB:", duckdb.__version__)
query = "SELECT concat_ws(',', array('b', 'c', 'd', 'e')) AS joined"
ast = sqlglot.parse_one(query, read="spark")
translated = ast.sql(dialect="duckdb")
print(translated)
print(duckdb.sql(translated).fetchall())
```

**Actual generated SQL:**

```sql
SELECT CONCAT_WS(',', ['b', 'c', 'd', 'e']) AS joined
```

**Actual result:** `[('[b, c, d, e]',)]`.

**Expected result (matching Apache Spark):** `[('b,c,d,e',)]`.

**One valid expected translation for this input:**

```sql
SELECT ARRAY_TO_STRING(['b', 'c', 'd', 'e'], ',') AS joined
```

Spark joins the array's elements; DuckDB's `concat_ws` stringifies the array
argument. The translation preserves the function call without adapting this
behavior, returning bracketed array text instead of joined elements.

#### Official Documentation

- [Apache Spark string functions](https://spark.apache.org/docs/latest/sql-ref-functions-builtin.html#string-functions):
  `concat_ws` accepts strings or arrays of strings and joins them with a separator.
- [DuckDB text functions](https://duckdb.org/docs/current/sql/functions/text):
  `concat_ws` accepts string arguments; `array_to_string` joins array elements
  using a delimiter.

