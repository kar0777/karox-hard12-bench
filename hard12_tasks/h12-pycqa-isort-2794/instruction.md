You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Non-idempotent output with `profile = "black"`: `from X import a as b, Z` needs two runs, so `isort --check` fails after `isort`

### Summary
When a single from import mixes a plain name with an as alias, and the alias import has to wrap, the first isort run leaves the plain-name import on one line. A second run then rewrites it as a parenthesised multi-line import.

As a result, isort --check-only fails on a file that isort has just formatted.
### Steps to Reproduce

1. Create `pyproject.toml`:
 ```toml
   [tool.isort]
   profile = "black"
   line_length = 40
   ```
2. Create `t.py` containing one line:
 ```python
   from requests import long_name_here as long_name_here2, Z
   ```
3. Run:
 ```
   isort t.py
   isort --check-only --diff t.py; echo "exit code: $?"
   ```
### Expected Behaviour:
The output of the first run is stable, so the second command passes with exit code 0.
### Actual Behaviour:
The first command prints `Fixing .../t.py`. The second reports `Imports are incorrectly sorted and/or formatted.` and exits with code 1:
```diff
-from requests import Z
+from requests import (
+    Z,
+)
 from requests import (
     long_name_here as long_name_here2,
 )
```
A third run changes nothing, so the output settles after two runs, but only after the first run's output has been rejected.
### Environment
- isort 10.0.0b3 
- Branch: main
- Commit: 841e43126cd2ca74751b421afd00d90ca36932e5
- Python 3.14.4
- Ubuntu 26.04.1 LTS (WSL)
### Notes
- I only varied `line_length`. 
- This appears related to [#2352](https://github.com/PyCQA/isort/issues/2352), which reported non-idempotent formatting involving aliased and directly imported names. That issue was closed after the behaviour was reported fixed on main. However, I can still reproduce similar behaviour on isort 10.0.0b3.
- This looks related to, but distinct from, #2694 (comments on names hoisted to the `(` line), #2741 (comment lost on `X as X` re-exports).My reproduction contains no comments.
- I haven't traced the cause. My guess is that the first pass decides whether to wrap `from requests import Z` using the original combined line, and the second pass decides differently on the already-split line. I haven't verified that.
- Happy to try a fix and open a PR if that would help.


