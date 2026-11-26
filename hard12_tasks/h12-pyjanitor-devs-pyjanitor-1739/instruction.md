You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] row_to_names fails on slices without a start or a stop

The docstring says `row_numbers` can be a slice, but slices without a start or a stop break:

```python
import polars as pl, pandas as pd, janitor, janitor.polars

pl.DataFrame({"a": ["x", "1"], "b": ["p", "2"]}).row_to_names(slice(None, 1))
# TypeError: unsupported operand type(s) for -: 'int' and 'NoneType'

df = pd.DataFrame({"a": list("wxyz"), "b": list("1234")})
df.row_to_names(slice(None, 2), remove_rows_above=True)
# TypeError
df.row_to_names(slice(-2, None), remove_rows_above=True).shape
# (6, 2), from a 4 row frame
```

The polars version uses `row_numbers.start` and `row_numbers.stop` directly, and so do the `remove_rows_above` branches in pandas. Normalizing with `slice.indices()` fixes both. Happy to open a PR.

