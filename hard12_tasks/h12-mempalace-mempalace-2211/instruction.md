You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Windows stdio MCP: mempalace_mine returns OSError 22 when fd capture fallback is needed

## Reproduction

MemPalace 3.6.0 on Windows, launched as a long-lived MCP stdio server. Calling `mempalace_mine` with an existing directory (including `dry_run=true, limit=1`) returns immediately:

```json
{"success":false,"error":"mine failed: [Errno 22] Invalid argument","error_class":"OSError"}
```

The equivalent CLI reaches the expected peer-writer guard because the live MCP owns the palace lease. A normal console-process probe of `_capture_fd_stdout` succeeds, so the defect is specific to a hosted stdio stream.

## Root cause

`_capture_fd_stdout` documents Python-level fallback when fd-level stdio is unavailable, but only `os.dup(1)` is guarded. These operations can still raise `OSError` and bypass the fallback:

- `sys.stdout.flush()` / `sys.stderr.flush()`
- the initial `os.dup2(tmp.fileno(), 1)`
- restoration via `os.dup2(saved_fd, 1)`

The tests exercise only the successful fd path. MCP requires stdout to remain exclusively JSON-RPC, so restoration must remain fail-closed.

## Executable specification

### Resolved caller matrix

| Site | Effective cwd/path | Runtime/version/platform | Permissions/trust | Configuration precedence | Input existence |
| --- | --- | --- | --- | --- | --- |
| MCP stdio `mempalace_mine` | Absolute existing project directory | MemPalace 3.6.0 / Python tool environment / Windows | Same-user local MCP process; palace writer lease | Explicit tool args, then loaded MemPalace config | Existing directory required |
| CLI `mempalace mine` control | Same absolute directory | Same MemPalace/Python/Windows | Same user; correctly rejected while MCP lease is held | CLI args, then config | Existing directory required |
| Unit-level `_capture_fd_stdout` | Temporary process/file | Supported Python platforms | Process-local fds | Function contract | Callback exists |

### State/failure matrix

| State | Immutable ownership | Preflight | Mutation order | Mixed state | Atomicity | Concurrency | Idempotency | Recovery | Fail-closed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fd capture available | MCP owns protocol stdout | flush + duplicate fd | save, redirect, run, restore, close | Python and C output captured | restore in finally | one synchronous tool call | each call restores fd | saved fd restores stdout | yes |
| fd redirect unavailable before callback | MCP still owns protocol stdout | redirect attempt fails | close saved fd, run once under Python capture | C-level output cannot be captured | no fd mutation retained | unchanged | retry is safe | Python-only fallback | yes; protocol fd was never redirected |
| restoration fails after callback starts | MCP protocol stdout is at risk | saved fd exists | restoration attempted before return | fd state is unsafe | cannot claim successful capture | unchanged | no retry inside call | surface hard failure | yes; never silently continue |

### Acceptance-to-proof map

| Criterion or invariant | Positive proof | Negative or mutation proof | Command |
| --- | --- | --- | --- |
| Declared fallback executes callback once when initial fd redirect is unavailable | focused test returns callback result and Python output | monkeypatched initial `os.dup2` raises `OSError(22)`; current 3.6.0 fails | `pytest -q tests/test_mcp_mine.py -k fd_redirect_unavailable` |
| Successful fd path still captures Python/C stdout | existing capture test | direct fd write must not leak | `pytest -q tests/test_mcp_mine.py -k stdout_captured_not_leaked_to_fd` |
| Restoration failure does not silently report success | focused test raises/surfaces the restore error | monkeypatched second `os.dup2` fails | `pytest -q tests/test_mcp_mine.py -k restore_failure` |
| MCP framing stays clean | existing subprocess stdio tests | any non-JSON stdout fails | `pytest -q tests/test_mcp_stdio_protection.py` |

## Plan

1. Add the two focused failure-path tests and observe the initial-redirect test fail on 3.6.0.
2. Make setup transactional: guard flush/save/initial redirect; close any saved fd and use Python-only capture only if stdout was never redirected.
3. Keep restoration errors fail-closed after the callback starts.
4. Run focused mine/stdout tests, then the affected MCP test files.
