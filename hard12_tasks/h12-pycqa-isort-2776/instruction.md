You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

An aliased import with an opening-line comment goes past line_length, and isort and black keep rewrapping it

With `--profile black`, isort and black never agree on an aliased import that only fits on one line without its `# noqa` comment. On main (1060ab4) and on 9.0.2, with black 26.10.1:

```console
$ cat example.py
from some.package.with_a_rather_long_module_name import (
    SomeLongClassName as alias,  # noqa: N813
)
$ isort --profile black example.py
Fixing /tmp/demo/example.py
$ cat example.py
from some.package.with_a_rather_long_module_name import (  # noqa: N813
    SomeLongClassName as alias,
)
$ isort --profile black example.py
Fixing /tmp/demo/example.py
$ cat example.py
from some.package.with_a_rather_long_module_name import SomeLongClassName as alias  # noqa: N813
$ black -q example.py
$ cat example.py
from some.package.with_a_rather_long_module_name import (
    SomeLongClassName as alias,
)  # noqa: N813
$ isort --profile black example.py
Fixing /tmp/demo/example.py
$ cat example.py
from some.package.with_a_rather_long_module_name import SomeLongClassName as alias  # noqa: N813
```

The second isort run writes a 96-character line, past the profile's line length of 88. From then on black wraps it and isort joins it back on every run, so with both tools in pre-commit the file is modified every time. 10.0.0b1 does the same, while 8.0.1 keeps the wrapped form from the first run on. It happens in real code too: on matplotlib's [backend_wxcairo.py](https://github.com/matplotlib/matplotlib/blob/e2256af2e75b4342ea943efe193e4dac3e3b5a67/lib/matplotlib/backends/backend_wxcairo.py#L5-L6), `isort --profile black` writes `from .backend_wx import NavigationToolbar2Wx as NavigationToolbar2WxCairo  # noqa: F401 # pylint: disable=W0611`, which is 111 characters long. Other opening-line comments also end up past `line_length`, although black leaves the joined line alone when the comment is a `# type: ignore`.

`_build_as_imports` wraps the import without the opening-line comment and adds the comment to the first line afterwards ([output.py#L373-L391](https://github.com/PyCQA/isort/blob/1060ab47708b7a7c907f30e1be56bf6b2647bd0e/isort/output.py#L373-L391)), so an import that fits on its own ends up past `line_length` once the comment is added. This came with 5349578a in #2491, which dropped the branch that wrapped this single-line case again with the comment included. A plain import in the same situation stays wrapped with the comment on the `(` line.

I have a fix with a regression test and will open a pull request for it.
