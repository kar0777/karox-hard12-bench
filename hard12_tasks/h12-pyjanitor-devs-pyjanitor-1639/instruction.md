You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

pivot_longer column_level collapses duplicate labels and loses the row index

## Summary

When `pivot_longer` receives `column_level`, `_data_checks_pivot_longer` reconstructs the DataFrame through a dictionary keyed by labels from the selected level. This has two observable effects:

1. Repeated labels at that level are silently collapsed, so measured columns and their values can be lost.
2. The original row index is discarded, even when `ignore_index=False`.

## Minimal reproducer

```python
import pandas as pd
import janitor

columns = pd.MultiIndex.from_tuples([("x", "a"), ("x", "b")])
df = pd.DataFrame(
    [[1, 2], [3, 4]],
    columns=columns,
    index=pd.Index([10, 20], name="row"),
)

result = df.pivot_longer(column_level=0, ignore_index=False)
print(result)
```

The result contains only values from the second `x` column and has a new `RangeIndex`. Both selected columns should participate in the reshape, and the original index labels should be retained and repeated.

## Likely cause

The `column_level` branch converts the columns to a dictionary before constructing a new DataFrame. Duplicate dictionary keys overwrite earlier entries, and the constructor is not given the original index.

## Proposed scope

- Replace dictionary reconstruction with a shallow DataFrame copy followed by column reassignment.
- Add regression coverage for repeated labels at the selected level.
- Add regression coverage for `ignore_index=False` with a non-default index.
- Preserve extension-array dtypes and existing column-selection behavior.

## Performance note

On a 10,000-row by 100-column frame, shallow relabeling took about 0.014 ms versus about 1.08 ms for dictionary reconstruction while preserving shape and index.
