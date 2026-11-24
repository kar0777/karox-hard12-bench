You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] SuppressStdoutStderr in Prophet.fit() is not thread-safe and permanently redirects process FD 1/2 to /dev/null under concurrent execution

### Bug Description

`Prophet` enables `suppress_stdout_stderror=True` by default (`darts/models/forecasting/prophet_model.py`), which wraps `self.model.fit(fit_df)` in `execute_and_suppress_output(..., logger, logging.WARNING, ...)` -> `SuppressStdoutStderr()` (`darts/logging.py`). Because `prophet_model.py` sets `logger.level = logging.WARNING` at import time, `SuppressStdoutStderr` is always entered by default.

`SuppressStdoutStderr` redirects OS-level file descriptors `1` (`stdout`) and `2` (`stderr`) process-wide using `os.dup` and `os.dup2` without any thread synchronization or reference counting:

```python
class SuppressStdoutStderr:
    def __init__(self):
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        for fd in self.null_fds + self.save_fds:
            os.close(fd)
```

This causes three problems:

1. **Permanent loss of `stdout` / `stderr` in multi-threaded execution (`ThreadPoolExecutor`)**:
   - Thread A enters `SuppressStdoutStderr`: `save_fds_A` duplicates the real FD 1/2, and `__enter__` points FD 1/2 to `os.devnull`.
   - While Thread A is inside `fit()`, Thread B instantiates `SuppressStdoutStderr`: `os.dup(1)` duplicates **the current FD 1 (which is `os.devnull`)** into `save_fds_B`.
   - Thread A finishes first and restores the real `stdout`/`stderr` to FD 1/2.
   - Thread B finishes second and executes `os.dup2(self.save_fds[0], 1)`, **permanently overwriting process FD 1 and FD 2 with `os.devnull` for the remainder of the Python process lifetime**.
2. **Crash in non-console environments (e.g., Windows GUI / `pythonw.exe` / background services)**:
   - When FD 1 or FD 2 is not associated with a valid OS file descriptor, `os.dup(1)` raises `OSError: [Errno 9] Bad file descriptor`.
   - Additionally, because `os.open` and `os.dup` are called in `__init__` rather than `__enter__`, if the second `os.dup(2)` fails, the already-opened file descriptors in `self.null_fds` leak.
3. **Obsolescence with modern `prophet` (`cmdstanpy`)**:
   - `SuppressStdoutStderr` was originally needed when `fbprophet` used `pystan` (which wrote directly to C-level FD 1/2). Modern `prophet >= 1.1` uses `cmdstanpy`, which logs via standard Python `logging` (`logging.getLogger("cmdstanpy")` / `logging.getLogger("prophet")`).

---

### Minimal Reproducible Example

```python
import concurrent.futures
import time
from darts.logging import SuppressStdoutStderr


def worker(delay_enter: float, hold_time: float) -> None:
    time.sleep(delay_enter)
    with SuppressStdoutStderr():
        time.sleep(hold_time)


print("Before ThreadPoolExecutor (visible)")

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    # Thread 1 enters at t=0.0s and exits at t=0.10s
    f1 = executor.submit(worker, 0.0, 0.10)
    # Thread 2 enters at t=0.02s (while FD 1/2 point to devnull) and exits at t=0.20s
    f2 = executor.submit(worker, 0.02, 0.20)
    f1.result()
    f2.result()

# Everything printed after this point is permanently lost to /dev/null!
print("After ThreadPoolExecutor (PERMANENTLY SILENCED - NEVER PRINTED!)")
```

Running this script prints `"Before ThreadPoolExecutor (visible)"` and never prints `"After ThreadPoolExecutor..."` because FD 1 and FD 2 remain pointing to `os.devnull`.

---

### Expected Behavior / Suggested Fix

1. If `SuppressStdoutStderr` is kept in `darts/logging.py`, it should be protected by a module-level lock + reference counter (so `save_fds` is only captured when the outermost context enters `refcount == 0 -> 1` and restored when the last context exits `refcount == 1 -> 0`), and all FD operations should happen inside `__enter__` with graceful fallback if `os.dup` raises `OSError`.
2. Alternatively, for `Prophet`, output suppression can be achieved thread-safely via `cmdstanpy` / `prophet` logger levels (or passing `show_console=False` / `refresh=0` to CmdStanPy) without mutating process-wide OS file descriptors.

---

### Environment

- Darts version: `0.48.1`
- Python version: `3.12` / `3.13`
- OS: Windows / Linux / macOS (reproducible on all platforms)

