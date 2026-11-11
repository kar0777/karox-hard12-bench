You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Stop hook diary checkpoint always fails on sqlite_exact backend: "attempt to write a readonly database"

**What happened?**

With `backend: "sqlite_exact"`, the Stop hook's diary checkpoint fails every time:

```
[21:35:46] TRIGGERING SAVE at exchange 184
[21:35:46] Diary checkpoint failed: Backend open failed
[21:35:46] Transcript ingest started: <session>.jsonl -> <wing>
[21:36:28] Diary checkpoint failed: attempt to write a readonly database
[21:37:01] Diary checkpoint failed: attempt to write a readonly database
```

The transcript ingest that runs after the checkpoint works, and drawers are filed. Only the checkpoint drawer is lost. The same hook saved its checkpoint fine on the chroma backend a few minutes earlier, on the same machine and version.

(The first `Backend open failed` happened because `sqlite_exact.sqlite3` did not exist yet on the very first save. Every save after that fails with `readonly database`.)

**Likely cause**

`hooks_cli.py` writes the checkpoint by calling `tool_diary_write` in-process, not through an MCP round trip. In `mcp_server/_session.py::_get_collection`, any backend other than chroma opens read-only while no MCP writer lock is held:

```python
collection_read_only = _READ_ONLY or (
    backend_name in {"sqlite_exact", "rust_exact"}
    and getattr(_args, "transport", "stdio") == "stdio"
    and _MCP_WRITER_LOCK_CM is None
)
```

The hook process never acquires `_acquire_mcp_writer_lock()`. Tracing `sqlite3.connect` during the call shows only `...sqlite_exact.sqlite3?mode=ro&immutable=1` connections, followed by the readonly write error.

The same tool called through a real stdio MCP server (`mempalace-mcp`, `tools/call mempalace_diary_write`) succeeds, presumably because the server promotes itself to writer before the mutation.

**What did you expect?**

The Stop/PreCompact hook checkpoint should be written on `sqlite_exact` the same way it is on chroma. Either the hook should take the writer lock, or it should route the write through the normal write path.

**How to reproduce:**

1. In `~/.mempalace/config.json`, set `"backend": "sqlite_exact"`, a fresh `palace_path` and `"hooks": {"auto_save": true}`, then let one mine create the DB.
2. Run the Stop hook: `echo '{"session_id":"<id>","transcript_path":"<path to a .jsonl>","stop_hook_active":false}' | mempalace hook run --hook stop --harness claude-code`
3. `hook.log` shows `Diary checkpoint failed: attempt to write a readonly database`.

A minimal in-process repro gives the same result:

```python
from mempalace.mcp_server import tool_diary_write
print(tool_diary_write(agent_name="claude-code", entry="test", topic="checkpoint", wing="wing_test"))
# {'success': False, 'error': 'attempt to write a readonly database'}
```

**Environment:**
- OS: macOS 26.6.2 (Apple Silicon)
- Python version: 3.12.2
- MemPal version: 3.11.0 (PyPI), Claude Code plugin 3.12.0 from the marketplace
- I checked current `main`: `hooks_cli.py` still calls `tool_diary_write` directly, so the bug looks present there too. Not tested on main.

