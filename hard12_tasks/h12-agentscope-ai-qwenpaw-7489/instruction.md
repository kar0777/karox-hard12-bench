You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug] macOS StdIO MCP spawn child re-enters backend_guard and kills the active backend

## Environment

- QwenPaw Desktop: 2.2.0-beta.6
- OS: macOS 26.4.1, Apple Silicon / arm64
- Installation: packaged macOS Desktop App
- Trigger: invoking a StdIO MCP tool
- Observed with: `@tokenhub-cash/mcp` / `tokenhub-tools`

## Symptoms

When a StdIO MCP tool is invoked during an active conversation:

- The current conversation is interrupted and may disappear from the UI.
- The Console workbench becomes stuck or unresponsive.
- Feishu long connections repeatedly disconnect and reconnect.
- The backend restarts every 2–5 minutes.
- `desktop.log` repeatedly reports that it is terminating an “orphaned” backend, although that PID is the active backend currently serving requests.

Captured example:

```text
== qwenpaw tauri sidecar 2026-09-02T09:09:53.070910 ==
argv=['.../qwenpaw-backend',
      '--multiprocessing-fork',
      'tracker_fd=87',
      'pipe_handle=89']

2026-09-02 09:09:53 | INFO |
qwenpaw/tauri/backend_guard.py:97 |
Terminating orphaned QwenPaw backend pid 51111

2026-09-02 09:09:58 | WARNING |
qwenpaw/tauri/backend_guard.py:103 |
Orphaned backend pid 51111 did not exit; killing it

QWENPAW_BACKEND_READY {"port":49427}
```

The same pattern was observed repeatedly in the rotated and current desktop logs.

## Steps to reproduce

1. Install or enable a StdIO MCP server.
2. Start QwenPaw Desktop.
3. Start a conversation.
4. Invoke any tool exposed by the StdIO MCP server.
5. Observe the backend process and `desktop.log`.

For example:

```bash
ps -axo pid,ppid,command | grep qwenpaw-backend
grep -E \
  'multiprocessing-fork|Terminating orphaned|Orphaned backend|QWENPAW_BACKEND_READY' \
  ~/.qwenpaw/desktop.log
```

## Actual behavior

The multiprocessing child re-enters the desktop backend entry point and calls:

```python
reconcile_singleton_backend(WORKING_DIR)
```

It reads the shared `desktop_backend.pid`, sees the PID of the active parent backend, identifies it as a QwenPaw backend, and sends SIGTERM followed by SIGKILL. The child then writes its own PID to the same PID file and may start another backend, producing a self-killing restart loop.

## Expected behavior

Only the top-level desktop sidecar should participate in single-backend reconciliation.

Multiprocessing spawn/fork helper processes must:

- not call `reconcile_singleton_backend`;
- not overwrite `desktop_backend.pid`;
- not bind the desktop backend port;
- continue only with their multiprocessing child bootstrap.

## Source-level evidence

In `v2.2.0-beta.6`:

- `_run_backend_server()` unconditionally calls the singleton guard:
  https://github.com/agentscope-ai/QwenPaw/blob/v2.2.0-beta.6/src/qwenpaw/tauri/entry.py#L296-L300

- The module entry point unconditionally calls `main()`:
  https://github.com/agentscope-ai/QwenPaw/blob/v2.2.0-beta.6/src/qwenpaw/tauri/entry.py#L393-L395

- The guard terminates any recorded PID whose command line contains `qwenpaw-backend`:
  https://github.com/agentscope-ai/QwenPaw/blob/v2.2.0-beta.6/src/qwenpaw/tauri/backend_guard.py#L76-L107

The spawned process has the characteristic command line:

```text
qwenpaw-backend --multiprocessing-fork tracker_fd=N pipe_handle=M
```

On the bundled macOS Python runtime, `multiprocessing.freeze_support()` does not dispatch to the multiprocessing child bootstrap on macOS, so the child reaches the normal entry path.

## Suggested fix

Guard the singleton reconciliation so it runs only for the top-level desktop sidecar.

For example, detect the multiprocessing child before backend startup using the multiprocessing spawn marker or an explicit sidecar-role environment variable:

```python
if not is_multiprocessing_child():
    reconcile_singleton_backend(WORKING_DIR)
```

A role/environment check supplied only by the Tauri sidecar would be preferable to relying solely on a command-line substring.

## Regression tests requested

1. Unit test that a process with `--multiprocessing-fork` does not terminate the PID recorded in `desktop_backend.pid`.
2. Unit test that multiprocessing children do not rewrite `desktop_backend.pid`.
3. Integration test that invoking a StdIO MCP tool keeps the original backend PID and port alive.
4. Regression test that normal desktop relaunch still cleans up a genuinely orphaned backend.

## Related change

The singleton guard was introduced by PR #5570 while fixing the orphaned-backend problem reported in #5550:

- https://github.com/agentscope-ai/QwenPaw/issues/5550
- https://github.com/agentscope-ai/QwenPaw/pull/5570

That fix handles orphaned top-level backends, but the current implementation does not distinguish them from multiprocessing child processes.
