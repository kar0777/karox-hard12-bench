You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Use changelog deltas

When a PR has a merge conflict in most cases it is because of the CHANGELOG.md changes that GitHub is unable to merge because it doesn't follow the `merge=union` rule. This currently requires us to have the PR author fix the trivial merge conflict so the maintainer can merge the PR (if the maintainer fixed the conflict, they couldn't merge the PR even after they approved it because they made the last commit).

Isaac Lab is using a changelog deltas compilation script that works well for them, we should investigate something similar using a library such as [towncrier](https://pypi.org/project/towncrier/) or develop our own solution.
