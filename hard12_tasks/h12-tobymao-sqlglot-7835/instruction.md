You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

tsql: EXECUTE @return_status = proc @args fails to parse (regression since v29.0.0)

**Before you file an issue**
- [x] `read` dialect specified: `parse_one(sql, read="tsql")`
- [x] N/A — this is a parse-only issue, no `write`/`ast.sql(...)` involved
- [x] Confirmed still broken on latest release (30.12.0) and traced the regression back to v29.0.0 (see below)

**Fully reproducible code snippet**

```python
import sqlglot

sqlglot.parse("EXEC @RC = dbo.MyProc @a, @b;", read="tsql")

Raises:

sqlglot.errors.ParseError: Required keyword: 'this' missing for <class 'sqlglot.expressions.core.EQ'>. Line 1, Col: 23.
EXEC @RC = dbo.MyProc @a, @b;

The plain form without the return-status assignment parses fine:

sqlglot.parse("EXEC dbo.MyProc @a, @b;", read="tsql")  # OK

Also fails with no arguments at all, and with the unabbreviated keyword:

sqlglot.parse("EXEC @RC = dbo.MyProc;", read="tsql")            # ParseError
sqlglot.parse("EXECUTE @RC = dbo.MyProc @a, @b;", read="tsql")  # ParseError

**Official Documentation**

[EXECUTE (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/execute-transact-sql?view=sql-server-ver17) — EXEC/EXECUTE supports an optional @return_status =  prefix that captures the stored procedure's return code:

[ [ EXEC [ UTE ] ]
    {
      [ @return_status = ]
      { module_name [ ;number ] | @module_name_var }
      ...

This is standard, widely used syntax, and sqlglot's tsql dialect fails to parse it.
