You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[bug] Incorrect source hash is allowed if sources are cached

## Summary

An incorrect SHA is permitted for sources if that SHA already exists in the download cache, but does not necessarily correspond to the sources being requested.

## Expected Behaviour

An incorrect SHA should be detected regardless if the sources are cached or not.

## Actual Behaviour

No error is raised if an attempt is made to download sources with an incorrect hash, if that hash already exists in the download cache.

## Steps to Reproduce

1. Download the ZLib sources
    ```
    cd recipes/zlib/all
    conan source . --version=1.3.1
    ```

2. Add a new version of the package in `conandata.yml`. Use the same hash as 1.3.1 (or any other package in the download cache)
    ```yaml
    "1.3.2":
    url: "https://github.com/madler/zlib/releases/download/v1.3.2/zlib-1.3.2.tar.gz"
    sha256: "9a93b2b7dfdac77ceba5a558a580e74667dd6fede4585b91eefb60f03b72df23"
    ```

3. Download the new sources
     ```
    cd recipes/zlib/all
    conan source . --version=1.3.2
    ```

Note that this will also work using a hash from a different package, such as zstd - though the bug is more obvious in this case as you will have the zstd sources and not zlib.

## Workaround

Clean the download cache before calling `conan source`.

```
conan cache clean --backup-sources
```
    
## System Info

conan version 2.28.1
python 3.14.2
Arch Linux x86_64 

