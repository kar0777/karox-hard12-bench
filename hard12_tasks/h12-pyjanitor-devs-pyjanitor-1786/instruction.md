You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] drop_constant_columns drops columns that mix one value with NaN and keeps all-NaN columns

## Brief Description

drop_constant_columns ignores missing values when deciding whether a column is constant, because it uses df.nunique(), which defaults to dropna=True. As a result:

- a column such as [5.0, NaN, NaN] is dropped as constant, so data is silently lost
- a column that is entirely NaN (nunique() == 0) is kept, although it is constant

The original implementation (#852) used len(df[col].unique()) == 1, which counts NaN as a value and behaves as expected. The behaviour changed when it was rewritten to df.nunique().ne(1) in #1219. R janitor's remove_constant() also keeps a column that mixes a single value with NA by default (na.rm = FALSE).

## System Information

- Operating system: macOS
- Python version (required): 3.12
- pandas 3.0.6, pyjanitor dev at 9f068d20 (0.32.42)

## Minimally Reproducible Code

```python
import numpy as np
import pandas as pd
import janitor

df = pd.DataFrame(
    {
        "constant": [1, 1, 1],
        "value_and_missing": [5.0, np.nan, np.nan],
        "all_missing": [np.nan, np.nan, np.nan],
        "varying": [1, 2, 3],
    }
)
print(df.drop_constant_columns().columns.tolist())
```

Output: ['all_missing', 'varying']

Expected: ['value_and_missing', 'varying']

## Proposed fix

Use df.nunique(dropna=False).ne(1), with a test for both cases and a CHANGELOG entry. Happy to open a PR.

Disclosure: found, reproduced and the draft fix tested locally with the help of an AI coding agent (Claude Code); reviewed before filing.

