You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

A bare `#` is dropped and leaves trailing whitespace when the import line is wrapped

A bare `#` on an import line that has to be wrapped disappears, and the whitespace before it is left behind:

```python
>>> import isort
>>> isort.code("from sys import super_long_name  #\n", force_grid_wrap=3, line_length=30)
'from sys import \\\n    super_long_name  \n'
```

The `#` is gone and the second line ends with two spaces. A second run strips them, so the output is not a fixpoint. The same input with a non-empty comment is handled correctly:

```python
>>> isort.code("from sys import super_long_name  # x\n", force_grid_wrap=3, line_length=30)
'from sys import \\\n    super_long_name  # x\n'
```

Star imports hit the same path even without wrapping, minus the trailing space:

```python
>>> isort.code("from sys import *  #\n", line_length=30)
'from sys import *\n'
```

In `isort/wrap.py`, `comment` is `None` when the line has no `#` and `""` for a bare `#`. The checks `if comment` and `comment and (...)` treat the empty string as "no comment", so the comment is never put back and the trailing whitespace split off by `content.split("#", 1)` stays on the line.

Expected:

```python
>>> isort.code("from sys import super_long_name  #\n", force_grid_wrap=3, line_length=30)
'from sys import \\\n    super_long_name  #\n'
>>> isort.code("from sys import *  #\n", line_length=30)
'from sys import *  #\n'
```

I have a fix with regression tests and will open a pull request.

