You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Support multiple constraints and constraint files

Fromager 0.82 and earlier only supports a single constraints file with unique entries. `packaging` 26.1 added a new feature to check if a [SpecifierSet is satisfiable](https://packaging.pypa.io/en/stable/specifiers.html). This feature finally allows us to support multiple constraints and constraints files safely.

```python
>>> from packaging.specifiers import SpecifierSet
>>> SpecifierSet("<1").is_unsatisfiable()
False
>>> SpecifierSet("<1,>2").is_unsatisfiable()
True
```

1. extend `fromager.constraints.Constraints.add_constraint` to combine constraints and verify that the combined constraints are satisfiable.
2. update the global `-c` / `--constraints-file` option to support multiple constraints files
