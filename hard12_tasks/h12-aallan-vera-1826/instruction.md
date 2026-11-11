You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Nightly mutation sweep stopped short on main (tracking)

The nightly mutation sweep stopped short against `eab5d72` (commit eab5d7229f7157873fd29bfaeb1421e98f4b7a1c): a night that decided no mutant, a slice whose engine or lane failed, or slices with no record beyond what the sweep tolerates (one a night, three over seven nights).

**Run**: https://github.com/aallan/vera/actions/runs/41150541363

The stitch job's summary names what stopped it; each slice's record is its `mutation-sweep-slice-<n>` artifact.  Survivors never file this issue.  MUTATION.md § The measure-all baseline has the sweep's rules.
