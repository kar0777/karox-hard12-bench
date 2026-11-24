You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Save configured sdists with a standard filename

Some supported `source:` configurations fail to download source, or save it under a name that later commands cannot find. This prevents the package from building.

Examples:
- A `hook-sdist` resolver hook returns a tag archive URL ending in `/v1.0`. With no download hook, the download fails with `InvalidSdistFilename`.
- `pypi-download` with `download_kind: sdist` saves `pkg-v1.0.tar.gz`. Later, `find_sdist()` searches for `pkg-1.0.tar.gz` and finds nothing.

**Expected:** Save the archive using the package name and resolved version, preserving `.tar.gz` or `.zip`. Both cases should work without a custom download hook. Add regression tests for both cases.

Observed on `new-resolver-config` at `ff8d7683`. Related: #1414 — [review comment](https://github.com/python-wheel-build/fromager/pull/1414#discussion_r4443496023).

