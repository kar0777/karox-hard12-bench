You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`logger.exception()` from `haystack.logging.getLogger` does not log the traceback

**Describe the bug**

`haystack.logging.getLogger` wraps `logger.exception` with `patch_log_method_to_kwargs_only`, which always forwards `exc_info=None`:

```python
# haystack/logging.py
def _log_only_with_kwargs(msg, *, _=None, exc_info=None, stack_info=False, stacklevel=1, **kwargs):
    ...
    return func(msg, exc_info=exc_info, ...)

logger.exception = patch_log_method_to_kwargs_only(logger.exception)  # in getLogger()
```

Stdlib `Logger.exception` defaults to `exc_info=True`, but only when the argument is omitted. The explicit `None` leaves `LogRecord.exc_info` empty, so every `logger.exception(...)` logs an ERROR line without a traceback, in JSON and console output alike, since the record carries no `exc_info` for handlers or structlog to render. Passing `exc_info=True` explicitly restores it.

Because `getLogger` patches the stdlib logger object in place, a plain `logging.getLogger(name).exception(...)` is affected too once `name` has gone through `haystack.logging.getLogger` (e.g. any imported Haystack module's `__name__`).

On Python 3.10 the caller line is also wrong. Stdlib `exception` calls the patched `error`, so the call passes two wrappers that each add 1 to `stacklevel`, and 3.10's `findCaller` counts every frame (3.11+ skips `logging` internals). Records then point at `haystack/logging.py:163`. This hits plain `logging.Logger` instances, including Haystack's module loggers created during `import haystack` (e.g. `breakpoint.py`, `type_serialization.py`). `fatal`/`warn` have the same 3.10 issue (unused in Haystack). Moot once #13065 drops 3.10.

The wrapper dates from #7207, which does not discuss `exception()`. The `PatchedLogger` protocol also declares `exception(..., exc_info: Any = None)`.

No test checks the traceback on a patched logger. `TestCompositeLogger` calls `exception()` only outside `except` blocks, and `test_logging_exceptions`/`test_logging_exceptions_json` use a stdlib logger. The JSON test passes only because it runs before `TestCompositeLogger` patches the same name (`haystack.test_logging`); run after one, it fails:

```
hatch run test:unit "test/test_logging.py::TestCompositeLogger::test_various_levels[debug-debug]" \
                    "test/test_logging.py::TestStructuredLoggingJSONRendering::test_logging_exceptions_json"
# E   Right contains 1 more item: {'exception': [...]}   (condensed)
# 1 failed, 1 passed
```

Affected Haystack call sites (13 calls in 8 files, all in `except` blocks): `core/pipeline/breakpoint.py`, `utils/type_serialization.py`, `components/embedders/openai_document_embedder.py`, `components/query/query_expander.py`, `components/extractors/llm_metadata_extractor.py`, `components/extractors/image/llm_document_content_extractor.py`, `components/preprocessors/csv_document_cleaner.py` and `csv_document_splitter.py`.

Most messages interpolate the error text, so the stack trace is what is lost. It matters most where the error is swallowed: always in the CSV components and the query expander, with `raise_on_failure=False` (the default) in the embedder and extractors, and in `breakpoint.py` when a snapshot is saved after a non-`BreakpointException` error. `type_serialization.py` re-raises `from error`, so its traceback survives. Integrations using `haystack.logging.getLogger` are affected the same way.

**Error message**

None; the traceback is silently missing.

**Expected behavior**

`logger.exception(...)` logs the active traceback (stdlib default `exc_info=True`) and the caller's line. Explicit `exc_info` keeps working.

**Additional context**

Proposed fix (no API change):

- Delete `logger.exception = patch_log_method_to_kwargs_only(logger.exception)` in `getLogger`. Stdlib `Logger.exception` then calls the already patched `error` with `exc_info=True`: the traceback is attached, positional args are still rejected (the `TypeError` names `Logger.error()`), and with one wrapper frame the 3.10 line is right for the default `stacklevel`. This relies on CPython's `Logger.exception` delegating to `self.error` (same on 3.10 and 3.14). `fatal`/`warn` could be unwrapped likewise.
- Change `PatchedLogger.exception` to `exc_info: Any = True`.
- Add regression tests with `haystack.logging.getLogger`: JSON `exception` entry, console traceback, `exc_info=False` respected, other levels unchanged.

Alternative: a keyword-only `default_exc_info` on the wrapper, `True` for `exception`. It restores the traceback but keeps the 3.10 line bug.

Either way, outside an `except` block `exc_info=True` resolves to `(None, None, None)` as in the stdlib, so `TestCompositeLogger::test_various_levels[exception-error]` stays green.

Side effects of tracebacks appearing:

- JSON `exception[].exc_value` is not truncated to `MAX_LOG_VALUE_LENGTH` (`bound_event_dict_values` skips `exc_info`, #12849), as is already the case for stdlib loggers.
- Console mode (`ConsoleRenderer()` with `rich`) shows local variables in tracebacks; the JSON renderer disables them as sensitive.

I am happy to open a PR.

**To Reproduce**

Needs `structlog` for the output below (without it the stdlib output lacks the traceback too). The logger must be under the `haystack` namespace, where `configure_logging` attaches its handler.

```python
from haystack import logging

logger = logging.getLogger("haystack.demo")

try:
    raise ValueError("boom")
except ValueError:
    logger.exception("Something failed")
```

Actual, Python 3.14, non-TTY (JSON by default; same with `configure_logging(use_json=True)`):

```
{"event": "Something failed", "level": "error", "timestamp": "...", "lineno": 8, "module": "haystack.demo"}
```

Python 3.10 reports `"lineno": 163` (unless `configure_logging()` runs before `getLogger`). Console output (`HAYSTACK_LOGGING_USE_JSON=false`) has no traceback either.

Expected: an `exception` entry (JSON) or a rendered traceback (console), and `"lineno": 8`.

A stdlib logger whose name never went through `haystack.logging.getLogger` gets the traceback under the same config:

```python
import logging as std_logging
from haystack import logging

logging.configure_logging(use_json=True)
try:
    raise ValueError("boom")
except ValueError:
    std_logging.getLogger("haystack.stdlib").exception("Something failed")
# {"event": "Something failed", ..., "exception": [{"exc_type": "ValueError", "exc_value": "boom", ...}]}
```

**FAQ Check**
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: macOS (Darwin 25.5.0)
- Haystack version: 3.4.0-rc0 (main, 5fa8cff71); Python 3.14.2 (3.10.19 for line numbers), structlog 26.1.0

