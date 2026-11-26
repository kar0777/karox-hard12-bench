You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add an "auto" option for iOS simulator selection

### What is the problem or limitation you are having?

At present, `briefcase run iOS` requires either a `-d <simulator ID>` option, or a manual selection from a simulator list. This is inconvenient for CI purposes when the available simulators can change.

It should be able to "auto select" a simulator when the specific image doesn't matter.

### Describe the solution you'd like


`briefcase run iOS -d auto` should select a good candidate simulator - use the most recent iOS version, selecting an "SE-class" device (i.e., iPhone 17e). This matches the default behavior of the CPython iOS testbed runner.

### Describe alternatives you've considered

We could also make `-d auto` the default behavior, and make a bare `-d` an option to "show the full simulator list". 

### Additional context

This problem doesn't exist on Android because (a) Android requires explicit creation of a simulator, and (b) Briefcase already has a syntax to "auto drive" the creation of an emulator for test purposes.
