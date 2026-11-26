You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`Agent` loops to `max_agent_steps` when a reasoning model returns no text because it hits `max_output_tokens`

## Describe the bug

Under the default `exit_conditions=["text"]`, a reply that is empty because the model spent its whole `max_output_tokens` budget on reasoning does not exit the loop. The `Agent` keeps calling the LLM until `max_agent_steps`, and when the budget is systematically too small for the task every retry truncates identically, so all of those calls are wasted.

### Details
An assistant reply can be empty for two different reasons, and the `"text"` exit currently treats them the same:

| Reply is empty because | 2.29.0 | After #11665 | Desired |
| --- | --- | --- | --- |
| a malformed tool call was discarded | exits | retries | retries |
| generation hit `max_output_tokens` | exits | **retries until `max_agent_steps`** | exits |

#11665 fixed the first row, which was its intent. But the condition it introduced is `bool(last.text)`, so it changed the second row too.

### Expected behavior

The "Desired" column above: exit when the reply is empty because it was truncated, and keep #11665's recovery loop for every other empty reply.

## Reproduce
### What we observed

Measured against the real OpenAI API, `gpt-5.6-terra`, `OpenAIResponsesChatGenerator` (streaming), haystack 2.31.0.

With a reasoning budget well below what the task's reasoning pass needs (`max_output_tokens=256`, `reasoning={"effort": "high"}`, on a hard combinatorics prompt), the truncation is deterministic rather than a coin flip:

```
trial 1: text=EMPTY  output_tokens=256 reasoning_tokens=256  status='incomplete' reason='max_output_tokens'
trial 2: text=EMPTY  output_tokens=256 reasoning_tokens=256  status='incomplete' reason='max_output_tokens'
trial 3: text=EMPTY  output_tokens=256 reasoning_tokens=256  status='incomplete' reason='max_output_tokens'
trial 4: text=EMPTY  output_tokens=256 reasoning_tokens=256  status='incomplete' reason='max_output_tokens'
=> zero-text on 4/4 attempts
```

Wrapping the same generator in an `Agent` with `max_agent_steps=5`, one tool, and the default `exit_conditions=["text"]`:

```
assistant replies (= real API calls): 5
  [0] user      'Let S be the set of all 12-digit positive integers whos...'
  [1] assistant EMPTY
  [2] assistant EMPTY
  [3] assistant EMPTY
  [4] assistant EMPTY
  [5] assistant EMPTY

reasoning tokens burned across the run: 1280
Agent reached maximum agent steps of 5, stopping.
```

This becomes worse when `max_agent_steps` is higher. For example, `max_agent_steps` is 100 by default.

### Reduced reproduction, no API key

```python
from typing import Any

from haystack import component
from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import Tool

llm_calls = 0


@component
class TruncatedGenerator:
    """Mimics a reply that hit `max_output_tokens` during reasoning: no text, no tool calls."""

    @component.output_types(replies=list[ChatMessage])
    def run(self, messages: list[ChatMessage], tools: Any = None, **kwargs: Any) -> dict:
        global llm_calls
        llm_calls += 1
        return {
            "replies": [
                ChatMessage.from_assistant(
                    "",
                    meta={"status": "incomplete", "incomplete_details": {"reason": "max_output_tokens"}},
                )
            ]
        }


def noop(x: str) -> str:
    """A tool, so that a ToolInvoker is configured."""
    return x


tool = Tool(
    name="noop",
    description="noop",
    function=noop,
    parameters={"type": "object", "properties": {"x": {"type": "string"}}, "required": ["x"]},
)

agent = Agent(
    chat_generator=TruncatedGenerator(),
    tools=[tool],
    exit_conditions=["text"],   # the default
    max_agent_steps=15,
)
agent.warm_up()
agent.run(messages=[ChatMessage.from_user("Write a very long essay.")])

print(f"LLM calls: {llm_calls}   (expected 1, got {llm_calls})")
```

On 2.31.0 this prints `LLM calls: 15`. On 2.29.0 and earlier it prints `LLM calls: 1` (verified by running the same script against 2.29.0).

## Possible fix

### 1. Retry on the discarded tool call itself, not on empty text.

The condition #11665 wanted to retry on is "haystack discarded a malformed tool call". Every generator already detects exactly that and logs a warning, then drops the fact:

| Generator | Discard site (2.31.0) |
| --- | --- |
| `OpenAIChatGenerator` | `chat/openai.py:634` |
| `OpenAIResponsesChatGenerator` | `chat/openai_responses.py:611`, `:825` |
| shared streaming path | `generators/utils.py:134` |
| `HuggingFaceAPIChatGenerator` | `chat/hugging_face_api.py:77` |
| `HuggingFaceLocalChatGenerator` | `chat/hugging_face_local.py:85` |

If that were recorded on the message instead of only logged, the Agent could retry on it directly rather than inferring it from `bool(last.text)`. That is more precise, and it keeps provider knowledge out of `agent.py`: each generator sets the flag at its own discard site, and the Agent reads one haystack-owned field.

It also means the Agent never needs to know about truncation. A truncated reply simply would not set the flag, so it exits by default. The same goes for other empty-text replies that are currently retried by mistake, such as a reasoning-only reply or a content-filter stop.

### 2. If keeping the empty-text condition, exclude truncation explicitly.
On OpenAI, the only provider we tested, the signal is:

| OpenAI API | Generator | Truncation signal on the message |
| --- | --- | --- |
| Responses | `OpenAIResponsesChatGenerator` | `meta["incomplete_details"]["reason"] == "max_output_tokens"` |
| Chat Completions | `OpenAIChatGenerator` | `meta["finish_reason"] == "length"` |

This is localized to `agent.py` but needs provider-specific knowledge there, or a normalized `finish_reason == "length"` that generators populate consistently. Other providers report truncation differently.

The check is inline in `run` (`haystack/components/agents/agent.py:869`) and `run_async` (`:1113`) on 2.31.0, and extracted into `_is_text_exit` (`:201-211`) on 3.0.0.

**FAQ Check**

- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: Linux
- Haystack version: 2.31.0
