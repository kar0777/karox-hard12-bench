You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

serve: out-of-range --port leaks a raw OverflowError traceback instead of an actionable error

## Friction point (dogfood, release 0.12.16)

A new user who typos the port past 65535 gets a raw Python traceback instead of the friendly, actionable message we already emit for other port problems.

### Repro
```
$ rapid-mlx serve qwen3.5-4b-4bit --port 99999
...
  File "vllm_mlx/cli.py", line 323, in _port_preflight_or_die
    _sock.bind((probe_host, port))
OverflowError: bind(): port must be 0-65535.
```
Same for `--port 70000` (any value > 65535).

### Root cause
`_port_preflight_or_die` (`vllm_mlx/cli.py` ~L320-336) wraps `socket.bind()` in `except OSError`, which correctly turns a busy port into a clean message:
```
  Error: Port 8155 is already in use on 127.0.0.1.
  Try a different port: rapid-mlx serve <model> --port 8156
```
But an out-of-range port makes `bind()` raise **OverflowError** (not an `OSError` subclass), so it escapes the handler and prints a cryptic traceback.

### Expected
Validate the port range (0–65535) up front — or widen the preflight to also catch `OverflowError`/`ValueError` — and print the same style of actionable message, e.g.:
```
  Error: --port 99999 is out of range. Ports must be 0-65535.
```

### Notes
- Not a release blocker; cosmetic/UX. Filed from the 0.12.16 dogfood pass.
- `--port 0` is legitimately valid (OS picks an ephemeral port) and should keep working.
- Preflight ordering is correct — it runs before `load_model`, so this fails fast without wasting a model load. Only the error *presentation* is the problem.

_Reported by an AI agent (Claude) during release dogfood._
