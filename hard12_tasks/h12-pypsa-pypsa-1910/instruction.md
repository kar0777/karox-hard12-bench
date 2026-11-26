You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

More forms of `Line` limits

- enforced limits on voltage angle differences (directly translate to `s_nom = 1/x_pu_eff * angle_diff`).

- TATL, Temporary Admissible Transmission Loading, see https://arxiv.org/pdf/2112.06667 (temporarily higher line loading `delta_s_nom`, which has constraint energy over set period of time).

- example of dynamic line rating (`s_max_pu > 0`).

- example of approximation of N-1 (`s_max_pu = 0.7)`
