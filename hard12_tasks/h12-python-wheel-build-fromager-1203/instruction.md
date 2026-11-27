You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

bug: multiple_versions mode retries already-failed versions on every new resolution

## Summary

In `--multiple-versions` mode, when a build-system dependency (e.g. `setuptools>=40.8.0`) fails to build across many versions, the entire version walk-down is repeated from scratch each time another package triggers resolution of the same requirement. Failed versions are recorded in `_failed_versions` and removed from `_seen_requirements`, but the resolution cache still returns the full candidate list and `_has_been_seen()` no longer blocks re-entry, so every candidate is re-downloaded, re-prepared, and re-built — only to fail again with the same error.

## Observed behavior

Running `fromager --multiple-versions bootstrap` on a multi-package build, setuptools (required as a build-system dependency via `setuptools>=40.8.0`) is resolved and walked down repeatedly. In a multi-day run (92+ hours), we observed repeated complete walk-downs of the same failing versions:

- **159 build failures** in a single log window, all with the same error (`pkgutil.ImpImporter` removed in Python 3.12)
- **73 versions** attempted and failed **at least twice**
- **~56 minutes** wasted on redundant builds in one log window alone
- Every attempt re-downloaded the sdist, re-extracted it, re-created a build environment, and re-ran `get_requires_for_build_wheel` before failing identically

The work directory contained **275 setuptools version directories**, confirming extensive repeated extraction across the full run.

## Expected behavior

Once a version fails to build, it should not be retried when the same requirement is resolved again for a different parent package.

## Root cause

The bug is in the interaction between three mechanisms:

### 1. Resolution cache returns the full candidate list (including already-failed versions)

`BootstrapRequirementResolver._resolved_requirements` caches the full list of `(url, version)` tuples returned by PyPI resolution. When the same requirement is resolved a second time, the cache returns the same full list of candidates — it has no knowledge of which versions already failed.

### 2. Failed versions are removed from `_seen_requirements`

When a version fails in `multiple_versions` mode, `_handle_phase_error()` discards it from `_seen_requirements` (`bootstrapper.py:1815-1820`). This means the `_has_been_seen()` guard in `_phase_start()` no longer blocks re-entry for failed versions.

### 3. `_failed_versions` is only used for end-of-run reporting

The `_failed_versions` list records failure tuples but is only consulted for logging at the end of `bootstrap()`. It is never checked before attempting a build.

### The cycle

1. Package A needs `setuptools>=40.8.0` → resolves all matching versions → each version fails
2. `_handle_phase_error()` records failure in `_failed_versions` and **discards from `_seen_requirements`**
3. Package B also needs `setuptools>=40.8.0` → cache hit → same full list returned
4. `_has_been_seen()` returns `False` (was discarded in step 2) → every version is retried → fails again
5. Repeat for every subsequent package needing the same dependency

## Potential fix

Filter out already-failed versions in `_phase_resolve()` before expanding them into work items:

```python
# In _phase_resolve(), after getting resolved_versions:
if self.multiple_versions:
    failed_set = {(name, ver) for name, ver, _ in self._failed_versions}
    pkg_name = canonicalize_name(item.req.name)
    resolved_versions = [
        (url, ver) for url, ver in resolved_versions
        if (pkg_name, str(ver)) not in failed_set
    ]
```

This is a minimal, localized change that doesn't alter the semantics of `_seen_requirements` or the resolver cache.

## Reproduction

```bash
fromager \
  --work-dir /src/work-dir \
  --sdists-repo /src/sdists-repo \
  --wheels-repo /src/wheels-repo \
  --multiple-versions \
  bootstrap 'requests==2.34.2'
```

Any package whose dependency tree triggers `setuptools>=40.8.0` resolution multiple times on Python 3.12 will exhibit this behavior.

## Environment

- fromager 0.87.0
- CPython 3.12.12
- `--multiple-versions` mode
- manylinux_2_28 container (UBI8)
