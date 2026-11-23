You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Cached-agent reuse closes newer Agent Persistence handle and leaves agent.persistence stale

## Summary

With the in-process chat backend and Hermes Agent's newer `Persistence` interface, a cached conversation can fail immediately on its next turn with `RuntimeError: persistence handle used after close`. This is a WebUI/Agent-main compatibility report; **I am not claiming it affects the older stable Agent v0.23.2 persistence implementation**.

The WebUI's `_session_db_is_open()` only checks `_conn`. A live `Persistence` handle has no `_conn`, so `_adopt_session_db_for_cached_agent()` closes it and replaces `agent._session_db`, leaving `agent.persistence` pointing at the now-closed handle. Turn-lease admission then fails on `store.coordination`, before provider execution.

## Versions / update verification

- WebUI latest stable: v0.52.679, commit `1f606ec5dbc10de79328c63d4ce9c30ef4738e73`.
- Also reproduced against freshly fetched WebUI `master`: `a236bb9b8bcca2b658a533c9f01530acc9010803`.
- Hermes Agent updated to current `main`: `3f5a11f624c8c3c7d0e99ddd8b4b7da97fcb7940` before repeating the reproduction.
- Linux; production WebUI interpreter Python 3.14.9. The minimal reproduction also runs with Python 3.13.5. No provider calls, credentials, or production database are needed.

## Steps to reproduce

In a WebUI checkout, with the current Agent checkout on `PYTHONPATH`, run the following. It executes the actual WebUI helpers with real lazy Agent persistence handles, using disposable state only:

```python
import ast
import logging
import tempfile
from pathlib import Path
from types import SimpleNamespace
from persistence_assembly import open_persistence, profile_scope

source = Path('api/streaming.py').read_text()
module = ast.parse(source)
names = {'_session_db_is_open', '_adopt_session_db_for_cached_agent'}
helpers = [n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in names]
ns = {'logger': logging.getLogger('repro')}
exec(compile(ast.Module(body=helpers, type_ignores=[]), 'webui_helpers', 'exec'), ns)

with tempfile.TemporaryDirectory() as home:
    scope = profile_scope(home=Path(home))
    old = open_persistence(scope)
    new = open_persistence(scope)
    agent = SimpleNamespace(_session_db=old, persistence=old)
    try:
        print('WebUI sees live handle as open:', ns['_session_db_is_open'](old))
        ns['_adopt_session_db_for_cached_agent'](agent, new)
        print('_session_db replaced:', agent._session_db is new)
        print('persistence retains old handle:', agent.persistence is old)
        agent.persistence.coordination
    finally:
        old.close()
        new.close()
```

## Actual result

```text
WebUI sees live handle as open: False
_session_db replaced: True
persistence retains old handle: True
RuntimeError: persistence handle used after close
```

Observed server traceback, with private paths removed:

```text
api/streaming.py: _run_agent_streaming -> agent.run_conversation(...)
agent/turn_facade.py: run_conversation -> admit_durable_turn_lease(...)
agent/turn_facade_lease.py: admit_durable_turn_lease
    acquired = acquire_turn_lease_waiting(store.coordination, ...)
persistence_assembly.py: __getattr__ -> _bound_store
    raise RuntimeError('persistence handle used after close')
```

## Expected result

Cached-agent reuse preserves a live persistence handle. If replacement is actually necessary, every Agent-owned persistence reference and dependent compressor binding must remain coherent. Preserve legacy SessionDB support and the resource-lifetime protections from #6143; do not close a shared handle underneath live children.

## Scope / related work

- Related historical fix: #6143 (legacy SessionDB/subagent lifetime). Its `_conn`-based liveness check does not recognize the new interface.
- Searched issues and PRs for the exact error, persistence/cached-agent variants, and both helper names; found no existing report or proposed fix for this specific mismatch.
- This is not session-deletion fencing, a provider authentication problem, or a request to implement the broader run-adapter RFC.

## Contract Routing

Task type: in-process runtime compatibility / cached-agent persistence ownership.
Touched area: Agent handle adoption and the credential self-heal sibling path in `api/streaming.py`.
Relevant docs: `AGENTS.md`, `CONTRIBUTING.md`, `docs/GUIDELINES.md`, `docs/CONTRACTS.md`, `docs/rfcs/webui-run-state-consistency-contract.md`, and `docs/architecture/agent-api-contract.md`.
Invariant: retained Agent persistence references stay live and coherent; unused per-request handles are released without invalidating retained users.

## AI disclosure

Investigated and written by Hermes Agent using OpenAI Codex provider, model `gpt-6.1-sol`, at the account holder's request. Source inspection and isolated real-handle reproduction were executed locally. No independent human code review is claimed. A focused, locally tested candidate fix will follow separately.

