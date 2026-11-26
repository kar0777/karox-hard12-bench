You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

A named pipe at chroma.sqlite3 stops the MCP server from answering

**What happened?**

If `chroma.sqlite3` in a palace is a named pipe, or a symlink to one, the integrity probe opens it for reading and blocks until a writer shows up, while holding `_sqlite_integrity_refresh_lock`. Gated tool calls, `mempalace_status`, `mempalace_reconnect` and `GET /statusz` all run that probe or wait behind it.

On `develop` @ 38260df5, with a palace whose only entry is that `chroma.sqlite3`:

- stdio: the first `tools/call` for `mempalace_list_wings`, `mempalace_status` or `mempalace_reconnect` gets no answer in 30 s, and a `ping` sent after it gets none in 5 s. The session stays silent until the idle watchdog exits the process, 8 h by default.
- HTTP: the same three tools and `GET /statusz` get no answer in 15 s each, while `ping` and `GET /healthz` still answer.
- `python -m mempalace.repair rebuild` hangs in the same probe.

With an empty regular file in its place, those MCP requests answer within 1 s. `faulthandler` shows the probe blocked in `open(db_path, "rb")` in `config._is_wal_without_sidecars`, reached from `repair._quick_check_errors`. 3.9.0 hangs too, in `sqlite3.connect` in that function.

**What did you expect?**

The probe to refuse the pipe by type before opening it, as `sqlite_drawer_count` does for `repair-status` since #2393, and to report an integrity error. Gated tool calls would then get the `-32002` refusal, `mempalace_status` and `/statusz` would report `ok: false`, and the session would keep answering.

**How to reproduce:**

1. `mkdir /tmp/fifo-palace && mkfifo /tmp/fifo-palace/chroma.sqlite3`
2. Start `python -m mempalace.mcp_server --palace /tmp/fifo-palace` and send `initialize`, then `tools/call` for `mempalace_list_wings`, then `ping`, one JSON-RPC message per line.
3. `initialize` is answered. The tool call and the `ping` are not.

**Environment:**
- OS: Linux (WSL2)
- Python version: 3.12.3 (SQLite 3.45.1)
- MemPal version: `develop` @ 38260df5, and 3.9.0

