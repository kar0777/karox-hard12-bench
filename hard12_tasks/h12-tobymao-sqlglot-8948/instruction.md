You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Teradata EXEC / EXECUTE macro calls are not parsed as structured expressions [CODEX]

On upstream `main` at `3457400b5d5a1888fc8b4327c0eab04e4cc989f4`, `EXEC` macro calls raise a parse error, while `EXECUTE` calls fall back to `exp.Command`.

```python
from sqlglot import parse_one

parse_one("EXEC example_db.example_macro(1, 'value')", read="teradata")
parse_one("EXECUTE example_db.example_macro(1, 'value')", read="teradata")
```

Expected: an `exp.Execute` with a separately accessible macro identifier and argument expressions.

A narrow parser/generator change could support ordinary macro invocations, preserve omitted arguments and other unsupported execution forms as opaque commands, and normalize `EXEC` to `EXECUTE`. This does not request full BTEQ scripting or macro execution support.

AI-assisted report prepared with Codex. The examples above are invented.

