You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Set CARGO_TARGET_DIR per package to prevent collisions during parallel builds

## Problem

Fromager never sets `CARGO_TARGET_DIR` when building Rust packages (via maturin or setuptools-rust). Since maturin is a first-class build backend in fromager, Rust packages can be built without any special plugin configuration. However, during **parallel builds**, the `CARGO_TARGET_DIR` environment variable can leak between packages, causing cross-package collisions and build failures.

### How the leak happens

1. `external_commands.run()` starts with `os.environ.copy()` and merges `extra_environ` on top.
2. If a package plugin or user environment sets `CARGO_TARGET_DIR`, that value persists in the process environment.
3. When multiple Rust packages build in parallel, they can end up writing to the same target directory, causing corrupted artifacts or build failures.

Serial builds are less affected because each build completes before the next starts, but parallel builds hit this race condition.

### Current workaround

Downstream projects work around this by setting `CARGO_TARGET_DIR` per package in individual `update_extra_environ` plugin hooks. For example, the [fondue daft plugin](https://gitlab.com/redhat/rhel-ai/wheels/fondue/-/blob/main/builder/package_plugins/daft.py#L255-266) does:

```python
extra_environ["CARGO_TARGET_DIR"] = str(sdist_root_dir / "target")
```

This also solves a secondary issue: `daft-dashboard`'s `build.rs` uses `std::fs::rename` to move frontend assets into `OUT_DIR`, and keeping the cargo target dir on the same filesystem as the source tree avoids `EXDEV` (cross-device rename) failures.

Every Rust package plugin needs this same workaround, which is error-prone and shouldn't be left to individual plugins.

## Proposed fix

Fromager should automatically set `CARGO_TARGET_DIR` to `sdist_root_dir / "target"` for any package that uses a Rust build backend (maturin or setuptools-rust). This could be done in one of these locations:

1. **`wheels.py:build_wheel()`** — after `get_extra_environ()` returns, detect Rust packages using `vendor_rust._detect_rust_build_backend()` and set `CARGO_TARGET_DIR` in `extra_environ`.
2. **`packagesettings/_pbi.py:get_extra_environ()`** — alongside `MAKEFLAGS` / `CMAKE_BUILD_PARALLEL_LEVEL` / `MAX_JOBS`.
3. **`build_environment.py:run()`** — alongside the existing `CARGO_NET_OFFLINE` logic.

Using `setdefault` would allow per-package overrides via `env:` settings in the package YAML config to still take precedence.

This would:
- Isolate Rust build artifacts per package during parallel builds
- Prevent `CARGO_TARGET_DIR` leaking between packages
- Avoid cross-device rename (`EXDEV`) failures
- Eliminate the need for per-plugin workarounds
