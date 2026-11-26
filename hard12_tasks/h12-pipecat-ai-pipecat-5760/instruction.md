You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Per-tool timeout_secs is disarmed by an intermediate (is_final=False) result callback — hung async tools are never bounded

## Description

A per-tool `timeout_secs` (and the global `function_call_timeout_secs`) stops protecting a function call the moment the handler reports an intermediate result with `FunctionCallResultProperties(is_final=False)`. In `LLMService._run_function_call`, the shared `function_call_result_callback` cancels `timeout_task` on every delivery — the `is_final` check gates `runner_item.settled`, but the timer cancel below it runs for intermediate updates too:

```python
if is_final:
    runner_item.settled = True

# Cancel timeout task if it exists
if timeout_task and not timeout_task.done():
    await self.cancel_task(timeout_task)
```

An async tool that reports "working on it" a millisecond in — the pattern the docs invite for async function calls — permanently disarms its own deadline. If the handler then hangs, nothing bounds it; a voice caller sits in silence until an idle/silence mechanism ends the call.

The current function-calling docs say a call exceeding `timeout_secs` is cancelled, and that an intermediate result does not close the call — which conflicts with the intermediate result disabling the deadline. No existing issue seems to report this specifically. The closest history: a comment on #4936 ("a valid result callback disables the deadline") and the unmerged PR #5195 built on that rule — but the subsequently merged #5291 semantics and the docs describe the deadline as covering the handler's execution.

Checked on pipecat 1.8.0 and on current `main` (the callback region is identical).

## Deterministic repro

Minimal harness driving `_run_function_call` directly — a handler with `timeout_secs=1.0`, `cancel_on_interruption=False`, that pushes one intermediate update then sleeps 4s:

- **With the intermediate update**: the timeout never fires; the call settles only when the handler returns at ~4.0s.
- **Control (no intermediate update)**: `FunctionCallCancelFrame` with `run_llm=True` is broadcast at ~1.0s, as documented.

Repro script: https://gist.github.com/mannyb223/c71701f2541a83567b5ad560d0f35712

Output (with update):
```
+  0.0s call start (timeout_secs=1.0)
+  0.0s handler start
+  0.0s intermediate update pushed
+ 4.01s broadcast FunctionCallResultFrame     <- only the handler's own late return
```

Control:
```
+  0.0s call start (timeout_secs=1.0)
+  0.0s handler start
+  1.0s broadcast FunctionCallCancelFrame run_llm=True
```

## Suggested fix

Gating the cancel on finality restores the documented behaviour; re-running the repro with this one-line change makes the timeout fire at 1.0s with the intermediate update present:

```python
if is_final and timeout_task and not timeout_task.done():
    await self.cancel_task(timeout_task)
```

If the #4936-comment behaviour (any callback disarms) is actually the intended design, a docs note would help — but then there is no way to bound an async tool that reports progress, which is exactly the long-running shape `timeout_secs` seems built for.

