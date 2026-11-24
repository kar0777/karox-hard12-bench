You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] pandas pivot_longer: output aliases input under CoW

## Summary

Bug in pandas `pivot_longer` (`janitor/functions/pivot.py`, dev @ `5b4e755`, pandas 3.0.6): the output shares memory with the input, so writes to the result modify the caller's DataFrame.

The performance half of this issue (the quadratic per-label `.value` loop) has moved to #1821.

### Bug

`_build_df` passes raw `ravel` views of the source blocks to `pd.DataFrame(..., copy=False)`. Copy-on-Write does not track those references:

```python
df2 = pd.DataFrame(np.arange(8.0).reshape(2, 4), columns=["x1", "x2", "x3", "x4"])
df2.insert(0, "id", [1, 2])
o2 = df2.pivot_longer(index="id", names_to=".value", names_pattern="(x)\\d")
o2.loc[0, "x"] = -1.0          # df2.loc[0, "x1"] is now -1.0
o3 = df2.pivot_longer(index="id")
o3.loc[0, "value"] = -7.0      # df2.loc[0, "x1"] is now -7.0
```

In a 2,000-case fuzz, in-place writes to the output changed the input in 405 cases, across the plain, `.value`-only (single and multiple labels), `.value` + other names, and `names_transform` paths.

Later review on #1820 found two more alias sources: `datetime64`/`timedelta64` value columns (`DatetimeArray`/`TimedeltaArray` ravel views), and `np.tile(DatetimeArray, 1)` for a datetime index column with a single value column.

## Fix

Copy only where a view of the input is created: after each `._values.ravel(...)` and after `np.tile` in `_build_index`, when `np.may_share_memory` reports overlap. Being fixed in #1820.

## Verification

- A regression test for each path: write to the output and assert the input is unchanged.
- The extra memory should be exactly one copy of the columns that were views. Nothing extra should be copied where pandas already returns new arrays.

Related: #1821, #1769 (polars).

