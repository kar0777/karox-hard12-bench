You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Enums with custom `__init__` cannot be imported under mutmut: `KeyError: '_mutmut_orig'`

My project has enums with a custom `__init__`, and `mutmut run` stops at the stats run because the mutated module cannot be imported.

`Enum` calls `__init__` once per member while the class is still being created, before the trampoline table of its methods is assigned after the class body. `__new__` is already in `NEVER_MUTATE_FUNCTION_NAMES` for that reason.

Skipping `__init__` and `_generate_next_value_` on an enum class the same way works for me. Shall I submit a PR?

## Reproducer

mutmut 3.8.0, pytest 9.1.1, Python 3.15, `mutmut run`:
```
File ".../mutmut/mutation/trampoline.py", line 75, in trampoline
  orig_func = mutants_dict["_mutmut_orig"]
KeyError: '_mutmut_orig'
ERROR tests/test_color.py - KeyError: '_mutmut_orig'
failed to collect stats. runner returned 2
```

`src/color.py`:
```python
from enum import Enum


class Color(Enum):
    RED = 1

    def __init__(self, value):
        self.label = f"c{value}"
```

`tests/test_color.py`:
```python
from color import Color


def test_label():
    assert Color.RED.label == "c1"
```

`pyproject.toml`:
```toml
[tool.mutmut]
source_paths = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
```

