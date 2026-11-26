You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

perf: renyi_entropy computes the spectrum multiple times

### Summary
`state_props/renyi_entropy.py` factors `rho` more than once. Line 95 calls `is_density(rho)`, which factors `rho` via `is_positive_semidefinite` -> `eigvalsh`; line 104 then calls `np.linalg.eigvalsh(rho)` again. The `alpha == 1` branch (line 102) is worse: it delegates to `von_neumann_entropy`, which re-validates and re-factors a third time.

This is the same pattern recently fixed in `von_neumann_entropy`: compute the spectrum once and validate from it.

### Fix
Compute `eigs = np.linalg.eigvalsh(rho)` once, validate the density-matrix conditions from the spectrum plus `np.isclose(np.trace(rho), 1)`, and drop the `is_density` import. Mirror the `von_neumann_entropy` refactor.

Good first issue.

