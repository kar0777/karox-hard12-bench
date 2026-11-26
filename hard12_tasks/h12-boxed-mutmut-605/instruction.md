You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

mutmut run crashes on float literals too large for a float, like 1e999

If a source file contains a float literal that is too large for a float, `mutmut run` aborts while creating mutants. `1e999` is a fairly common way to spell infinity, so this is easy to hit:

```python
# src/calc/limits.py
INFINITY = 1e999
```

```
$ mutmut run
...
  File ".../mutmut/__main__.py", line 121, in create_mutants
    raise result.error
libcst._nodes.base.CSTValidationError: Number is not a valid float.
```

The same happens for `-1e999`, `1.5e400` and the imaginary `1e999j`.

The cause is `operator_number` in `src/mutmut/mutation/mutators.py`. The literal evaluates to `inf`, so the mutant becomes `repr(inf + 1)`, which is `"inf"`. That isn't a valid number literal, so libcst raises, and the error stops the whole run instead of just skipping that one mutation.

Since `inf + 1` is still `inf` and there is no literal for it, I think `operator_number` should yield nothing in that case. The other mutations of the line (for example `a = 1e999` → `a = None`) would still be generated. I have a fix with tests and can open a PR.
