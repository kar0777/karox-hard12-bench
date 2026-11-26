You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Unexpected exception with parameter without values specified by keyword and with an abstract type

```python
# test.py
from collections.abc import Sequence
from typing import Annotated

from cyclopts import App, Parameter

app = App()

@app.default
def foo(*, values: Annotated[Sequence[int], Parameter(consume_multiple=True, allow_repeating=False)]) -> None:
   print(values)

app()
```

If you type

```bash
$ python test.py --values
```

you'll get:

```
Traceback (most recent call last):
...
TypeError: Can't instantiate abstract class Sequence without an implementation for abstract methods '__getitem__', '__len__'
```
