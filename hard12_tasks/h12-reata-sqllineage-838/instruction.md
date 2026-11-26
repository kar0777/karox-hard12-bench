You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

SELECT * from CTE fails to resolve column lineage

**Describe the bug**
Column lineage fails to resolve when referencing a SELECT * from a CTE.

Not sure if this is the same issue as https://github.com/reata/sqllineage/issues/303 as it looks similar just 1 layer deeper with a secondary select * CTE.

Below is a simplified example, our production scenarios are more complicated but it boils down to this.

**SQL**
```sql
CREATE TABLE MAIN.FOOBAR AS (
    WITH FOO AS (
        SELECT COL1, COL2 FROM FROM MAIN.BAR
    )
    SELECT * FROM FOO
)
```

Column Lineage fails to resolve columns defined in FOO

**To Reproduce**
```python
from sqllineage.runner import LineageRunner
sql1 = """
CREATE TABLE MAIN.FOOBAR AS (
    WITH FOO AS (
        SELECT COL1, COL2 FROM FROM MAIN.BAR
    )
    SELECT * FROM FOO
)
"""
LineageRunner(sql1).print_column_lineage()
```
actual output is
```
main.foobar.* <- foo.*
```
I'd expect it to return this instead
```
main.foobar.col1 <- main.bar.col1
main.foobar.col2 <- main.bar.col2
```

**Python version (available via `python --version`)**
 - 3.11.5

**SQLLineage version (available via `sqllineage --version`):**
 - 1.5.3

We noticed the issue using the snowflake dialect for our own production use cases

