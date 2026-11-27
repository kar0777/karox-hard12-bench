You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Create whole project FTE trace

A method within the `Project` model that returns the project FTE trace, adding together the traces of all its phases as a pandas Series. If a date range is provided as input, that one is used, otherwise the project start and end dates are used instead. 

Like with the phases, any date outside of the project date range should have a value of zero.

If a project has no phases, the output should be a trace full of zeros.
