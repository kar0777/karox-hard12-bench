You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

inconsistent errors for missing default dataclass value

Please check the snippet:

```python
from cyclopts import App, Parameter
from dataclasses import dataclass
from typing import Annotated

app = App()

@dataclass(frozen=True, kw_only=True)
class Opts:
    test: bool = False


type OptsParam = Annotated[Opts, Parameter(name="*")]

@app.default
def run(opts: OptsParam) -> None:
    print(opts)


if __name__ == '__main__':
    app()
```

if invoked it results with the following error:

```
Parameter * requires an argument.
```

However if `OptsParam` is defined as eager variable (without `type`):

```python
OptsParam = Annotated[Opts, Parameter(name="*")]
```

the error is now:

```
Traceback (most recent call last):
  File ".../default.py", line 14, in <module>
    @app.default
     ^^^^^^^^^^^
  File ".../env/lib/python3.12/site-packages/cyclopts/core.py", line 1518, in default
    validate_command(obj)
  File ".../env/lib/python3.12/site-packages/cyclopts/parameter.py", line 618, in validate_command
    raise ValueError(
ValueError: Parameter "opts" in function <function alias at 0x7c3831320e00> has all optional values, uses Parameter(name="*"), but itself has no default value. Consider either:
    1) If immutable, providing a default value "opts: Annotated = Annotated()"
    2) Otherwise, declaring it optional like "opts: Annotated | None = None" and instanting the opts object in the function body:
           if opts is None:
               opts = Annotated()
```

Worth noting: if both kind of definitions present in the same source then it always second kind of error even for type aliases.
