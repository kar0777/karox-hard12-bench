You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Multiple version bootstrap crashes on RESOLVE-phase failures instead of continuing

## Summary

In multiple version bootstrap mode (`--multiple-versions`), if version resolution fails for a dependency (e.g. all candidates filtered by `--max-release-age` and cache server fallback also finds no match), the entire bootstrap crashes instead of recording the failure and continuing with remaining packages.

## Root Cause

In `Bootstrapper._handle_phase_error()` (`src/fromager/bootstrapper.py`), RESOLVE-phase errors always re-raise unless in test mode. The `self.multiple_versions` error handler (which records failures and continues) is only reachable for build-phase errors — not for RESOLVE failures:

```python
# Resolution failures: only recoverable in test mode
if item.phase == BootstrapPhase.RESOLVE:
    if self.test_mode:
        self._record_test_mode_failure(item.req, None, err, "resolution")
        return []
    raise  # <-- crashes in multiple_versions mode too
```

The `if self.multiple_versions` block further down is never reached for RESOLVE-phase errors because the `raise` fires first.

## How to Reproduce

1. Run multiple version bootstrap with `--max-release-age` against a collection where a dependency (e.g. `importlib-metadata`) has all candidates older than the age cutoff
2. Ensure the cache server does not have a version matching the requirement specifier

Example log:
```
INFO importlib-metadata: found 32 candidate(s) matching importlib-metadata<8.8.0,>=6.0
INFO importlib-metadata: have 0 candidate(s) published within 90 days
INFO importlib-metadata: all 32 candidate(s) are older than 90 days
INFO importlib-metadata: no results found with normal resolution, falling back to the cache server
WARNING importlib-metadata: error checking cache server: found no match for importlib-metadata<8.8.0,>=6.0
WARNING importlib-metadata: resolver returned no results (multiple version mode)
ERROR its-hub: Could not resolve any versions for importlib-metadata<8.8.0,>=6.0
```

The bootstrap crashes at the ERROR line instead of recording the failure and continuing to process other packages.

## Expected Behavior

Multiple version bootstrap mode should handle RESOLVE-phase failures the same way it handles build-phase failures: record the failure, log a warning, and continue processing remaining packages. A summary of all failed versions should be displayed at the end.
