You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Enum with __init__ method cannot be used to supply a set of choices

An enumeration cannot be used to supply a set of choices if it has an `__init__`  method.

To see why:

```python
from enum import Enum

from cyclopts import App

app = App()

class Choice(Enum):
    A = 0
    B = 2

    def __init__(self, value: int) -> None:
        ...

@app.default
def default(choice: Choice) -> None:
    app.console.print(f"Your choice: {choice}")

app()
```

```bash
$ my-program a
╭─ Error ───────────────────────────────────────────────────────────╮
│ Invalid value for CHOICE.VALUE: unable to convert "a" into int.   │
╰───────────────────────────────────────────────────────────────────╯
```

cyclopts version: 4.22.2
