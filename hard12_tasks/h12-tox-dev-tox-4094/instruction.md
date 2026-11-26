You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

set_env as a list of tables drops every file entry but the last, and ignores the order

`docs/reference/config.rst`, in "References within set_env", documents the list-of-tables form as the way to inherit `set_env` from another environment:

> When you want to inherit `set_env` from another environment you can use the feature that if you pass a list of dictionaries to `set_env` they will be merged together. […] Here the `magic` tox environment will have both `A`, `B`, `C` and `D` environments set.

The entries are flattened into a single dict before being parsed (`src/tox/config/set_env.py:49`):

```python
if isinstance(raw, list):
    self._parse_dict({key: value for entry in raw for key, value in entry.items()})
```

A dict cannot hold the same key twice, and `file` is exactly the key that legitimately repeats, so only the last `file` entry survives. That breaks the documented inheritance pattern itself.

## Reproduction

`base.env` contains `BASE=1`, `extra.env` contains `EXTRA=2`:

```toml
[env_run_base]
package = "skip"
set_env = {file = "base.env", KEEP = "yes"}

[env.magic]
set_env = [
    {replace = "ref", of = ["env_run_base", "set_env"]},
    {file = "extra.env"},
]
```

```
$ tox c -e magic -k set_env
[testenv:magic]
set_env =
  EXTRA=2
  KEEP=yes
  ...
```

`KEEP=yes` is inherited but `BASE=1` is gone, with no warning: the `file = "base.env"` that arrived through `replace = "ref"` was overwritten by the local `file = "extra.env"` during the flattening.

Minimal form, with the INI sibling for comparison:

```
TOML  set_env = [{file = "a.env"}, {file = "b.env"}]   ->  B=2         (A=1 lost)
INI   set_env = \n file|a.env \n file|b.env            ->  A=1  B=2    (correct)
```

## Second symptom, same cause: the order of the entries is ignored

`f.env` contains `FOO=fromfile`:

```
INI    FOO=1 / file|f.env / FOO=2              ->  FOO=2          (the later explicit value wins)
TOML   [{FOO="1"}, {file="f.env"}, {FOO="2"}]  ->  FOO=fromfile   (wrong)
```

A dict keeps a repeated key at the position of its *first* occurrence with the value of the *last*, so `FOO` is pulled back to before the `file` entry and becomes overridable by the file. That contradicts the rule this project already fixed and pinned for INI in `tests/config/test_set_env.py::test_set_env_file_does_not_override_later_values` (#3740).

Both symptoms happen in `tox.toml` and in `pyproject.toml` under `[tool.tox]`.

Notably, the list form exists *because* TOML cannot hold a duplicate key inside one table, so flattening it back into a table undoes the only reason for the form to exist. The existing tests for the list form use distinct keys, so neither symptom was covered.

I have a fix ready (stream the entries in order instead of merging them into a dict first; `_parse_dict` already processes pairs in order and already resets `keys_after_file` at each `file` entry) plus two tests, and will open a PR against this issue.

