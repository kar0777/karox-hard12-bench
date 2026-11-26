You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Windows: merged regression test test_unlinking_storage_files_waits_out_transient_holders fails with PermissionError (WinError 32)

*Filed by Claude Code on evnchn's behalf.*

### First Check

- [X] I added a very descriptive title here.
- [X] This is not a security issue (those should be reported via the [security advisory](https://github.com/zauberzeug/nicegui/security/advisories/new) instead).
- [X] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [X] I used the GitHub search to find a similar [issue](https://github.com/zauberzeug/nicegui/issues) and came up empty. (Closest are #6158 and #5949, both closed by #6159 — this is that fix's own regression test failing.)

### Example Code

```python
# tests/test_storage.py on main @ 9a088b2e — verbatim, no modification needed.
# Run on Windows:  pytest tests/test_storage.py -k unlinking_storage_files_waits_out_transient_holders

async def test_unlinking_storage_files_waits_out_transient_holders(user: User):
    @ui.page('/')
    def page():
        ui.label('ok')

    await user.open('/')  # needed to ensure NiceGUI's event loop is running
    filepath = Storage.path / 'storage-general.json'

    async def wait_until(condition: Callable[[], bool], *, timeout: float = 2.0) -> None:
        deadline = time.monotonic() + timeout
        while not condition() and time.monotonic() < deadline:
            await asyncio.sleep(0.01)

    async def write_and_hold_file() -> None:
        app.storage.general['key'] = 'value'  # schedules an async backup task
        await wait_until(filepath.exists)  # let the backup write the file
        assert filepath.exists()
        handle = filepath.open(encoding='utf-8')  # stands in for a backup write still holding the file
        threading.Timer(0.2, handle.close).start()

    await write_and_hold_file()
    app.storage.general.clear()  # schedules an async backup which deletes the now-empty file
    await wait_until(lambda: not filepath.exists())
    assert not filepath.exists()  # PASSES

    await write_and_hold_file()
    app.storage.clear()  # <-- FAILS HERE on Windows: PermissionError [WinError 32]
    assert not filepath.exists()
```

### Description

`test_unlinking_storage_files_waits_out_transient_holders` — the regression test merged with #6159 — **fails on Windows** on current `main`, with the same `PermissionError: [WinError 32]` it was written to prove fixed.

**Expected:** the test passes, as it does on Linux and macOS.
**Actual:** phase 1 (the async path, `app.storage.general.clear()`) passes; phase 2 (the sync path, `app.storage.clear()`) raises `PermissionError [WinError 32]` after the 1.0 s retry window expires.

**Reproduced 2/2 CI runs** on `windows-2022`, ~1.7 s, no browser involved. Ubuntu stays green because the race cannot occur on POSIX, and there is currently no Windows leg on CI — so this is invisible to the matrix today.

I have the failure reliably, but **not** a proven mechanism. Best hypothesis and the evidence against it are in Additional Context. Reporting rather than sending a PR, because the fix depends on which of two readings you take:

1. **Product** — `Storage.clear()` shouldn't depend on a loop it blocks. Options: drain/await pending backups before unlinking, offer an async `clear()` for callers already on the loop, or have the backup release its handle before the retry window.
2. **Test** — if sync `clear()` is intentionally best-effort against a loop-bound holder, phase 2 asserts more than the code promises and should be reshaped (and the `# used to raise PermissionError` comment then reads misleadingly).

Either way, worth noting the user-facing shape: `app.storage.clear()` is public and synchronous, and on Windows it can raise `PermissionError` when called from a running event loop with a backup in flight — the scenario #6158 and #5949 were about. If reading 2 is right, that limitation may deserve to be documented where users meet it, not only in a private helper's docstring.

Happy to send a PR in whichever direction you prefer — and happy to dig for the actual holder first if that's more useful.

### NiceGUI Version

`main` @ `9a088b2e` (`v3.14.0-26-g9a088b2e`)

### Python Version

3.10.20

### Browser

Other

*(No browser involved — this is a `user`-fixture test, in-process, no Selenium.)*

### Operating System

Windows

### Additional Context

<details><summary><b>Failure output (verbatim, from CI)</b></summary>

```
platform win32 -- Python 3.10.20, pytest-9.0.3, pluggy-1.6.0
collected 28 items / 26 deselected / 2 selected

tests/test_storage.py::test_awaiting_backup_scheduled_during_teardown PASSED  [ 50%]
tests/test_storage.py::test_unlinking_storage_files_waits_out_transient_holders FAILED [100%]

    await write_and_hold_file()
>   app.storage.clear()  # used to raise PermissionError (WinError 32) on Windows while the handle was open

tests\test_storage.py:452:
nicegui\storage.py:213: in clear
    helpers.unlink_with_retry(filepath, missing_ok=True)
nicegui\helpers\files.py:39: in unlink_with_retry
    while not _try_unlink(filepath, missing_ok=missing_ok, deadline=deadline):
nicegui\helpers\files.py:53: in _try_unlink
    filepath.unlink(missing_ok=missing_ok)

self = WindowsPath('C:/Users/runneradmin/AppData/Local/Temp/nicegui-test-storage-vprccsut/storage-general.json')
missing_ok = True

E   PermissionError: [WinError 32] The process cannot access the file because it is
    being used by another process:
    'C:\\Users\\runneradmin\\AppData\\Local\\Temp\\nicegui-test-storage-vprccsut\\storage-general.json'

================= 1 failed, 1 passed, 26 deselected in 1.63s ==================
```

Environment: `windows-2022`, Python 3.10.20, `uv sync --locked`, no reruns, no browser.

Two runs, identical apart from the tempdir name and 1.63 s vs 1.82 s. A third was cancelled by the workflow's `cancel-in-progress` concurrency group, not by a failure — so the sample is two, which is why I say "reproduced 2/2" rather than "deterministic".

</details>

<details><summary><b>What the evidence does and doesn't show</b></summary>

**What's established:** after 1.0 s of retrying, `filepath.unlink()` still raises `WinError 32`, so *something* held the file for the whole window.

**What isn't:** which holder. The obvious candidate — the explicit handle from `write_and_hold_file()` — is unlikely to be the one: it's closed by a `threading.Timer` on an independent thread, which shouldn't be blocked by the sleeping loop and fires at 0.2 s, comfortably inside the deadline.

**Best hypothesis:** a second, loop-bound holder — the `aiofiles` backup writer scheduled by `app.storage.general['key'] = 'value'`. `wait_until(filepath.exists)` only proves the file was *created*, not that the writer finished and closed it. If that coroutine is still open when phase 2 begins, sync `clear()` blocks the very loop it needs to resume, and the retry cannot succeed no matter how long the timeout.

That would be the case `nicegui/helpers/files.py` already documents, in the docstring added during #6159's review:

> Note: The blocking wait can only help if the holder releases the file independently of the current thread. A writer that needs this thread's event loop to close its file (e.g. an ``aiofiles`` coroutine suspended on the very loop that is calling this function) cannot proceed while we sleep and exhausts the timeout.

I can't confirm that from CI output alone — it would need a Windows box and a handle dump (or logging in the backup task) to nail down. Other explanations I can't fully exclude: the writer holding across a longer window than expected, or Windows-side scanning/indexing briefly retaining the file. I don't find those as likely, but I haven't ruled them out.

The earlier real-Windows red→green verification recorded in #6160 predates the two-phase consolidation of this test, so it doesn't cover this structure.

</details>

---

**Changelog**
- 2026-07-23: Restructured to follow the repository's issue template (First Check / Example Code / Description / versions / Additional Context). Content unchanged apart from adding the verbatim test source, the exact Python version, and the version string.

