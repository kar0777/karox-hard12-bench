You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`--sort-reexports` does not respect `--profile=black`

### Problem

Attempting to sort a multiline `__all__` attribute that is longer than the line limit with `isort . --sort-reexports --profile=black` wraps the lines in a non-black compatible way:

#### Before

```
__all__ = [
    "ArgumentReference",
    "ConfigurationSource",
    "HeptoFlow",
    "HeptoFlowContainer",
    "InMemoryCache",
    "Input",
    "InputReference",
    "InputValue",
    "Service",
    "parse_input_expression",
]
```

#### After

```
__all__ = ['ArgumentReference', 'ConfigurationSource', 'HeptoFlow', 'HeptoFlowContainer',
 'InMemoryCache', 'Input', 'InputReference', 'InputValue', 'Service',
 'parse_input_expression']
```

### Env

```
Python 3.12
isort 5.13.2
black 24.4.2
```

PS: Very willing to fix this myself and to PR it if someone can triage this and point me in the right direction.
