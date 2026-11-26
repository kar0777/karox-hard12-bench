You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] recipe export is slow with multiple patterns on repo with many files

### Describe the bug

OS: Ubuntu 2404 in WSL2 under Windows 11
Recipe contains ~30 patterns in exports_sources, repo contains ~2000 files including repository history (.git/*)
`conan export .` runs on Ubuntu and works with source folder shared with Windows host
The completion time is more than 5 minutes for such simple operation

The problem lies in the implementation of _export_source() function from `conan/internal/api/export.py`. It calls copy() from `conan/tools/files/copy_pattern.py` for each (non-exclusion) pattern in export_sources.
Although this is relatively cheap operation on host itself (Mac, Windows), it may not be cheap when VM shares filesystem with host. In my case each scan takes about 11 seconds.

My proposal is to rewrite copy() and _filter_files() functions to accept list in `pattern` parameter, similar to `excludes`. This will decrease number of iterations over filesystem to a single one.

### How to reproduce it

_No response_
