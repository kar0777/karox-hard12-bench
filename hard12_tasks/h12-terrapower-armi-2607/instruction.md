You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`Database.genTimeSteps()` does not support EOL

@albeanth and I identified ~two places~ one place where the ARMI codebase does not support the new `EOL` time point being written to the database (added in [PR 1090](https://github.com/terrapower/armi/pull/1090)):

1. `Database3.genTimeSteps()`:

https://github.com/terrapower/armi/blob/8b5163a8b61ebe704419d2d77067bfcf8018f328/armi/bookkeeping/db/database3.py#L612

Returns `(cycle, node)`, but if the `EOL` is present in the DB, it just returns the last time node twice.

~2. `Database3.load()` takes in `cycle` and `node` as integers, thus not allowing us to load an EOL timestep:~

Never mind. Drew correctly points out you can do this: `db.load(0, 1, statePointName="EOL")`.
