You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

/api/btw writes its duplicate-stream 409 while holding STREAMS_LOCK

`_handle_btw` (POST `/api/btw`) writes its duplicate-stream 409 while holding `STREAMS_LOCK`:

```python
# api/routes.py (exp-v0.52.675, ~29046)
current_stream_id = getattr(s, "active_stream_id", None)
if current_stream_id:
    with STREAMS_LOCK:
        if current_stream_id in STREAMS:
            return j(handler, {"error": "session already has an active stream"}, status=409)
```

AGENTS.md: "Keep HTTP response writes outside runtime registry locks." `j(handler, ...)` writes the status line, headers and body to the client socket while every stream start, Stop, steer and SSE registration that needs `STREAMS_LOCK` waits. The comment says it copies chat/start's guard, but chat/start's 409 sites decide under the lock and respond after releasing it. This is the only response write under `STREAMS_LOCK` on master.

**Impact:** low. The body is tiny and normally fits the socket send buffer, so the write rarely blocks. But a client that has stopped reading (or a full send buffer) would stall the stream registry for every session for the duration of the write.

**Fix shape:** decide under the lock, respond outside it:

```python
if current_stream_id:
    with STREAMS_LOCK:
        busy = current_stream_id in STREAMS
    if busy:
        return j(handler, {"error": "session already has an active stream"}, status=409)
    s.active_stream_id = None
```

A regression test can assert `STREAMS_LOCK` is not held when the handler's response is written (wrap `j` and check `STREAMS_LOCK.locked()` from inside it, as other lock-scope tests do).

Found during the independent review of #9028.

