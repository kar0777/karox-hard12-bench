You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Status of `DensityDist`

Looks like an old name for `CustomDist`:

https://github.com/pymc-devs/pymc/blob/2b81f331a35d91e4249c7616d877deddf2916214/pymc/distributions/custom.py?plain=1#L845

However, the `CustomDist` references, `DensityDist`

https://github.com/pymc-devs/pymc/blob/2b81f331a35d91e4249c7616d877deddf2916214/pymc/distributions/custom.py?plain=1#L803-L813
https://github.com/pymc-devs/pymc/blob/2b81f331a35d91e4249c7616d877deddf2916214/tests/distributions/test_custom.py?plain=1#L163-L166

And it is being referenced in documentation:

https://github.com/pymc-devs/pymc/blob/2b81f331a35d91e4249c7616d877deddf2916214/docs/source/contributing/review_pr_pymc_examples.md?plain=1#L42-L43
https://www.pymc.io/projects/docs/en/latest/contributing/review_pr_pymc_examples.html#define-the-scope

## Options

- work to deprecate the `DensityDist`
- Use `CustomDist` name everywhere
