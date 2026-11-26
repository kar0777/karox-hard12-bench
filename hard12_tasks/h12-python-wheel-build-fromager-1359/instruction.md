You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

_is_wheel_built() raises fatal ValueError for pre-built packages with build tags after #1273

After #1273, `_is_wheel_built()` crashes with a `ValueError` when a candidate wheel on a package index carries a build tag but the local configuration expects none.

```
ValueError: torch: changelog for version 2.11.0 is inconsistent.
Found build tag (2, '') but expected (0, '')
```

Pre-built packages return an empty build tag from `PackageBuildInfo.build_tag()` ([`_pbi.py:298-300`](https://github.com/python-wheel-build/fromager/blob/1d07f3088f7c365ecbc0bec229c3beb7086ebcf0/src/fromager/packagesettings/_pbi.py#L298-L300)) because we assume pre-built wheels come from PyPI and do not have a fromager build tag. When a separate package index (configured via `wheel_server_url`) hosts a wheel with a build tag > 0, the consistency check at [`build.py:548-554`](https://github.com/python-wheel-build/fromager/blob/1e3c39d7/src/fromager/commands/build.py#L548-L554) raises.

This check existed before #1273 but was inside the broad `try/except Exception` block that caught it and treated it as a cache miss (`return None`). The refactoring in #1273 moved the candidate iteration loop outside that exception handler, making the previously-swallowed `ValueError` fatal.

## How to reproduce

1. Configure a package as `pre_built` with a `wheel_server_url` pointing to a package index (e.g. torch with a GitLab PyPI registry)
2. Ensure that index has a wheel with a build tag > 0 (e.g. `torch-2.11.0-2-cp312-cp312-linux_aarch64.whl`)
3. Run a build that looks up that package:
   ```
   fromager build torch==2.11.0
   ```
4. The build fails with:
   ```
   ValueError: torch: changelog for version 2.11.0 is inconsistent. Found build tag (2, '') but expected (0, '')
   ```

**Expected behavior:** The build tag mismatch should be treated as a cache miss (log and skip the candidate), matching the pre-#1273 behavior.
