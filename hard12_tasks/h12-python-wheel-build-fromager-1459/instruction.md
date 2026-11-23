You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

list-overrides: use the package-level `source:` for variants without one

## Problem

`list-overrides --details` decides whether a variant is prebuilt from the variant's own `source:`, or else from its `pre_built` flag ([list_overrides.py#L77-L84](https://github.com/python-wheel-build/fromager/blob/ccd98cc73fc580a5b806b84990dae92565fe8ce4/src/fromager/commands/list_overrides.py#L77-L84)). It ignores a package-level `source:`.

With this settings file, the `cpu` variant shows `yes` although its effective provider downloads prebuilt wheels:

```yaml
source:
  provider: pypi-prebuilt
variants:
  cpu:
    env:
      FOO: "1"
```

## Fix

Use the variant's `source:` if it has one, otherwise the package's `source:`, and read `resolves_prebuilt_wheel` from that. Fall back to `pre_built` only when neither has a `source:`. Add a test for this case.

Display only. Non-blocking for #1414. Reported by CodeRabbit on #1414.

