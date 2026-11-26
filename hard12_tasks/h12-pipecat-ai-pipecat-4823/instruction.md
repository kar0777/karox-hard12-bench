You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Same-named tool in a new advertised set keeps the previous handler (regression of flows #269/#270 under context-driven registration)

### Summary

pipecat-ai-flows #269 / #270 (released in flows 1.1.1) fixed *"Re-declaring a function in a new node silently keeps the previous node's handler bound"* by always re-registering the node's functions on the LLM service. With the move to context-driven tool registration in **pipecat 1.4.0 + pipecat-flows 1.3.0**, that fix appears to have regressed — and the responsible mechanism now lives in pipecat core, so the repro below reproduces it on a bare `LLMService` with no flows involved.

### Cause

In flows 1.3.0, `FlowManager._set_node` no longer calls `llm.register_function`; it advertises the node's tools via `_update_llm_context(functions=ToolsSchema(...))` (an `LLMSetToolsFrame` carrying handlers on the schemas). pipecat 1.4.0 then registers handlers from the advertised `LLMContext` in `LLMService._sync_registered_tool_handlers` (run on every `LLMContextFrame`). That method:

- prunes handlers for names that **leave** the advertised set (orphan unregistration — great), but
- **skips registering a name that is already registered** (`_register_advertised_tool_handlers`: *"Any tool whose name is already registered … is left untouched"*).

So when two consecutive advertised tool sets both carry a tool with the **same name but a different handler** (e.g. a per-node closure), the second handler is silently ignored, because the name never leaves the advertised set (no prune) and the register step skips it (already present). This is exactly the #269 scenario, now in core.

### Minimal repro (pipecat 1.4.0, no flows)

```python
from pipecat.adapters.schemas.function_schema import FunctionSchema
from pipecat.adapters.schemas.tools_schema import ToolsSchema
from pipecat.services.llm_service import LLMService

async def hA(params): ...
async def hB(params): ...

def tool(name, h):
    return ToolsSchema(standard_tools=[
        FunctionSchema(name=name, description="d", properties={}, required=[], handler=h)
    ])

llm = LLMService()
llm._sync_registered_tool_handlers(tool("x", hA))
llm._sync_registered_tool_handlers(tool("x", hB))  # re-advertise same name, new handler
# llm._functions["x"] still wraps hA, not hB
```

Observed against `pipecat-ai==1.4.0`:

```
after A: x -> hA
after B: x -> hA      # second handler ignored
x present after advertising only y: False   # orphan unregistration works
```

(Orphan unregistration works: advertising only `tool("y", ...)` afterward does drop `x`, then re-advertising `x` registers it afresh. So the bug only bites when the same name is advertised **continuously across the transition** — directly adjacent tool sets, or always-on tools.)

### Impact

Any tool name shared across two consecutive advertised tool sets with **different** handlers runs the **first** handler instead of the current one, with no warning. In a Flows app this hits any tool name shared across nodes with per-node handlers (global / transition / interrupt tools keyed by the originating node) after a transition.

### Suggested direction

`LLMService` already distinguishes `auto_registered=True` entries (from advertised tool sets) from explicit `register_function` registrations. The fix can live entirely in core: when an advertised set carries a **different** handler for a name that is currently registered as `auto_registered`, rebind it — while still leaving explicit registrations untouched (preserving the existing "explicit wins / repeated frames don't churn" invariant). Happy to send a PR if a maintainer confirms this is the preferred shape (vs. e.g. flows forcing re-registration downstream).

### Versions

`pipecat-ai==1.4.0`, `pipecat-ai-flows==1.3.0`.

### Note

We worked around it downstream by making our handlers node-agnostic (resolving the current node at call time), so this is not blocking us — filing for visibility, since it reverses the pipecat-ai-flows #269/#270 fix under the new context-driven registration model.

