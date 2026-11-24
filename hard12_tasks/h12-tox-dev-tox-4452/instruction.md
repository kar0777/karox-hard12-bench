You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

TOML {[table]key} reference to a table whose name starts with env (e.g. [envvars]) is never resolved

### Issue

In a TOML configuration, a `{[table]key}` reference to a table whose name merely starts with `env` is treated as a
reference to a tox environment. The key is never read from the table, and the reference text stays in the value with
no warning.

`tox.toml`:

```toml
env_list = ["a"]

[extra]
ok = "from-extra"

[envvars]
ok = "from-envvars"

[env.a]
description = "{[extra]ok} | {[envvars]ok}"
```

```console
$ tox config -e a -k description
[testenv:a]
description = from-extra | {[envvars]ok}
```

Expected `from-extra | from-envvars`. The same happens in `pyproject.toml` for `[tool.tox.environment]`, and for an
`env_base` template (`{[tool.tox.env_base.tmpl]description}` or `{[env_base.tmpl]description}`).

The reference docs say `{[<table>]<key>}` reads from any table and substitutes only when the table is a tox
environment, so these tables should be read as plain tables.

### Cause

`TomlReplaceLoader._config_value_sources` in `src/tox/config/loader/toml/_replace.py` checks
`sec.startswith(env_prefix)` without the `.` separator, so `envvars` is looked up as the environment `ars` (the first
character after the prefix is dropped as the separator). That lookup raises `KeyError`, and the raw table is never
tried. `env_run_base` and `env_pkg_base` are excluded by name, which hides the problem for those two, but `env_base.*`
and any other `env*` table are not.

### Environment

- OS: macOS 26
- tox main (a6a824e8, 4.67.15), Python 3.14

