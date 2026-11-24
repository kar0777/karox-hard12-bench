You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

logging: MEMPALACE_LOG_FILE lines carry no timestamp - add one, and log one line per palace call with lock-wait and run time

---

### Summary

The `MEMPALACE_LOG_FILE` handler formats bare `%(message)s` (`mempalace/mcp_server/_logging.py`, still so on `main` as of 2026-09-29), so a server-side log cannot be lined up against a client-side timeout. And there is no per-call record at all: `_http_dispatch` in `mempalace/mcp_server/http.py` takes the read or exclusive lock and calls `handle_request` with no timing, so the only timing signal is the write-stall watchdog. With the writer-preferring dispatch lock (#2398) a slow call and a call queued behind a writer look identical from the client - and from the log.

### Proposed change (we run it as a local patch and can send a PR)

- Formatter `"%(asctime)s %(levelname)s %(message)s"` on the `MEMPALACE_LOG_FILE` handler.
- In `_http_dispatch`, time the lock wait and the handler separately and log one INFO line per palace tool call: `CALL <tool> <read|write> wait=<ms> run=<ms> <ok|error>`; WARNING `SLOW CALL ...` at or above `MEMPALACE_SLOW_CALL_WARN_SECS` (default 20; parsed the same way as `MEMPALACE_MCP_WRITE_STALL_WARN_SECS`). Lock-free tools are unaffected. The logging call never raises, so a logging failure cannot fail the call.

### What it looks like on a live server (188k drawers, chromadb 1.5.9, two HTTP clients)

```
2026-09-15 09:49:06,548 WARNING SLOW CALL mempalace_status read wait=0ms run=36407ms ok
2026-09-15 09:59:43,301 INFO CALL mempalace_diary_read read wait=0ms run=31ms ok
2026-09-15 10:01:39,663 WARNING SLOW CALL mempalace_diary_write write wait=0ms run=78886ms ok
2026-09-28 11:15:45,960 WARNING SLOW CALL mempalace_diary_write write wait=0ms run=106753ms ok
2026-09-28 11:15:51,024 WARNING SLOW CALL mempalace_search read wait=104436ms run=5063ms ok
```

`wait=0ms` on the 36 s `status` is what told a cold page cache from lock contention; the last pair shows a 5 s search that spent 104 s queued behind a write. Neither distinction was visible before, and the timestamps are what let us match each line to a client "Request timed out" and prove the write had landed (the retry then filed a duplicate drawer).

### Environment

```
mempalace 3.9.0 (uv tool install), chromadb 1.5.9, Python 3.14.6, Windows 11 Pro.
Transport: mempalace serve --host 0.0.0.0 --port 8765, two Claude Code HTTP clients.
Palace: 188,875 drawers, chroma.sqlite3 1.55 GB, embedding_metadata 2,845,774 rows.
```

