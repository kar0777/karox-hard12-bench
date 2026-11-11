You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

NOQA mode adds another `# NOQA` marker on every run, so the output never converges

NOQA mode adds another `# NOQA` marker on every run, so the output never converges

With `multi_line_output=7` (NOQA) and `use_parentheses=True`, an import that carries an opening-line comment gets a new `# NOQA` marker appended on every run:

```python
>>> import isort
>>> src = ("from my_package.my_module import super_long_file_name as super_long_alias"
...        "  # type: ignore\n")
>>> opts = dict(multi_line_output=7, use_parentheses=True, line_length=40)
>>> isort.code(src, **opts)
'from my_package.my_module import super_long_file_name as super_long_alias  # NOQA  # type: ignore\n'
>>> isort.code(isort.code(src, **opts), **opts)
'from my_package.my_module import super_long_file_name as super_long_alias  # NOQA  # NOQA  # type: ignore\n'
```

Each pass reads the previous markers back as one comment and appends another, so the statement never settles and `isort --check` keeps failing on the file it just wrote. The non-parenthesised path (`use_parentheses=False`) is already stable, and output that ends with the marker instead of `# type: ignore` is also what that path produces.

Cause: in `isort/output.py::_build_as_imports` the statement is wrapped by `wrap.line()` first and the opening-line comment is attached afterwards; NOQA mode never wraps in parentheses, so there is no opening parenthesis to attach the comment to, and the comment lands behind the marker. A fix that merges the comments before wrapping and keeps the output a fixpoint is ready; I will open a pull request for it. This issue is to claim the behaviour before anyone else starts on it.

