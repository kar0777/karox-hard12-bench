You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

background_tasks.create fails in async tests that don't start the app

### First Check

- [x] I added a very descriptive title here.
- [x] This is not a security issue (those should be reported via the [security advisory](https://github.com/zauberzeug/nicegui/security/advisories/new) instead).
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [x] I used the GitHub search to find a similar [issue](https://github.com/zauberzeug/nicegui/issues) and came up empty.

### Example Code

```python
# conftest.py
pytest_plugins = ['nicegui.testing.user_plugin']
```

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
main_file =
```

```python
# test_background_tasks.py
import asyncio

from nicegui import background_tasks, ui
from nicegui.testing import User


async def test_with_the_app(user: User) -> None:
    @ui.page('/')
    def page():
        ui.label('Hello')

    await user.open('/')
    await user.should_see('Hello')


async def test_without_the_app() -> None:
    await background_tasks.create(asyncio.sleep(0))
```

### Description

1. Run `pytest test_background_tasks.py::test_without_the_app`: it fails with an `AssertionError` from `assert core.loop is not None` in `background_tasks.create`.
2. Run `pytest test_background_tasks.py`: now `test_without_the_app` fails with `RuntimeError: Event loop is closed`, because `core.loop` still holds the event loop of `test_with_the_app`, which pytest-asyncio closed when that test ended.

Expected: the task runs, as one created with `asyncio.create_task` does.

`background_tasks.create` creates every task on `core.loop`, the event loop NiceGUI notes when the app starts, so code that runs on another event loop cannot use it. We ran into this in an app whose data loader lets concurrent callers share one load. The pages call the loader, and so do async unit tests that load the data without starting the app, each on an event loop of its own. With `background_tasks.create` these tests fail as above. That is why the loader creates its task with `asyncio.get_running_loop().create_task()` and keeps the reference itself, although we would rather use `background_tasks.create` everywhere.

### NiceGUI Version

4.0.0

### Python Version

3.12.11

### Browser

Other (the problem shows in pytest, without a browser)

### Operating System

macOS

### Additional Context

`core.loop` is set once when the app starts (`nicegui.py`) and keeps that value after the app has stopped.

[※](https://zauberzeug.github.io/colophon/#m=claude-opus-5-5&t=Claude%20Code%20reproduced%20the%20problem%20and%20wrote%20this%20issue%3B%20Rodja%20decided%20to%20report%20it.&p=agent&d=2026-11-15&a=claude-code "claude-opus-5-5: Claude Code reproduced the problem and wrote this issue; Rodja decided to report it.")

