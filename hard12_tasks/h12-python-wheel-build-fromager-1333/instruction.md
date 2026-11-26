You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Multi-version bootstrap silently drops versions with no sdist

In multi-version bootstrap mode, versions that match the specifier but have no sdist are silently filtered out during candidate resolution. No warning is logged, no entry is added to partial-failures.json, and no record exists that the version was ever considered.

## Reproduction

Package `drr` has versions 1.0.2 through 1.0.5 on PyPI. Version 1.0.4 has only a wheel (no sdist).

```
$ fromager list-versions "drr>=1.0.2" --distribution-type both
Found 4 version(s)
1.0.2
1.0.3
1.0.4
1.0.5

$ fromager list-versions "drr>=1.0.2" --distribution-type sdist
Found 3 version(s)
1.0.2
1.0.3
1.0.5
```

When bootstrapping with `--multi-version` and `drr>=1.0.2`, only 1.0.2, 1.0.3, and 1.0.5 are processed. 1.0.4 is never mentioned in logs or in partial-failures.json.

## Root cause

`PyPIProvider.validate_candidate()` in `resolver.py` ([lines 945-957](https://github.com/python-wheel-build/fromager/blob/main/src/fromager/resolver.py#L945-L957)) silently rejects candidates that don't match the desired distribution type. The debug log is gated behind `DEBUG_RESOLVER`, which is off by default.

## Expected behavior

In multi-version mode, when a version matching the specifier is dropped because it lacks an sdist, Fromager should either:
1. Log a warning (e.g., "drr==1.0.4: skipped, no sdist available on PyPI")
2. Record it in partial-failures.json with a clear reason
3. Ideally, both.

This matters for downstream observability -- operators need to know when a version exists but was not built, and why.

## Contrast with pinned versions

When pinned (`drr==1.0.4`), Fromager correctly errors out: "found no match for drr==1.0.4... searching for sdists." The gap is only in multi-version mode where other versions satisfy the requirement and the missing one is silently skipped.
