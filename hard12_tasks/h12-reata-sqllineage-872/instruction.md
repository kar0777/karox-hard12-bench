You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Snowflake stage path in FROM clause is reported as a table, and lost in COPY INTO with a transformation subquery

**Describe the bug**

With `--dialect=snowflake`, a stage referenced in a FROM clause is reported as a table in the default schema, and when followed by an option list it is dropped entirely. `COPY INTO` with a transformation subquery loses the stage (loading) or the source table (unloading).

**SQL**

```sql
SELECT $1, $2 FROM @mystage/path/
```

```sql
SELECT t.$1, t.$2 FROM @mystage/path/ (FILE_FORMAT => 'myformat') t
```

```sql
COPY INTO tab1 FROM (SELECT $1, $2 FROM @mystage/path/) FILE_FORMAT = (TYPE = CSV)
```

```sql
COPY INTO @mystage/unload/ FROM (SELECT col1, col2 FROM tab1)
```

**To Reproduce**

```
sqllineage --dialect=snowflake -e "SELECT $1, $2 FROM @mystage/path/"
sqllineage --dialect=snowflake -e "SELECT t.$1, t.$2 FROM @mystage/path/ (FILE_FORMAT => 'myformat') t"
sqllineage --dialect=snowflake -e "COPY INTO tab1 FROM (SELECT $1, $2 FROM @mystage/path/) FILE_FORMAT = (TYPE = CSV)"
sqllineage --dialect=snowflake -e "COPY INTO @mystage/unload/ FROM (SELECT col1, col2 FROM tab1)"
```

**Expected behavior**

1. Source `@mystage/path/` (a path, like `COPY INTO tab1 FROM @mystage/path/` already reports), not a table.
2. Source `@mystage/path/`.
3. Source `@mystage/path/`, target `<default>.tab1`.
4. Source `<default>.tab1`, target `@mystage/unload/`.

**Actual behavior**

1. `Source Tables: <default>.@mystage/path/`
2. No source table.
3. No source table, target `<default>.tab1`.
4. No source table, target `<default>.@mystage/unload/`.

For comparison, `COPY INTO tab1 FROM @mystage/path/` reports `@mystage/path/` as the source and `COPY INTO @mystage/unload/ FROM tab1` raises `UnsupportedStatementException` for `copy_into_location_statement`, so the subquery forms are the ones that silently give wrong results.

**Python version (available via `python --version`)**

Python 3.10.20

**SQLLineage version (available via `sqllineage --version`):**

master at 4edbde0 (1.5.9), sqlfluff 4.5.0

**Additional context**

Querying a stage directly and transforming data while loading/unloading are both documented snowflake usage: https://docs.snowflake.com/en/user-guide/querying-stage, https://docs.snowflake.com/en/user-guide/data-load-transform, https://docs.snowflake.com/en/sql-reference/sql/copy-into-location

