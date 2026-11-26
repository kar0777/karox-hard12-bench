You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

_recalculate_caches should autodetect the list of fields

### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### Description

Internal quality improvement. The `BaseSegment._recalculate_caches()` function has a hardcoded list of `@cached_property` fields to clear. This is easy to overlook when adding a new cached property. Can we generate this list of fields automatically by looking for fields marked with the the `@cached_property` decorator? That would eliminate a potential source of tricky bugs.

### Use case

_No response_

### Dialect

n/a

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

