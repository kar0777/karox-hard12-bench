You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

LLMAssistantAggregator merges overlapping LLM response cycles into one corrupted assistant message

### Pipecat version

1.2.0 (also present on `main` and `v1.3.0` — see note below)

### Python version

3.12.12

### Operating System

Linux

### Issue description

`LLMAssistantAggregator` accumulates streamed assistant text in a single `_aggregation` buffer. That buffer is only cleared by `push_aggregation()` (on `LLMFullResponseEndFrame`) and by `_handle_interruptions()`. The turn-start path does **not** clear it:

```python
async def _handle_llm_start(self, _: LLMFullResponseStartFrame):
    await self._trigger_assistant_turn_started()

async def _trigger_assistant_turn_started(self):
    self._assistant_turn_start_timestamp = time_now_iso8601()   # no reset of _aggregation
    await self._call_event_handler("on_assistant_turn_started")
```

As a result, if a **second** `LLMFullResponseStartFrame` arrives while a turn is still open (buffer non-empty, and no `LLMFullResponseEndFrame`/interruption flushed it in between), the new cycle's `TextFrame`s are appended on top of the previous cycle's leftover. The two cycles are then committed to the context as **one merged, corrupted assistant message** — doubled prefixes and run-together words.

This is not a hypothetical: it happens in production when a second generation for the same turn is triggered before the first is flushed. In our case an idle/presence check issued via `LLMMessagesAppendFrame(run_llm=True)` (which pushes a context frame upstream and starts a generation) raced the user's reply, which started its own generation. The committed assistant message came out as e.g.:

```
[say lightly with [[say lightly with a friendly, conversational tone]say  Greatlightly,  with thanks. Just to confirm, ...
```

(We use Inworld TTS audio-tag prompting, so each line is prefixed with a `[say ... tone]` tag — hence the doubled `[[say ...]` and the mashed `Greatlightly`.)

`_handle_interruptions()` already does the right thing (`_trigger_assistant_turn_stopped(interrupted=True)` + `reset()`); the gap is that a new turn start does not get the same treatment.

### Reproduction steps

Minimal, no LLM / no transport — drives the aggregator's frame handlers directly to isolate the buffer behavior:

```python
import asyncio
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.frames.frames import (
    LLMFullResponseStartFrame, LLMFullResponseEndFrame, LLMTextFrame,
)

async def main():
    assistant = LLMContextAggregatorPair(context=LLMContext()).assistant()

    # Cycle A starts and streams some text...
    await assistant._handle_llm_start(LLMFullResponseStartFrame())
    await assistant._handle_text(LLMTextFrame("[tag] Great"))

    # Cycle B starts before A was flushed by an end frame / interruption.
    await assistant._handle_llm_start(LLMFullResponseStartFrame())
    await assistant._handle_text(LLMTextFrame("[tag] thanks, just to confirm."))
    await assistant._handle_llm_end(LLMFullResponseEndFrame())

    for m in assistant._context.get_messages():
        print(m)

asyncio.run(main())
```

Output:

```
{'role': 'assistant', 'content': '[tag] Great[tag] thanks, just to confirm.'}
```

In the wild the second cycle is started by a real frame (e.g. `LLMMessagesAppendFrame(run_llm=True)`) racing a user turn, rather than by calling the handler directly — but the merge mechanism is the same.

### Expected behavior

A new `LLMFullResponseStartFrame` arriving while a turn is still open should close/flush the stale turn first (the same way an interruption does), so the two response cycles surface as **two separate assistant messages**:

```
{'role': 'assistant', 'content': '[tag] Great'}
{'role': 'assistant', 'content': '[tag] thanks, just to confirm.'}
```

### Actual behavior

The two cycles are concatenated into a single corrupted assistant message (`'[tag] Great[tag] thanks, just to confirm.'`), which is then committed to the context and surfaced via `on_assistant_turn_stopped`.

### Logs

Note: still present on `main` and `v1.3.0` — `_trigger_assistant_turn_started()` does not reset `_aggregation` on either, and the non-realtime `_handle_llm_start` path is unchanged. A local workaround we use is to subclass the assistant aggregator and, in `_handle_llm_start`, flush+reset (`_trigger_assistant_turn_stopped(interrupted=True)` then `reset()`) when `self._assistant_turn_start_timestamp` is set and `self._aggregation` is non-empty, before delegating to `super()`.

