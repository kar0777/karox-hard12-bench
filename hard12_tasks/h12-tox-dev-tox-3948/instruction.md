You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Conflict between `constraints` and `constrain_package_deps` / `use_frozen_constraints` options

## Issue

(Posting this as an issue first because there are at least two potential outcomes, and I want to determine which one to pursue before I propose a PR)

We currently have three constraints-related options:

* The `constraints` option allows you to specify a `constraints.txt` file that is used when installing all package *except* the package under test.
* The `constrain_package_deps` option ensures packages specified in `deps` are not overridden by dependencies of the package.
* The `use_frozen_constraints` option ensures the exact version of packages installed during the `deps` phase are not overridden during the package phase.

These can conflict. Given the following setup:

**`pyproject.toml`**

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "foo"
version = "0.1.0"
dependencies = ["requests"]

[tool.hatch.build.targets.wheel]
include = ["foo.py"]
```

**`foo.py`**

```python
def main():
    pass
```

**`tox.ini`**

```ini
[tox]
envlist = py

[testenv]
constrain_package_deps = true
constraints = constraints.txt
deps =
    packaging
commands =
    python -c "import foo; print('ok')
```

**`constraints.txt`**

```
packaging==24.2
requests==2.31.0
```

If you run e.g. `tox -e py3`, you'll see a duplicate `-c` option in the `install_package_deps` phase:

```
❯ .venv/bin/tox -e py3 
py3: install_deps> python -I -m pip install packaging -c constraints.txt
.pkg: install_requires> python -I -m pip install hatchling
.pkg: _optional_hooks> python /tmp/tox-bug/.venv/lib/python3.14/site-packages/pyproject_api/_backend.py True hatchling.build
.pkg: get_requires_for_build_sdist> python /tmp/tox-bug/.venv/lib/python3.14/site-packages/pyproject_api/_backend.py True hatchling.build
.pkg: build_sdist> python /tmp/tox-bug/.venv/lib/python3.14/site-packages/pyproject_api/_backend.py True hatchling.build
py3: install_package_deps> python -I -m pip install requests -c constraints.txt -c/tmp/tox-bug/.tox/py3/constraints.txt
py3: install_package> python -I -m pip install --force-reinstall --no-deps /tmp/tox-bug/.tox/.tmp/package/1/foo-0.1.0.tar.gz
py3: commands[0]> python -c 'import foo; print('"'"'ok'"'"')'
ok
.pkg: _exit> python /tmp/tox-bug/.venv/lib/python3.14/site-packages/pyproject_api/_backend.py True hatchling.build
  py3: OK (3.24=setup[3.22]+cmd[0.02] seconds)
  congratulations :) (3.26 seconds)
```

I have also seen reports that this can also cause errors during this phase like so:

```
The conflict is caused by:
    The user requested oslo.context>=2.22.0
    The user requested (constraint) oslo-context===6.3.0,===6.4.0
```

But I've been unable to figure out how to trigger this yet. There is more detail in [this pastebin](https://paste.opendev.org/show/bCwEv5W8TeNaXKKvKg2K/) though.

With regard to fixes, I *think* the best suggestion is to forbid setting `constraints` at the same time as the `constrain_package_deps` / `use_frozen_constraints` or ignore the latter if the former is set (likely with a warning). The former already applies to both dependencies specified via `deps` and package dependencies, meaning the latter serves little to no purpose. The only case where I think you might want the two is if `deps` contained a constraint that was not present in your constraints file. If this were a likely case, then we'd probably need to merge the two constraints files. However, I suspect this is not common and we'd be better off waiting until someone requests it with a good reason why (YAGNI).

## Environment

n/a (this is a tox issue and is present on the latest version installed from pip)

## Output of running tox

n/a (per above)

</details>

## Minimal example

See example.
