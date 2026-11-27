You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Bug report: `allow_leading_hyphen=True` is broken by #639

Hi, thank you for making and continuously improving cyclopts 👋 ❤️ 

When upgrading cyclopts to the latest version, I noticed a regression when using `allow_leading_hyphen=True` and I bisected it to #639.

Here is a minimal example:

```python
from typing import Annotated
import cyclopts
from cyclopts import App, Parameter

app = App(help_flags=[], version_flags=[])

@app.default
def k(*args: Annotated[str, Parameter(allow_leading_hyphen=True)]):
    # passthrough wrapper
    print(f"received: {list(args)}")

app(["-c=blue", "build", "thing"])
```

Before #639 (<4.1.0), the output is:

```
received: ['-c=blue', 'build', 'thing']
```

After #639 (>=4.1.0), the output is:

```
received: ['-c', '-=', '-b', '-l', '-u', '-e', 'build', 'thing']
```

`allow_leading_hyphen=True` should take precedence I think? Thanks in advance for taking a look at it!
