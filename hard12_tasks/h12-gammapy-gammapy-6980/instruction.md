You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Refactor JFactory line-of-sight integration

The `JFactory` line-of-sight integration is expressed in terms of radial branches. Thus, depending on the observer position and viewing direction, `_integrate_los()` needs to distinguish several geometrical cases and combine different branches of the integral.

The current implementation is working correctly after the recent LoS geometry fixes, but the parameterization makes the integration logic more complicated than necessary.

We propose refactoring the LoS integration using a cleaner and more general parameterization that can describe the physical forward line of sight with a single integration interval, independently of whether the observer is inside or outside the halo.

