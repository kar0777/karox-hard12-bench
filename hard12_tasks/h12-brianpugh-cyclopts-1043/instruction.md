You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Support argument files with argparse-style fromfile_prefix_chars

Cyclopts can generate many long dotted options for deeply nested user classes. Would it support argument files like Python's standard-library `ArgumentParser(fromfile_prefix_chars="@")`? GCC `@file` and Java `@argfile` provide similar facilities, but `argparse` is the most directly relevant precedent in the Python ecosystem.

A possible API is:

```python
app = App(fromfile_prefix_chars="@")
```

Then argument file could be used in command line as:

```bash
my-app @run.args
```

This is not another configuration schema. The file contains ordinary CLI arguments that are expanded in place and then handled by the existing Cyclopts parser, conversion, validation, and command dispatch.

```text
# run.args — one argument per line
run
--job.database.host
db.example.internal
--job.database.port
5432
--job.workers
16
--job.description
nightly integration run
```

Following `argparse` would give small, familiar semantics. Its behavior is:

- `fromfile_prefix_chars="@"` enables the feature.
- `@run.args` is replaced in place by the file's arguments.
- Each line is one argument by default.
-  A hook equivalent to `convert_arg_line_to_args()` may customize conversion.
- Referenced argument files may be expanded recursively.


A minimal external prototype, adapted from the stdlib implementation, is:

```python
from collections.abc import Iterable
from pathlib import Path
import sys


def expand_args_from_files(
    args: Iterable[str],
    prefix_chars: str = "@",
) -> list[str]:
    expanded = []
    for arg in args:
        if not arg or arg[0] not in prefix_chars:
            expanded.append(arg)
            continue

        lines = Path(arg[1:]).read_text(encoding="utf-8").splitlines()
        expanded.extend(expand_args_from_files(lines, prefix_chars))

    return expanded


app(expand_args_from_files(sys.argv[1:]))
```

But native support would make this behavior discoverable and consistent across Cyclopts applications. If the feature fits Cyclopts and the API direction is agreed upon, I would be interested in contributing an implementation and tests. Thanks!

## References

- [`argparse` documentation: `fromfile_prefix_chars`](https://docs.python.org/3/library/argparse.html#fromfile-prefix-chars)
- [CPython 3.13.2 implementation: `_read_args_from_files()` and `convert_arg_line_to_args()`](https://github.com/python/cpython/blob/v3.13.2/Lib/argparse.py#L2246-L2274)
