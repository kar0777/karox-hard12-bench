You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Avoid overriding pandas 3.1 DataFrame.select

## Problem

pandas 3.1 introduces `DataFrame.select`, which selects columns and supports pandas column expressions and computed keyword columns:

```python
df.select("a", new_col=pd.col("b") * 2)
```

pyjanitor currently registers its deprecated `janitor.select` function as a DataFrame method via `pandas_flavor`. With pandas 3.1, importing `janitor` therefore attempts to register an accessor named `select` over an existing pandas method and emits an accessor-registration warning. The registration can override pandas' implementation, so after importing pyjanitor:

```python
import pandas as pd
import janitor

df.select(...)
```

may resolve to pyjanitor's legacy row/column selector rather than pandas' `DataFrame.select`. The signatures and semantics are incompatible.

This is a namespace collision with `DataFrame.select`, not with a top-level `pandas.select`.

## Proposed resolution

- Stop registering the legacy `janitor.select` function as `.select` when pandas provides `DataFrame.select` (ideally remove the registration altogether).
- Retain the functional `janitor.select` symbol temporarily for compatibility, with its existing deprecation warning.
- Continue directing users to `janitor.select_columns` and `janitor.select_rows`.
- Remove the functional alias in the next major release, with a migration note.

## Regression coverage

Under pandas 3.1, importing `janitor` should not override or shadow `DataFrame.select`, and this should retain pandas semantics:

```python
import pandas as pd
import janitor

df = pd.DataFrame({"a": [1], "b": [2]})
result = df.select("a")
assert list(result.columns) == ["a"]
```

Also test a pandas-only signature such as a computed keyword column, and assert that importing pyjanitor does not emit an accessor-overwrite warning.

References:

- pandas `DataFrame.select`: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.select.html
- pyjanitor `select` source: https://github.com/pyjanitor-devs/pyjanitor/blob/dev/janitor/functions/select.py
- Existing pandas 3.x compatibility tracker: #1546
