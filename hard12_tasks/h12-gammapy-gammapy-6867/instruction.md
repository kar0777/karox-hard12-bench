You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

CI fail from memory usage in test_4FGL_DR4

CI is currently failing on windows platform due to the size of the covariance matrix created in the 4FGL DR4 test:
`models = cat.to_models()`is trying to create a (39832, 39832) float64 covariance matrix and fails.
```
E           numpy._core._exceptions._ArrayMemoryError: Unable to allocate 11.8 GiB for an array with shape (39832, 39832) and data type float64

```
See: https://github.com/gammapy/gammapy/actions/runs/11309053985/job/31452518166#step:8:244

