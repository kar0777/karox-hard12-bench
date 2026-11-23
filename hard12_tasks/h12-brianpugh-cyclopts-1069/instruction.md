You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

**kwargs captures negative-number positionals (e.g. -5) as keywords, silently corrupting args

`**kwargs` is documented as consuming tokens "starting with `--`"
(docs: Args & Kwargs), but single-hyphen tokens are also captured, including
negative numbers intended as positional values.

```python
from cyclopts import App
app = App(result_action="return_value")

@app.default
def main(*nums: int, **opts: str):
    return nums, opts

print(app(["-5", "-6"]))            # ((), {'5': '-6'})  <- expected ((-5, -6), {})
print(app(["-1", "2"]))             # ((), {'1': '2'})
app(["-1"], exit_on_error=False)    # MissingArgumentError: Parameter -1 requires an argument.
print(app(["--", "-1", "2"]))       # ((-1, 2), {})  works with "--"
```

The same function without `**opts` parses `["-5", "-6"]` as `(-5, -6)`.

**Cause:** `Argument.match` for a VAR_KEYWORD argument does
`term.lstrip("-")`, so `-1` matches as keyword `"1"`.

**Environment:** cyclopts <YOUR VERSION>, Python <YOUR VERSION>, <YOUR OS>.

I have a small fix that makes negative numbers/slices not match the catch-all
(plain `-x` still goes to kwargs, so nothing else changes); the full test suite
passes. Happy to open a PR with a regression test if the direction is right.
