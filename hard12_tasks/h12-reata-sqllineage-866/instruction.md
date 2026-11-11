You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Snowflake/Oracle multi-table INSERT (INSERT ALL / INSERT FIRST) raises SQLLineageException

**Describe the bug**
* A multi-table insert with more than one `INTO` clause fails with a bare `SQLLineageException` (no message), for both table and column lineage. sqlfluff parses the statement fine with `--dialect=snowflake` and `--dialect=oracle`. Conditional `INSERT ALL WHEN ... THEN INTO ...` and `INSERT FIRST ... ELSE INTO ...` (Snowflake) fail the same way.

  Syntax reference: https://docs.snowflake.com/en/sql-reference/sql/insert-multi-table and https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/INSERT.html

**SQL**
```sql
INSERT ALL
    INTO tab1 (col1) VALUES (col1)
    INTO tab2 (col2) VALUES (col2)
SELECT col1, col2 FROM tab3;
```

**To Reproduce**
```shell
sqllineage -f test.sql --dialect=snowflake
```
```
Traceback (most recent call last):
  ...
  File ".../sqllineage/core/parser/sqlfluff/extractors/create_insert.py", line 56, in extract
    holder |= self.delegate_to_select(segment, holder)
  ...
  File ".../sqllineage/core/parser/sqlfluff/extractors/select.py", line 62, in extract
    self.end_of_query_cleanup(holder)
  File ".../sqllineage/core/parser/__init__.py", line 24, in end_of_query_cleanup
    raise SQLLineageException
sqllineage.exceptions.SQLLineageException
```
`--dialect=oracle` gives the same traceback.

With a single `INTO` clause there is no exception, but the `VALUES` list is ignored and the query columns are mapped to the table by position.

**Expected behavior**
```
Statements(#): 1
Source Tables:
    <default>.tab3
Target Tables:
    <default>.tab1
    <default>.tab2
```
and for column lineage (`-l column`):
```
<default>.tab1.col1 <- <default>.tab3.col1
<default>.tab2.col2 <- <default>.tab3.col2
```

**Python version (available via `python --version`)**
 - 3.10.20

**SQLLineage version (available via `sqllineage --version`):**
 - master (7b0d89a, 1.5.9), sqlfluff 4.4.0

