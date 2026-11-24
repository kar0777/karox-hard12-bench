You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

LLM component returns an undeclared `exit_reason` output, causing a pipeline warning and an unconnectable socket

**Describe the bug**

The `LLM` component returns an `exit_reason` key from `run()`/`run_async()` but does not declare it in `@component.output_types`, so every pipeline run logs the framework's undeclared-output warning, the key is silently dropped, and `Pipeline.connect("llm.exit_reason", ...)` is impossible.

`haystack/components/generators/chat/llm.py:92` declares only `messages`/`last_message`/`token_usage`, while `run()` (`:164`) pops `step_count` and `tool_call_counts` but not `exit_reason`, which the `Agent` base returns from `_public_outputs` (`haystack/components/agents/agent.py:88-93, 121-123`). The `Agent` component exposes `exit_reason` as a socket; its `LLM` subclass does not.

**Error message**

```
WARNING:haystack.core.pipeline.base:Component 'llm' (type: LLM) returned output keys {'exit_reason'} that are not declared in its output types. These keys will be ignored and not passed to downstream components.

PipelineConnectError: 'llm.exit_reason' does not exist
```

Probe output:

```
keys: ['exit_reason', 'last_message', 'messages', 'token_usage']
declared outputs: ['last_message', 'messages', 'token_usage']
```

**Expected behavior**

Either expose `exit_reason` like `Agent` does (declare it in `set_output_types` so it can be connected), or remove it from the returned dict in `LLM.run`/`run_async` the same way `step_count`/`tool_call_counts` are removed — matching the `run()` docstring, which lists only the three declared outputs.

**To Reproduce**

Build a pipeline containing the `LLM` component with a scripted chat generator, run it, and inspect the missing-output warning and `Pipeline.connect("llm.exit_reason", ...)`. Repro scripts `probe_llm.py`, `probe_llm_async.py`, `probe_llm_connect.py` are available; happy to attach them.

**Additional context**

- Fix direction is a design choice (expose vs drop), hence an issue rather than a drive-by PR.
- Searched open and closed issues/PRs for `exit_reason`/undeclared outputs: nearest is #12890 (Agent `exit_reason` vs `last_message` ordering, different); closed PRs #11427/#12277 are unrelated.

**System**

- OS: Windows 11
- Haystack version: `4b5dd70` (main, v3.5.0-rc0)

Reported with AI assistance (Claude); the reproduction was executed and verified locally.

