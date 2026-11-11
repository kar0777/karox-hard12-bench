You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

CoercionError from convert() cannot be printed: __str__ raises AssertionError when argument is None (e.g. inside a custom converter)

Calling `convert` directly, as its docstring suggests ("Externally, may be
useful in a custom converter"), raises a `CoercionError` whose `str()`
fails:

```python
from cyclopts import convert
try:
    convert(int, ["abc"])
except Exception as e:
    print(e)
```

Expected: a message saying "abc" cannot be converted into int. Actual:
`print(e)` raises `AssertionError` at `assert self.argument is not None` in
`CoercionError._segments` (`cyclopts/exceptions.py` line 386), and a
traceback shows `CoercionError: <exception str() failed>`.

The CLI's own error output is fine, because cyclopts sets `argument` before
printing. Inside a custom converter, though, `argument` is still `None`, so a
converter that catches the error to log it and fall back hits the
AssertionError instead, and the fallback never runs:

```python
from typing import Annotated
from cyclopts import App, Parameter, convert
from cyclopts.exceptions import CoercionError

def conv(type_, tokens):
    try:
        return convert(int, [t.value for t in tokens])
    except CoercionError as e:
        print(f"warning: {e}; using 0")
        return 0

app = App()

@app.default
def main(x: Annotated[int, Parameter(converter=conv)]):
    print(x)

app(["abc"])  # expected: a warning, then 0; actual: "Invalid value for X" error, exit code 2
```

Removing the assert alone would not be enough: with `python -O` the first
snippet fails with `AttributeError` at line 393 (`self.argument.parameter`).
A message that does not need the argument when it is `None` would fix both.
Happy to send a PR if that direction suits you.

cyclopts 5.3.3 (also main at `e512a49`), Python 3.12, Windows 11.

Found with [qikly](https://github.com/gal-a/qikly), an AI-assisted test tool
I maintain, when a test it generated for `convert` failed. I reproduced it
by hand and checked every statement here against the current code.
