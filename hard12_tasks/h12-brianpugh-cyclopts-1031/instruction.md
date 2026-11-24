You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

support for generic type aliases used for annotations

First of all, thanks for your work!

Please check the example snippet below. It has two commands `base` and `tvar` which are intended to behave the same. But `base` uses pair of exact type aliases whereas `tvar` uses generic type aliases:

Example:

```python
from dataclasses import dataclass
from typing import Annotated
from cyclopts import App, Parameter


app = App()


@dataclass(frozen=True, kw_only=True)
class Upper:
    upper: bool = False


@dataclass(frozen=True, kw_only=True)
class Lower:
    lower: bool = False


type UpperOpts = Annotated[Upper, Parameter(name='*')]
type LowerOpts = Annotated[Lower, Parameter(name='*')]


@app.command
def base(
    *,
    upper: UpperOpts = Upper(),
    lower: LowerOpts = Lower(),
) -> None:
    print(upper.upper, lower.lower)


type Opts[OptsT] = Annotated[OptsT, Parameter(name='*')]


@app.command
def tvar(
    *,
    upper: Opts[Upper] = Upper(),
    lower: Opts[Lower] = Lower(),
):
    print(upper.upper, lower.lower)


if __name__ == '__main__':
    app()
```

```
$ python ./example.py base --upper --lower
$ python ./example.py tvar --upper --lower
```

Expected result:

Both commands behave the same.

Observed result:

Generic type alias version does not work correctly:

```
Command "tvar" parameter --upper requires an argument.
```
