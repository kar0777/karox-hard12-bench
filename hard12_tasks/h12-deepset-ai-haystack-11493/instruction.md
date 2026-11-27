You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

fix: InputSocket.__post_init__ crashes with IndexError on unsubscripted Variadic type

In `InputSocket.__post_init__`, line 100 calls `get_args(get_args(self.type)[0])[0]` to unwrap the inner type from a `Variadic` / `GreedyVariadic` annotation. This assumes the wrapped type is always a subscripted generic (e.g. `Iterable[int]`), but if a developer annotates a run-method parameter with a bare `Annotated[Iterable, HAYSTACK_VARIADIC_ANNOTATION]` — using `Iterable` without a type argument — then `get_args(Iterable)` returns an empty tuple `()`, and the unconditional `[0]` index raises `IndexError: tuple index out of range`.

This crash surfaces at component instantiation time (not import time), so it bypasses static type checking and takes down the whole component construction.

**Reproduction:**
```python
from typing import Annotated
from collections.abc import Iterable
from haystack import component
from haystack.core.component.types import HAYSTACK_VARIADIC_ANNOTATION

@component
class BadJoiner:
    @component.output_types(result=str)
    def run(self, inputs: Annotated[Iterable, HAYSTACK_VARIADIC_ANNOTATION]):
        return {"result": ""}

j = BadJoiner()  # IndexError: tuple index out of range
```

**Expected:** a clear `ComponentError` explaining that a type argument is required, e.g. `Variadic[int]`.
