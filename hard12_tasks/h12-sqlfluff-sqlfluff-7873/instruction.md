You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Ability to force color in the sqlfluff command

### Search before asking

- [x] I searched the [issues](https://github.com/sqlfluff/sqlfluff/issues) and found no similar issues.


### Description

I tried running `sqlfluff lint --color | tee .result`, but the output has no color.
I would like to force color for Bitbucket Pipelines output, because scripts don't detect it as a TTY that supports color, but Bitbucket Pipelines actually picks up on color codes and colors the output as one would expect.

If there's no way to force color output, then it would be nice to have an option to do so. Or have --color force color output.

Also, any workaround would be helpful too.

### Use case

_No response_

### Dialect

No

### Are you willing to work on and submit a PR to address the issue?

- [ ] Yes I am willing to submit a PR!

### Code of Conduct

- [x] I agree to follow this project's [Code of Conduct](https://github.com/sqlfluff/sqlfluff/blob/main/CODE_OF_CONDUCT.md)

