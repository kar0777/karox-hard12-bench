You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Nightly mutation sweep stopped short on main (tracking)

The nightly mutation sweep stopped short against `f6d45a7` (commit f6d45a787ba66912fe6604089d3e977cefd26031): a night that decided no mutant, a slice whose engine or lane failed, a slice whose budget ran out before its first mutant, or more than two slices with no record in one night.

**Run**: https://github.com/aallan/vera/actions/runs/41751614052

The stitch job's summary names what stopped it; each slice's record is its `mutation-sweep-slice-<n>` artifact.  Survivors never file this issue.  MUTATION.md § The measure-all baseline has the sweep's rules.
