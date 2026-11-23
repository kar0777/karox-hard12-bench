You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Tool default arguments behviour changes when called Agent directly and via pipeline

**Describe the bug**
The same Agent with the same tool behaves differently:
- Called directly -> the tool uses its own default.
- Run inside a Pipeline -> the tool gets `None`.

**Error message**
No error is raised. Output of `hatch -e test run python test_script.py`:
```
Agent alone      : top_k=5
Agent in pipeline: top_k=None
```

**Expected behavior**
Inside a Pipeline, the tool should also get its default: `top_k=5`.

**Additional context**
The Pipeline is indeed handing off the default arguments as `None` (becuase no kwargs are set in pipeline), but the Agent treats that `None` as a value and overwrites the tool's default argument with `None`.
https://github.com/deepset-ai/haystack/blob/d768bb8fa815f0bb1ed39056327835c952cdedf8/haystack/components/agents/agent.py#L570

When users are developing, they expect to set solid defaults and have the Agent work as expected, but the same Agent silently behaves differently in a Pipeline: the tool gets `None` instead of its default.

**Proposed naive solution**
Skip `None` values when the Agent seeds its State, so an input that was never provided does not become a state value:
https://github.com/deepset-ai/haystack/blob/d768bb8fa815f0bb1ed39056327835c952cdedf8/haystack/components/agents/agent.py#L819

change:
```python
state_kwargs: dict[str, Any] = {
    key: kwargs[key] for key in self.resolved_state_schema.keys() if key in kwargs and kwargs[key] is not None
}
```

**Trade off**
Inside the Pipeline, the Agent can't tell "not provided" from "explicitly `None`" anyway, because both arrive as `None`. I I tried it locally, the change mentioned above prints `top_k=5` in the Pipeline, and the existing Agent unit tests pass.

I'm happy to open a PR with a regression test if this approach sounds right.

**To Reproduce**
```python
from typing import Any

from haystack import Pipeline, component
from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage, ToolCall
from haystack.tools import tool

# One way to set a default argument for a tool.
@tool(inputs_from_state={"top_k": "top_k"})
def search(query: str, top_k: int = 5) -> str:
    """Search for documents."""
    return f"top_k={top_k}"


# A fake LLM: if the tool hasn't run yet, call it; otherwise finish.
@component
class FakeLLM:
    @component.output_types(replies=list[ChatMessage])
    def run(self, messages: list[ChatMessage], tools: Any = None, **kwargs: Any) -> dict:
        if messages[-1].tool_call_result:
            return {"replies": [ChatMessage.from_assistant("done")]}
        call = ToolCall(tool_name="search", arguments={"query": "haystack"})
        return {"replies": [ChatMessage.from_assistant(tool_calls=[call])]}


def new_agent() -> Agent:
    return Agent(chat_generator=FakeLLM(), tools=[search], state_schema={"top_k": {"type": int}})


question = [ChatMessage.from_user("find something")]

# When called directly, the Agent falls back to the tool's default value.
result = new_agent().run(messages=question)
print("Agent alone      :", result["messages"][-2].tool_call_result.result)

# Passing a value directly works.
# result = new_agent().run(messages=question, top_k=1)
# print("Agent alone      :", result["messages"][-2].tool_call_result.result)

# If nothing is passed to the Agent in a Pipeline, None is passed down, and the Agent literally replaces the default value with None.
pipe = Pipeline()
pipe.add_component("agent", new_agent())
result = pipe.run({"agent": {"messages": question}})
print("Agent in pipeline:", result["agent"]["messages"][-2].tool_call_result.result)

# Passing a value in a Pipeline also works.
# pipe = Pipeline()
# pipe.add_component("agent", new_agent())
# result = pipe.run({"agent": {"messages": question, "top_k": 1}})
# print("Agent in pipeline:", result["agent"]["messages"][-2].tool_call_result.result)
```

**FAQ Check**
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: Windows 11 Pro, 25H2
- Haystack version: main @ d768bb8fa815f0bb1ed39056327835c952cdedf8 (3.6.0-rc0)

<!-- handled-internally -->
---
👋 Hello there! This issue will be handled internally and isn't open for external contributions. If you'd like to contribute, please take a look at issues labeled [contributions welcome](https://github.com/orgs/deepset-ai/projects/14) or [good first issue](https://github.com/deepset-ai/haystack/contribute). We'd really appreciate it!
<!-- /handled-internally -->
