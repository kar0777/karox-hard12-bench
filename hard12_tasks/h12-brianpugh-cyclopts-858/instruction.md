You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Importing pydantic breaks Dataclass Commands

This works if I invoke the command `test`:

```python
from dataclasses import dataclass, field
#import pydantic

from cyclopts import App

app = App(result_action=["call_if_callable", "print_non_int_sys_exit"])

@app.command
@dataclass
class Test:
    numbers: list[int] = field(default_factory=lambda: [1,2,3])

    def __call__(self) -> str:
        return str(self.numbers)

if __name__ == "__main__":
    app()
```

```shell
python -m test test
[1, 2, 3]
```

If, however, I uncomment the line `import pydantic`, I get:
```shell
python -m test test
╭─ Error ────────────────────────────────────────────────────────────╮
│ 1 validation error for list[int]                                   │
│   Input should be a valid list [type=list_type,                    │
│ input_value=<factory>, input_type=_HAS_DEFAULT_FACTORY_CLASS]      │
│     For further information visit                                  │
│ https://errors.pydantic.dev/2.13/v/list_type                       │
╰────────────────────────────────────────────────────────────────────╯
```

