You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Actual man pages

### What is the problem or limitation you are having?

Can't actually write man pages

### Describe the solution you'd like

Take in troff, ship man page

### Describe alternatives you've considered

* Make a wrapping script that temporarily overrides the long description
* Run a side process that watches for briefcase to write out the man page and rewrite it
* Munge the resulting packages to insert the correct man page

### Additional context

This was discussed in discord
