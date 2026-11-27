You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`isort: skip` not working when futures imports are present

## Bug summary
`isort: skip` seems to not work when there is a futures imports are present.


## Reproducible example

Running `isort test.py` on this example works well. No changes are made.

```python
# test.py
from foo import bar  # isort: skip
from bar import baz

baz + bar
```

When modifying the file to include a futures import:

```python
from __future__ import annotations

from foo import bar  # isort: skip
from bar import baz

baz + bar
```

isort now moves the marked import to the bottom. 
