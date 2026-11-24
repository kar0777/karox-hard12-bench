You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Make Engine.is_series_like a real type guard

## Problem

`graphistry/Engine.py::is_series_like` is the typed helper the docs and the `dynamic-attr` hygiene check point people to, but it is implemented as `hasattr(s, "dropna") or is_polars_series(s)` and returns a plain `bool`. So:

- mypy gets no narrowing from it; call sites still need ignores or stay untyped.
- It is true for anything with `.dropna`, including a DataFrame.
- The duck-typed probe is centralised, not removed.

## Expected

- `is_series_like` returns a `TypeGuard` for the engine Series union and decides by type (pandas `isinstance`, the existing cuDF and Polars guards), not by attribute probing.
- Every existing caller is checked: any that relies on a DataFrame or another non-Series passing gets its own explicit check.
- No behaviour change on pandas, cuDF, Polars and polars-gpu test lanes; mypy count does not rise.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01WBbrdr4aMMzda6y3NQuwmr
