You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Guard against changelog entries being assigned to the wrong release

## Problem

An open PR can add a changelog entry under `## [Unreleased]` while another merge triggers a release. If the release moves the existing entries into a versioned section before the PR merges, Git can merge cleanly and place the PR entry under the next release section instead of `[Unreleased]`.

Example result:

```markdown
## [Unreleased]

## [v0.32.56] - 2026-10-25

- entry1
- entry2  # shipped after v0.32.55, but filed under v0.32.56
```

The race window is short but currently has no warning.

## Possible safeguards

- Add CI validation that changelog additions in a PR occur only inside the `[Unreleased]` section.
- Have release rotation compare the version-section body against entries introduced since the previous release tag (`<previous-tag>..HEAD`) and fail or warn when content is inconsistent.

The chosen approach should account for rebases, release-generated changelog changes, link updates, and merge commits.
