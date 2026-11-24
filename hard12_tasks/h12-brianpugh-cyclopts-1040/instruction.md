You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Since 5.0, an unknown combined short flag is blamed on a meta-app option

Since 5.0.0, a mistyped hyphen-leading token in a subcommand is reported as an error about a meta-app option instead of as an unknown option. The command is still rejected, but the message names the wrong parameter.

The setup: a meta app with `*tokens` (`allow_leading_hyphen=True`) plus a `-o/--output` option, forwarding `tokens` to the app. When a combined short-flag token such as `-xo` contains a letter the meta app owns (`o`), that letter is bound to the meta option and the meta parser fails first, so the subcommand's unknown-option error for `-x` is never raised.

This looks related to the merged combined-short scan in 5.0 (`_merged_combined_short_scan` in `bind.py`), and to #932 for the 4.x behavior that 4.25.1 fixed.

### Reproduction

```python
from importlib.metadata import version
from typing import Annotated

from cyclopts import App, Parameter

app = App(result_action="return_value")


@app.command
def get(name: str = "x") -> None:
    print("ran get", name)


@app.meta.default
def launch(
    *tokens: Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    output: Annotated[str, Parameter(name=("--output", "-o"))] = "text",
) -> None:
    app(tokens)


print("cyclopts", version("cyclopts"))
for argv in (["get", "-xo"], ["get", "-foo", "--output", "json"], ["get", "--flwo"]):
    try:
        app.meta(argv, exit_on_error=False, print_error=False)
    except Exception as exc:  # noqa: BLE001
        print(argv, "->", type(exc).__name__ + ":", exc)
```

Run with `uv run --with cyclopts==4.25.3 repro.py` and `uv run --with cyclopts==5.3.0 repro.py`:

```
cyclopts 4.25.3
['get', '-xo'] -> UnknownOptionError: Unknown option: -xo. -x is not a recognized option.
['get', '-foo', '--output', 'json'] -> UnknownOptionError: Unknown option: -foo. -f is not a recognized option.
['get', '--flwo'] -> UnknownOptionError: Unknown option: --flwo.
cyclopts 5.3.0
['get', '-xo'] -> MissingArgumentError: Parameter -o requires an argument.
['get', '-foo', '--output', 'json'] -> RepeatArgumentError: Parameter --output specified multiple times.
['get', '--flwo'] -> UnknownOptionError: Unknown option: --flwo.
```

5.0.0 behaves like 5.3.0. Long options (`--flwo`) are unaffected.

### Expected

The 4.25.x behavior: `UnknownOptionError` naming the token the user mistyped (`-xo`, `-foo`), since neither is a valid combination of known short flags.

