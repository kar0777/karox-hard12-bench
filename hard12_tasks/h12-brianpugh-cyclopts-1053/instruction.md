You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Automatically generated application name lack support for `python -m <module/package>` scenarios

When running cyclopts-based applications via `python -m <module/package>`, the auto-generated application name does not correspond to the actual command used to run the application. Since this name is used in the `Usage` text, it may confuse end users:

- When running a module: `Usage: mymodule.py [ARGS...]` instead of the expected `Usage: python -m mymodule [ARGS...]`
- When running a package: `Usage: __main__ COMMAND` instead of the expected `Usage: python -m mypkg COMMAND`
- When running a module within a package: `Usage: run.py [ARGS...]` instead of the expected `Usage: python -m mypkg.run [ARGS...]`

The implementation in the standard library `argparse` can be referenced as an example: https://github.com/python/cpython/blob/02843599bdcf07d6864024078fdbc9a338ee639e/Lib/argparse.py#L1958
