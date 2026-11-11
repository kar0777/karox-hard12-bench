You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

An exception inside the `user` simulation makes all following tests error during setup

### Description

When a test using the `user` fixture logs an error, one failed test turns into errors in every test that follows it in the same process, as soon as the main file registers a startup handler:

```
RuntimeError: Unable to register another startup handler. NiceGUI has already been started.
```

The output then reads as if many tests were broken, and the actual failure is easy to miss among them.

### Example

`pytest.ini`:

```ini
[pytest]
asyncio_mode = auto
main_file = main.py
```

`main.py`:

```python
from nicegui import app, ui

app.on_startup(lambda: None)


@ui.page('/')
def index() -> None:
    def fail() -> None:
        raise RuntimeError('boom')

    ui.button('Fail', on_click=fail)
    ui.label('Hello')


ui.run()
```

`test_cascade.py`:

```python
from nicegui.testing import User

pytest_plugins = ['nicegui.testing.user_plugin']


async def test_logs_an_error(user: User) -> None:
    await user.open('/')
    user.find('Fail').click()
    await user.should_see('Hello')


async def test_unrelated(user: User) -> None:
    await user.open('/')
    await user.should_see('Hello')
```

On 3.19.0, `test_logs_an_error` errors at teardown as expected, but `test_unrelated` errors during setup as well.

### Cause

The `user` fixture calls `pytest.fail` while still inside `async with user_simulation(...)`. The exception leaves through `_lifespan`, which has no `finally`:

```python
@asynccontextmanager
async def _lifespan(_: App):
    await _startup()
    yield
    await _shutdown()
```

So `_shutdown()` never runs, `app.is_started` stays `True`, and the next `app.on_startup` raises. From reading the code, any other exception leaving a `user_simulation` block should end the same way. `_lifespan` looks the same on `main` and on `4.0`.

### Suggested fix

Run `_shutdown()` in a `finally` block in `_lifespan`. With that replaced at runtime on 3.19.0, the example above reports only the error of `test_logs_an_error`, and `test_unrelated` passes. This also covers direct uses of `user_simulation`, which moving the log check behind the simulation in the fixture would not.

The open question is what it means outside of tests: `_shutdown()` would now also run when an exception is thrown into the lifespan context of a real server. That has not been tested yet.

Planned for 4.1, after the 4.0 release.

[※](https://zauberzeug.github.io/colophon/#m=claude-opus-5-5&t=Finding%2C%20reproduction%20and%20wording%20from%20the%20model%3B%20the%20author%20decided%20to%20report%20it%20and%20to%20fix%20it%20in%204.1.&d=2026-11-04&a=claude-code "claude-opus-5-5: Finding, reproduction and wording from the model; the author decided to report it and to fix it in 4.1.")

