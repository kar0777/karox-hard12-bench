You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Multiple version bootstrap should not silently skip packages when all candidates are older than max-release-age

## Problem

When `--multiple-versions` is combined with `--max-release-age`, if all candidates for a package are older than the configured age window, the resolver returns an empty set and the package is silently dropped from the build.

This is problematic in two distinct scenarios:

### 1. Unconstrained package where all releases are older than the timeframe

A package like `cmarkgfm` may not have had a release in the last 30 days. In multi-version mode with `--max-release-age=30`:

- `find_all_matching_from_provider()` is called with `fallback_on_empty_age_filter=False`
- All candidates are filtered out by the age check
- The resolver returns an empty list
- The package is silently skipped from the build

**Expected behavior**: When age filtering removes all candidates for an unconstrained package, fromager should fall back to building the latest matching version from source rather than returning an empty set.

### 2. Constrained/pinned package where the pinned version is older than the timeframe

A package pinned in constraints (e.g., `boto3==1.35.88`) where that specific version was published more than 30 days ago:

- The constraint restricts candidates to exactly one version
- Age filtering removes it (too old)
- The resolver returns an empty list
- The pinned version is silently skipped from the build

**Expected behavior**: When a package is explicitly pinned via constraints, the pinned version should always be built regardless of its age. A constraint pin is an explicit user intent that should take precedence over the age filter.

## Relevant code

- `bootstrap_requirement_resolver.py:162`: `fallback_on_empty_age_filter=not self.multiple_versions` — multi-version mode opts out of the fallback, causing the empty set return
- `resolver.py:332-340`: When `fallback_on_empty_age_filter=False` and all candidates are older than the cutoff, `candidates_list` is set to `[]`
- `bootstrap_requirement_resolver.py:165-171`: Cache server fallback exists but only triggers when a cache server URL is configured, and even then returns at most one version

## Suggested behavior

| Scenario | Current behavior | Proposed behavior |
|---|---|---|
| Unconstrained, all releases older than max-age | Returns empty set, package silently skipped | Build the latest version from source |
| Constrained/pinned, pinned version older than max-age | Returns empty set, package silently skipped | Always build the pinned version — constraint pin should override age filter |
