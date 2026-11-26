You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Parameter metadata on a container value type in dict[str, ...] is ignored

A dict whose value type is a container with its own `Parameter` metadata silently ignores that metadata. Here the validator runs for the top-level parameter but never for the dict value:

```python
from typing import Annotated

import cyclopts
from cyclopts import App, Parameter
from cyclopts.config import Dict


def reject_empty(type_, value):
    print(f"validator called with {value!r}")
    if not value:
        raise ValueError("must not be empty")


Ids = Annotated[list[int], Parameter(validator=reject_empty)]

top = App(config=Dict({"x": [1]}), result_action="return_value")


@top.default
def main_top(x: Ids):
    return x


nested = App(config=Dict({"x": {"k": [1]}}), result_action="return_value")


@nested.default
def main_nested(x: dict[str, Ids]):
    return x


print(cyclopts.__version__)
print("top:", top([]))
print("nested:", nested([]))
```

```
5.2.0
validator called with [1]
top: [1]
nested: {'k': [1]}
```

A value-type `Parameter(converter=...)` is ignored the same way. Scalar value types work (e.g. `dict[str, PositiveInt]`), because only the scalar dispatch at the end of `_convert_entry` re-attaches the stashed `annotations_`; the iterable (`convert_priv(type_, tokens)`) and nested-dict branches pass the resolved type with the metadata stripped. Probably the same `convert()` vs `_convert()` metadata-survival issue as before, just for container-valued entries.

Found while reviewing #993 (Copilot flagged it for the empty-value early return, but the non-empty path has the same gap).

