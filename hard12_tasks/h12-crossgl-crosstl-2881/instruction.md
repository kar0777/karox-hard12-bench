You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Slang output: error[E30015]: undefined identifier 'gl_NumWorkGroups'

<!-- crosstl-coverage key=wrong/slang/output/19a8381d6c8d -->
<!-- crosstl-coverage features=num-workgroups -->
The coverage probe for `num-workgroups` (Slang output, BuiltIn.NumWorkgroups) gives a wrong result. CrossTL translates the generated CrossGL probe but fails without a typed diagnostic or produces code that slangc rejects.

```text
error[E30015]: undefined identifier 'gl_NumWorkGroups'
```

Reproduce it with:

```bash
python -m tools.coverage run --backend slang --direction output --feature num-workgroups --keep probes
```

`probes/slang-output/num-workgroups/` then holds the probe and, if CrossTL produced one, its translation.

The coverage workflow closes this issue when no probe fails this way. [COVERAGE.md](https://github.com/CrossGL/crosstl/blob/coverage/COVERAGE.md#slang-output) has the current results.

