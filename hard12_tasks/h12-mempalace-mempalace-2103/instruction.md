You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

MCP --read-only gates on the palace-write set, so mempalace_hook_settings still rewrites config.json

## What happened?

A server started with `--read-only` (or `MEMPALACE_MCP_READ_ONLY=1`) still advertises `mempalace_hook_settings` in `tools/list` and executes it, rewriting `~/.mempalace/config.json` on the server host.

Both halves of the gate test one set. `_mcp_read_only_refusal` (`mcp_server.py:4683`) and the `tools/list` filter (`:4764`) check `_MUTATING_TOOLS` (`:386-403`). That set exists for the peer-writer lease: `_mcp_peer_writer_refusal` (`:475-496`) uses it to decide which calls need the palace mine lock. `mempalace_hook_settings` touches no palace state, so it is rightly absent from it, but it does write, through `MempalaceConfig.set_hook_setting` (`config.py:1010-1019`). `service.WRITE_TOOLS` already lists the tool as a write, so the daemon's allowlist and the read-only gate disagree about it.

`mempalace_memories_filed_away` is the same shape: no palace state, but it unlinks `~/.mempalace/hook_state/last_checkpoint` (`:3741`, `:3750`).

#1930 fixed this class once, for `checkpoint` and `delete_by_source`. One line each worked there because both are palace writes, so the lease wanted them too. Neither tool above is a palace write, so the same move would put them under the palace lease, and a server that lost the lease to a peer would start refusing calls the lease has no say over.

## What did you expect?

A read-only server to refuse every tool that changes state on the server host, as `--read-only` promises: "Expose recall only: mutating tools are hidden and refused".

## How to reproduce

1. Start a read-only server against a palace whose `~/.mempalace/config.json` has `"desktop_toast": false`:

   ```bash
   mempalace serve --read-only --host 127.0.0.1 --port 8765 &
   ```

2. Ask for the tool list. The tool is advertised, though it should be hidden:

   ```bash
   curl -s localhost:8765/mcp -H 'Content-Type: application/json' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | grep -c mempalace_hook_settings
   ```

   ```
   1          expected 0
   ```

3. Call it. It succeeds instead of returning `-32003`:

   ```bash
   curl -s localhost:8765/mcp -H 'Content-Type: application/json' \
     -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"mempalace_hook_settings","arguments":{"desktop_toast":true}}}'
   ```

   ```
   "success": true, "updated": ["desktop_toast → True"]
   ```

4. The file on disk has changed:

   ```bash
   cat ~/.mempalace/config.json
   ```

   ```
   "desktop_toast": true
   ```

Same over stdio (`mempalace-mcp --read-only`) and with the environment variable instead of the flag.

## Environment

- OS: Ubuntu 24.04 on WSL2 (kernel 6.18)
- Python version: 3.12.3
- MemPal version: develop `aa89bd82` (v3.6.0)

