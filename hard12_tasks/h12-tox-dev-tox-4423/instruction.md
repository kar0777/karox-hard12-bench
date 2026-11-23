You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

set_env: a line with an empty name, such as `=value`, is accepted and breaks commands on Windows

A `set_env` line that has nothing before the `=` is accepted as a variable with an empty name, both in a `set_env`
environment file and inline in `tox.ini`. tox does not complain while loading the config, and the empty name is passed
on to the command environment.

On Windows the command then fails with a confusing error that says nothing about the env file:

```
py312: commands[0]> python -c print(1)
py312: Exception running subprocess [WinError 87] The parameter is incorrect
py312: exit 22 ...
```

### Reproduce

`tox.ini`:

```ini
[tox]
no_package = true

[testenv]
set_env = file|e.env
commands = python -c "print(1)"
```

`e.env`:

```
A=1
=2
```

`tox config -e py -k set_env` shows an entry `=2` (a variable with an empty name), and `tox r -e py` fails on Windows
as shown above. The same happens inline, with `set_env =
    A=1
    =2` in `tox.ini`.

### Expected

The line is rejected the same way a line without `=` is: tox fails before running anything, e.g.
`invalid line 2 in .../e.env for set_env, expected KEY=VALUE` for the env file and `invalid line '=2' in set_env` inline.

### Version

tox main (4.67.14.dev13+gb62408452), Python 3.12, Windows 10.

