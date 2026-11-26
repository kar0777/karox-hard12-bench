You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

runLog message for negative DPA rate should be improved

When negative DPA rates are calculated, there is a warning message printed in the runLog:
https://github.com/terrapower/armi/blob/7d2b3b26296558d671a529b9180b9af9226838de/armi/physics/neutronics/globalFlux/globalFluxInterface.py#L901-L906

That message uses `single=True` and specifies a `label` with the message. That means that the message is only ever printed once in a run, even if negative DPA is calculated for every block in the core. This is not great, and does not give the user an appropriate sense for the issue.

Additionally, it would be very helpful if the location of the negative DPA rate was provided in the warning message. As of now, the user has to dig down in the neutronics kernel output file or infer the location from the database.
