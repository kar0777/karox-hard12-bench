You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

credential and encryption clauses are not fully redacted in logged SQL

### Describe the bug

`redact_credentials` in `dbt/adapters/databricks/utils.py` is applied to every logged statement
(`connections.py:244` and `connections.py:342`), but the `COPY INTO` pattern it uses misses several
shapes, so secrets can reach `logs/dbt.log` verbatim:

- The lookbehind is the lowercase literal `credential` and the pattern has no `re.IGNORECASE`, so an
  uppercase `CREDENTIAL (...)` clause is not redacted. Uppercase is the form used in the Databricks
  SQL reference.
- The `encryption (...)` clause is not matched at all. `databricks_copy_into` emits that clause from
  the caller supplied `source_encryption` mapping (`macros/adapters/copy_into.sql`), and for AWS
  SSE-C that mapping carries the master key.
- The key pattern is `'\w+'`, so a dotted key such as `'fs.azure.account.key'` is not redacted.
- The value pattern has no `re.DOTALL`, so a value containing a newline is not redacted.
- `search` plus a single slice replacement redacts only the first clause in a statement.

There are also two problems in the same function that are not leaks:

- Splitting the clause body on `,` raises `ValueError: not enough values to unpack (expected 2, got 1)`
  when a value contains a comma. `redact_credentials` is called on line 244, before the `try:` on
  line 246 of the `exception_handler` context manager, so the exception escapes during `__enter__`
  and the statement is never executed.
- `'.*?'` inside a repeated group backtracks exponentially. On `credential (` followed by N
  `'K' = 'V'` pairs with no closing parenthesis: 18 pairs 87 ms, 22 pairs 1,423 ms, 26 pairs
  23,760 ms.

### Steps To Reproduce

```python
from dbt.adapters.databricks.utils import redact_credentials

# 1. uppercase keyword is not redacted
redact_credentials("copy into t WITH (CREDENTIAL ('AWS_SECRET_KEY' = 'SECRET'))")
# -> "copy into t WITH (CREDENTIAL ('AWS_SECRET_KEY' = 'SECRET'))"

# 2. encryption clause is not redacted
redact_credentials("copy into t WITH (encryption ('MASTER_KEY' = 'SECRET'))")
# -> "copy into t WITH (encryption ('MASTER_KEY' = 'SECRET'))"

# 3. a comma in the value raises
redact_credentials("copy into t WITH (credential ('KEY' = 'A,B'))")
# -> ValueError: not enough values to unpack (expected 2, got 1)
```

### Expected behavior

`credential` and `encryption` clauses are redacted regardless of keyword case, every clause in a
statement is redacted, keys that are not `\w` only are handled, and a value containing a comma or a
newline neither leaks nor raises.

### Screenshots and log output

Rendering `databricks_copy_into` with `source_encryption` produces the following, and
`redact_credentials` leaves the master key untouched today:

```
copy into target_tbl
    from 's3://bucket/path'
      WITH (
        credential ('AWS_ACCESS_KEY' = 'AKIAEXAMPLE', 'AWS_SECRET_KEY' = 'SUPERSECRETVALUE')
        encryption ('TYPE' = 'AWS_SSE_C', 'MASTER_KEY' = 'MASTERSECRET123')
      )
    fileformat = parquet
```

### System information

**The output of `dbt --version`:**

```
dbt-databricks 1.12.2 (main @ 2d0fbe9e)
```

**The operating system you're using:** Linux

**The output of `python --version`:** Python 3.11.15

### Additional context

This is log hygiene rather than a remote exploit, so I am reporting it in the open, which matches how
#1469 handled the credential logging change. I have a fix ready and will open a PR for this issue.

