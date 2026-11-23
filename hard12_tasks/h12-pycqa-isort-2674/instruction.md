You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

isort skips a whole line when a semicolon is followed by a comment

## Description

`skip_line` in `isort/_parse_utils.py` guards on the code *before* the comment but then loops over the *unstripped* line, so the comment text is treated as if it were a statement:

```python
if ";" in line.split("#")[0] and needs_import:
    for part in (part.strip() for part in line.split(";")):
        if (
            part
            and not part.startswith("from ")
            and not part.startswith(("import ", "cimport "))
        ):
            should_skip = True
```

The guard uses `line.split("#")[0]`, which proves the intent to ignore comment text. The loop on the next line does not, so for:

```python
import sys; # comment
```

the parts are `['import sys', ' # comment']`. The second part is non-empty and starts with none of `from ` / `import ` / `cimport `, so `should_skip` becomes `True` and the whole line is skipped.

`skip_line` is called from `isort/parse.py` and `isort/identify.py`, so the import disappears from both the sorter and the public API.

## Reproduction

```python
>>> import isort
>>> src = "import sys; # comment\nimport os\n"
>>> isort.code(src)
'import sys; # comment\nimport os\n'      # unchanged
>>> isort.check_code(src)
True                                        # "Everything Looks Good!"
>>> [str(i) for i in isort.find_imports_in_code(src)]
[':2 import os']                             # 'import sys' is missing
```

The CLI is the part that matters for CI:

```
$ cat bad.py
import sys; # comment
import os
$ isort --check-only bad.py
$ echo $?
0
$ isort --diff bad.py
$ echo $?
0
```

Controls that already work: the same file without the comment sorts, and a real non-import statement (`import pdb; pdb.set_trace()`) is correctly left alone.

## Expected behaviour

`test_same_line_statements` in `tests/unit/test_isort.py` states the rule for same-line statements: two imports on a line are split and sorted, a non-import statement leaves the line alone. A trailing comment is neither, and a comment is not a statement, so `import sys; # comment` should be treated the same as `import sys;`:

```
'import os\nimport sys  # comment\n'
```

and `isort.check_code` should return `False` for the mis-sorted input.

## Environment

- isort 6.x, `main` at `c85a44fd9f27881ce16b7fa10a833afdf8d919ec`
- Python 3.11, macOS

## Fix

In `skip_line`, split the code once and use it for both the guard and the loop.

That alone is not enough to get correct output, though. With `skip_line` fixed, `isort/parse.py` exposed a second problem: the end-of-line comment was attached to `statements[-1]`, and a line ending in `;` leaves a spurious empty statement there, so the comment came back as a stray leading line:

```
'# comment\nimport os\nimport sys\n'
```

Dropping that empty statement before attaching the comment gives the expected output above. Both changes are in the same two-line neighbourhood and are needed for `import sys; # comment` to round-trip.

