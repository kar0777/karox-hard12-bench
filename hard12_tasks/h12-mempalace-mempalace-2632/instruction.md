You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

MCP kg_add leaks the palace mine lock on Windows (handle never released, blocks all mining)

**What happened?**

On Windows, a `kg_add` call through the MCP server (`mempalace-mcp`) acquires the palace mine lock but never releases it after the write completes. The lock file `~/.mempalace/locks/mine_palace_<hash>.lock` is created at the exact timestamp of the `kg_add` call, and an open file handle is retained indefinitely by the MCP server process. Every subsequent `mempalace mine` then fails with "is held by" lock contention — permanently, until the MCP process is killed and the lock file deleted manually.

**What did you expect?**

The mine-palace lock should be released when the KG write finishes (the `kg_add` call returned success with a `triple_id`), leaving subsequent mines free to proceed.

**How to reproduce:**

1. Run opencode (or any MCP client) with `mempalace-mcp` configured, palace at default location.
2. Have the model call `mempalace_mempalace_kg_add` (I did 4 adds in quick succession).
3. Calls return success; note `~/.mempalace/locks/mine_palace_<hash>.lock` now exists, created at the same second/millisecond as the kg_add calls, content empty.
4. Trigger any `mempalace mine` (or let an automation hook run it) — it reports the palace lock "is held by" the (still-running) MCP process and keeps failing.
5. `Remove-Item <lock>` on Windows → "being used by another process" (handle genuinely held).
6. Kill the `mempalace-mcp` process tree → handle released → lock file deletable → mining works again.

**Evidence (from my incident):**

- Lock file `mine_palace_eeea0af05abc81a9.lock` LastWriteTime `02:14:29` local, matching MCP tool-call log entries at `18:14:29.103/.129/.152/.173Z` to the millisecond (4 × `kg_add`).
- Lock file content: empty.
- Windows deletion error: `The process cannot access the file ... because it is being used by another process`.
- After killing all `mempalace-mcp` processes: lock deletable, `mempalace mine` immediately succeeded.
- Possibly related: several `mempalace-mcp` python processes had wedged (accumulated ~16s CPU then zero activity for 10+ minutes) — the handle appears to be held by a process that is otherwise unresponsive.

**Environment:**

- OS: Windows 11 (10.0.26231), PowerShell 7
- Python version: 3.10 (uv-managed cpython `cpython-3.10-windows-x86_64-none`)
- MemPal version: 3.10.0 (`mempalace status` reports backend chroma / chromadb 1.5.9), installed via `uv tool install mempalace`
- MCP server: `mempalace-mcp` spawned by OpenCode V2 (opencode 2.0.19) via stdio

Thank you for the project — the rest of the pipeline (mining, search, KG queries) has been rock solid.

