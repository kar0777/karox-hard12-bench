You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

default_build_sdist produces sdists rooted at build_dir's name instead of {name}-{version}

## Problem

The [sdist specification](https://packaging.python.org/en/latest/specifications/source-distribution-format/#source-distribution-file-format) requires that a source distribution contain exactly one top-level directory named `{name}-{version}`.

When a package sets `build_dir` in its package settings (the monorepo-subdirectory case), `default_build_sdist` produces a tarball rooted at the *build directory's* name instead. The filename is correct; only the directory inside is wrong.

For example, a package `mlserver-xgboost` whose sources live in `runtimes/xgboost/` yields `mlserver-xgboost-1.7.1.tar.gz` that unpacks into `xgboost/`.

## Cause

`default_build_sdist` tars from `build_dir` using the parent as the archive prefix:

https://github.com/python-wheel-build/fromager/blob/4eeb0f415c237578b2b970c516bbf2cee75b409f/src/fromager/sources.py#L549-L553

`tar_reproducible` then computes each entry as `arcname = os.path.relpath(fn, prefix)`:

https://github.com/python-wheel-build/fromager/blob/4eeb0f415c237578b2b970c516bbf2cee75b409f/src/fromager/tarballs.py#L58

So when `build_dir` is `<sdist_root_dir>/runtimes/xgboost`, `prefix` becomes `<sdist_root_dir>/runtimes` and every path is rooted at `xgboost/`. When `build_dir` is unset it equals `sdist_root_dir`, the prefix is its parent, and the root comes out correct — which is why this only affects packages that configure `build_dir`.

## Reproducer

No network or package settings required; it calls `default_build_sdist` directly.

```python
"""Reproducer: sdist top-level directory is build_dir's name, not {name}-{version}."""
import pathlib, tarfile, tempfile, types
from packaging.requirements import Requirement
from packaging.version import Version
from fromager import sources


def build(subdir: str | None) -> list[str]:
    tmp = pathlib.Path(tempfile.mkdtemp())
    sdist_root = tmp / "mypkg-1.0"
    build_dir = sdist_root / subdir if subdir else sdist_root
    build_dir.mkdir(parents=True)
    (build_dir / "setup.py").write_text("from setuptools import setup; setup()\n")
    out = tmp / "sdists-builds"
    out.mkdir()
    sdist = sources.default_build_sdist(
        types.SimpleNamespace(sdists_builds=out),  # ctx
        {},                                        # extra_environ
        Requirement("mypkg"),                      # req
        Version("1.0"),                            # version
        sdist_root,                                # sdist_root_dir
        None,                                      # build_env (unused here)
        build_dir,                                 # build_dir
    )
    with tarfile.open(sdist) as tar:
        return sorted({n.split("/")[0] for n in tar.getnames()})


print(f"build_dir unset (== sdist_root_dir) -> {build(None)}")
print(f"build_dir = 'python'               -> {build('python')}")
print(f"expected in both cases             -> ['mypkg-1.0']")
```

Run with `uv run --with-editable . python repro.py`:

```
build_dir unset (== sdist_root_dir) -> ['mypkg-1.0']
build_dir = 'python'               -> ['python']
expected in both cases             -> ['mypkg-1.0']
```

## Impact

Installers tolerate the layout — `pip` and `uv` build these sdists without complaint — so this does not break installs. It does affect anything that relies on the documented structure:

**Name collisions between unrelated projects.** The root directory is no longer unique per package, so distinct projects can produce sdists that unpack over each other. In one published index built with fromager, four unrelated projects (`ctranslate2`, `flatbuffers`, `tacozip`, `triton`) all emit sdists rooted at `python/`. Extracting two of them into the same directory silently loses one:

```
after flatbuffers-25.12.19.tar.gz: out/python/PKG-INFO says Name: flatbuffers
after ctranslate2-4.8.1.tar.gz:    out/python/PKG-INFO says Name: ctranslate2
what survived: python
```

No error is raised. Workflows that unpack a set of sdists into a common tree — source auditing, license scanning, vendoring, offline mirroring — drop packages here rather than failing loudly.

**Identity mismatch.** `PKG-INFO` inside the archive carries the correct `Name:` while the directory it sits in does not, so tools that infer the project from the directory name disagree with tools that read the metadata.

Same published index: 72 of 3,384 sdists have a top-level directory that is not `{name}-{version}`. Observed roots include `python/`, `xgboost/`, `sklearn/`, `lightgbm/`, `onnx/`, `core/`, `common/`, `tabular/`, `timeseries/`, `ogx_api/`.

This may also matter for #1311, which proposes unpacking the generated sdist and building the wheel from it — that pipeline would have to special-case a root directory that isn't `{name}-{version}`.

## Suggested fix

Root the archive entries at `{name}-{version}` regardless of where `build_dir` points, rather than deriving the prefix from `build_dir.parent`. `tar_reproducible` already takes the prefix as a parameter, so this could be an explicit arcname root rather than a path-relative computation.

