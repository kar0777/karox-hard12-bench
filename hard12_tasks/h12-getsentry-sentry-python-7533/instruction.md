You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Memory leak: DedupeIntegration pins exception tracebacks in asyncio apps

### How do you use Sentry?

Self-hosted/on-premise

### Version

2.56.0 (Python 3.12.6)

### Steps to Reproduce

1. `sentry_sdk.init` with only `LoggingIntegration` + `DedupeIntegration` enabled.
2. In a long-lived asyncio task: build a local variable of ~1 MB so the frame carries that
   much data, raise `ValueError`, log with `logger.exception(...)`, keep the task running.
3. The exception, its traceback, and the 1 MB local stay alive for the lifetime of the task (and maybe after its death)


### Expected Result

After `logger.exception(...)` returns and the `except` block exits, the exception, its
traceback, and all its frame locals become unreachable and memory are freed

### Actual Result

The exception stays alive for the whole lifetime of the task. Memory grows with every new
captured exception on a new task, and the 1 MB local (plus the whole traceback chain)
stays pinned until the task itself ends.

RAM usage growth:
<img width="1704" height="784" alt="Image" src="https://github.com/user-attachments/assets/31f2d8d5-bcd5-4558-9171-f38b66571c67" />

## What I found

`DedupeIntegration._last_seen` is a `ContextVar` that stores the last captured exception.
The SDK tries to store it as `weakref.ref(exc)`, but Python builtins (`ValueError`,
`TypeError`, `KeyError`, ...) do not support weakref. On `TypeError` the SDK falls back to
a strong reference

Under asyncio every long-lived task keeps its own `ContextVar` state, so the strong
reference lives as long as the task. Through that reference the SDK pins:
- the exception,
- `exc.__traceback__`,
- every frame local in the traceback.

In our web crawler frame locals held response payloads in the 500 KB-1 MB range, which is where
the RSS growth came from

## Fix (what I did)

Replace the dedupe processor with one that stores `weakref.ref(exc)` when possible and
silently skips on `TypeError`. Dedupe is lost for builtins, leak is gone
