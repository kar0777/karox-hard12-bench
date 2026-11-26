You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Commands in flattened subapps don't fully render in generated docs

The cyclopts [subcommand docs](https://cyclopts.readthedocs.io/en/latest/commands.html#flattening-subcommands) suggest using `app.command(sub_app, name="*")` to flatten a subapp into its parent command.

However `generate_docs` does not render the command help completely.

By contrast, using `app.update(sub_app)` (which is undocumented?) seems to achieve the same result, and _does_ render the flattened command properly.

For example:

```python
from cyclopts import App

app = App(name="app")

sub_app_update = App(name="update")
sub_app_star = App(name="star")


@sub_app_update.command()
def update(foo: int) -> None: ...


@sub_app_star.command()
def star(bar: int) -> None: ...


app.command(sub_app_star, name="*")
app.update(sub_app_update)


if __name__ == "__main__":
    print(app.generate_docs())
```

->

---

# app

```console
app COMMAND
```

## Table of Contents

- [`update`](#app-update)

**Commands**:

* [`star`](#app-star)
* [`update`](#app-update)

## app update

```console
app update FOO
```

**Parameters**:

* `FOO, --foo`: **[required]**

---

As you can see there is no documentation for `app star` other than the entry under `Commands`.

Also, are the two forms (otherwise) equivalent or am I missing something?
