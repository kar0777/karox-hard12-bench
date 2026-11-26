You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Accept mempalace.yml as project config filename

**What problem does this solve?**

`load_config()` in `mempalace/miner.py` only looks for `mempalace.yaml`, then falls back to the legacy `mempal.yaml`. A project config named `mempalace.yml` is silently ignored, and the mine runs with auto-detected defaults: wing from directory name, single `general` room, and no `exclude_patterns`. Excluded files get mined without any visible error, the only hint being the "No mempalace.yaml found" line on stderr, which is easy to miss.

This is also inconsistent within the codebase: `SKIP_FILENAMES` already lists `mempalace.yml` and `mempal.yml` alongside the `.yaml` variants, which suggests they were meant to be recognized config filenames. `room_detector_local.py` and `_MEMPALACE_PROJECT_FILES` in `cli/__init__.py` also only reference `mempalace.yaml`.

Many projects standardize on `.yml` (GitHub Actions, docker-compose, linters), so it's a natural filename to try.

**What's the proposed solution?**

Resolve the project config in this order: `mempalace.yaml`, `mempalace.yml`, `mempal.yaml`, `mempal.yml`. Ideally a single shared helper used by `miner.load_config()`, `room_detector_local`, and the CLI project-file detection, so the lists can't drift apart again.

Optionally, warn if more than one of these files exists in the same directory.

**Alternatives considered:**

- Keep `.yaml` only, but will fail or warn when a `mempalace.yml` is present and ignored. That would at least remove the silent fallback.
