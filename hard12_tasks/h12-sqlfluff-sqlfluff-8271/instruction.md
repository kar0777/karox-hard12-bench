You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

2.0.0a1 Auto-migration of deprecated config value `rules:max_line_length` has no effect

### Search before asking

- [X] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### What Happened

Running SQLFluff `2.0.0a1` with an existing config file that has `rules:max_line_length` yields the following warning

```
deprecated config value `rules:max_line_length`
```

which suggests that the (new) value will get automatically applied.

However, a run of `sqlfluff lint` throws a lot of `L016` warnings with default value (80)

```
L: 228 | P:  15 | L016 | Line is too long (106 > 80).
L: 229 | P:  13 | L016 | Line is too long (106 > 80).
L: 335 | P:   9 | L016 | Line is too long (227 > 80).
```

### Expected Behaviour

see above

### Observed Behaviour

see above

### How to reproduce

see above

### Dialect

all

### Version

2.0.0a1

### Configuration

```
[sqlfluff:rules]
max_line_length = 800
```

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [X] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

