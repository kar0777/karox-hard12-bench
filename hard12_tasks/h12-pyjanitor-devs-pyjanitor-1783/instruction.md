You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

select_columns/select_rows: an empty list should return an empty DataFrame

## Problem

An empty list passed to `select_columns` or `select_rows` should select nothing and return an empty DataFrame along that axis. Instead it crashes with an internal NumPy error.

Observed on `dev` at `17ee4d71` (pandas 3.0.6):

```python
import pandas as pd
import janitor  # noqa: F401

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

df.select_columns([])
# ValueError: need at least one array to concatenate

df.select_rows([])
# ValueError: need at least one array to concatenate

df.select(columns=[])
# ValueError: need at least one array to concatenate
```

Expected:

```python
df.select_columns([]).shape  # (2, 0)
df.select_rows([]).shape     # (0, 2)
```

Other empty selectors behave inconsistently:

| selector | `select_columns` | `select_rows` |
|---|---|---|
| `[]` | `ValueError: need at least one array to concatenate` | same |
| `()` | `KeyError: No match was returned for ()` | same |
| `np.array([])` | `KeyError` | same |
| `pd.Index([])` | `KeyError` | same |
| `pd.Series([], dtype=object)` | `KeyError` | same |
| `[False, False]` | `(2, 0)` | `(0, 2)` |

An all-`False` boolean mask already returns an empty frame, so "select nothing" is supported; only the empty-list form is broken.

## Cause

The list dispatch of `_select_index` in `janitor/functions/select.py` resolves each entry and ends with `return np.concatenate(include)` (line 955 on `dev`). With an empty list, `include` is empty and `np.concatenate` raises.

## Proposed fix

1. **An empty list selects nothing** on either axis: `select_columns([])` returns all rows and no columns, and `select_rows([])` returns no rows and all columns. `select(columns=[])` and `select(rows=[])` follow.
2. **The complement of `[]` selects everything,** matching `df.drop(columns=[])` in pandas and the existing `slice(None)` / all-`False` mask behavior:
   - `select_columns([], invert=True)` and `select_rows([], invert=True)`
   - `DropLabel([])`, which currently raises the same `ValueError: need at least one array to concatenate`
3. **Empty list-likes follow the same rule:** `np.array([])`, `pd.Index([])` and an empty `pd.Series` select nothing, as in pandas (see below).
   - **`()` is excluded.** pyjanitor treats tuples as labels, and pandas does too: `df[()]` raises `KeyError: ()` on flat columns and returns every column on a MultiIndex. `()` should keep its current label semantics.
4. **Tests:** both axes, plain and MultiIndex, unique and duplicate labels, with and without `invert`, and `DropLabel([])` alone and combined with other selectors (e.g. `["a", DropLabel([])]`).

## pandas behavior

pandas treats an empty list-like as "select nothing" everywhere. Observed on pandas 3.0.6, with both flat and MultiIndex columns; the result keeps the source column-index type:

| expression | shape for a 2×2 frame |
|---|---|
| `df[[]]`, `df.loc[:, []]`, `df.iloc[:, []]` | `(2, 0)` |
| `df.loc[[]]`, `df.iloc[[]]` | `(0, 2)` |
| `df.loc[:, pd.Index([])]`, `df.loc[:, np.array([])]` | `(2, 0)` |
| `df.filter(items=[])`, `df.reindex(columns=[])` | `(2, 0)` |
| `df[()]` | flat: `KeyError: ()`; MultiIndex: `(2, 2)` |

## Why now

#1753 adds `conditional_join(output_columns=...)` and routes every selector through `select_columns`. The discussion there is to drop `None` as conditional_join's own "omit this side" value. Today the only way to express "no columns" through `select_columns` is `DropLabel(slice(None))`. An empty list would be the natural, shorter spelling: `output_columns={"left": [], "right": ...}`.

