You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Exclusion/discrimination APIs are inconsistent across channel and state modules

The analogous discrimination entry points diverge on every surface. `channel_distinguishability(p, ...) -> float` names the prior `p`, requires it positionally, and returns a scalar; `channel_exclusion(probs=None, ...) -> tuple[float, list]` names it `probs`, defaults to None, and returns operators too. Worse, `channel_exclusion` requires probs to sum to 1, while `state_exclusion` deliberately accepts unnormalized weights (antidistinguishability passes `[1]*n`), so the same weights are rejected by one API and accepted by the other. Align naming, defaults, normalization semantics, and return shapes.
