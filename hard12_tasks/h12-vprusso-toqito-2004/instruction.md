You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Functions in channel_props can be shadowed by their submodules ("'module' object is not callable")

## Before reporting this bug:
- [x] Verify there is not an existing issue for it already
- [x] You are using the latest version of `toqito` with a Python version `>=3.12`

## Describe the bug
`toqito.channel_props` loads its functions lazily through a module-level `__getattr__`. Each function lives in a submodule with the same name (`channel_props/channel_dim.py` defines `channel_dim`, and so on).

When any code imports one of those submodules directly, for example `from toqito.channel_props.channel_dim import channel_dim` (which `choi_to_kraus`, `kraus_to_choi`, `dual_channel`, `channel_distinguishability` and others do), Python sets the submodule as an attribute of the package. After that, `__getattr__` is never called for that name, so `from toqito.channel_props import channel_dim` gives the module instead of the function.

Whether it breaks depends on import order. After importing every module in `toqito`, 8 of the 12 names in `channel_props.__all__` resolve to modules: `channel_dim`, `choi_rank`, `is_channel_antidistinguishable`, `is_extremal`, `is_positive`, `is_unital`, `is_unitary`, `is_unitary_antidistinguishable`.

## To Reproduce
```python
from toqito.channel_ops import choi_to_kraus  # imports toqito.channel_props.channel_dim
from toqito.channel_props import channel_dim

print(type(channel_dim))  # <class 'module'>
channel_dim([[1, 0], [0, 1]])  # TypeError: 'module' object is not callable
```

Without the first line, `channel_dim` is the function as expected.

## Expected behavior
`from toqito.channel_props import <name>` should always give the function, whatever was imported before.

Going back to eager imports in `__init__.py` is not an option, because that reintroduces circular imports (`matrix_props.sk_norm`, `channel_opt.channel_distinguishability`). A small fix that keeps the lazy loading is to give the package module a `__setattr__` that, when Python sets one of the `__all__` submodules on the package, stores the function from that submodule instead.

## System Information where `toqito` is installed
toqito master (c3fdb0f), Python 3.13

I have a fix with a regression test ready and will open a PR. (I used Claude to help find and fix this.)

