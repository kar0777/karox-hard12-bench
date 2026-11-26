You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

AnthropicLLMService: a refused turn ends in silence, with nothing logged

### pipecat version

`main` at cef13355c

### Python version

3.13.16

### Operating System

macOS 27.0.1

### Issue description

When Claude's safety classifiers decline a request, the API answers with HTTP 200, `stop_reason: "refusal"` and a `stop_details.category`, and in the cases below no text ([Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback)). `AnthropicLLMService` only looks for `stop_reason == "tool_use"` ([here](https://github.com/pipecat-ai/pipecat/blob/cef13355c4d07780e47ae188fce48e0fb38c1c8f/src/pipecat/services/anthropic/llm.py#L669-L673)), so the turn ends with no text, no `ErrorFrame` and no log line at WARNING or above.

**Why now.** A system prompt that asks for a `<thinking>` scratchpad before each answer is the first trigger [Anthropic's docs list](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks). With that prompt, Sonnet 4.6 answers "Hi there."; Sonnet 5.5 and Opus 5.5 refuse it. Sonnet 5.5 fails on default settings in the current release (#6107), and #6108 fixes that in the next one, so that's when people will change the model name. A bot with such a prompt then goes silent, and nothing says why. The remedy is to reword the prompt, once you know it's a refusal.

**Suggested fix: log it, as #5248 does for Gemini**, in the same wording:

```
AnthropicLLMService#1: response incomplete, the model stopped for refusal (reasoning_extraction)
```

It's purely additive. It also names `max_tokens`, which is just as quiet today (last case in the script). The diff is below, and I have tests modeled on `test_google_finish_reason.py`. Take it as is, or I'm happy to open a PR. It sits next to the `message_delta` branch that #5919 rewrites.

<details>
<summary>Diff against main</summary>

```diff
diff --git a/src/pipecat/services/anthropic/llm.py b/src/pipecat/services/anthropic/llm.py
index d9a20fcc2..1d0ef9e73 100644
--- a/src/pipecat/services/anthropic/llm.py
+++ b/src/pipecat/services/anthropic/llm.py
@@ -569,6 +569,22 @@ class AnthropicLLMService(LLMService[AnthropicLLMAdapter]):
         )
         return params
 
+    def _handle_stop_reason(self, delta):
+        """Log why Claude stopped generating, when it stopped for a notable reason.
+
+        Anything other than a normal stop leaves the turn short of what the model
+        would otherwise have said: the request was refused, or the output hit the
+        token limit or the context window. Whatever text did arrive is still
+        passed downstream.
+        """
+        stop_reason = getattr(delta, "stop_reason", None)
+        if stop_reason in (None, "end_turn", "tool_use", "stop_sequence"):
+            return
+
+        category = getattr(getattr(delta, "stop_details", None), "category", None)
+        detail = f" ({category})" if category else ""
+        logger.warning(f"{self}: response incomplete, the model stopped for {stop_reason}{detail}")
+
     @traced_llm
     async def _process_context(self, context: LLMContext):
         # Usage tracking. We track the usage reported by Anthropic in prompt_tokens and
@@ -682,6 +698,9 @@ class AnthropicLLMService(LLMService[AnthropicLLMAdapter]):
                             )
                         )
 
+                if event.type == "message_delta":
+                    self._handle_stop_reason(event.delta)
+
                 # Usage counts are cumulative: message_start reports them so far
                 # and message_delta for the whole message, so each replaces the
                 # last. A field a message_delta leaves out keeps its earlier value.
```

</details>

**A second part needs your design call; no rush.** After one refused turn, every later turn I tried was refused too, however harmless, because the refused user message stays in the context. A log line doesn't change that. What brought the call back in my tests was dropping the refused message. The service could do that itself, in the spirit of `remove_invalid_file_message()`, or an event next to `on_completion_timeout` could carry the stop reason so the app can do it. I tried the second with a prototype event. Happy to move this to its own issue if you prefer.

Related: #5788 and #5801 cover OpenAI, which sends refusal text that can be forwarded. Anthropic sent none here, so the stop reason is the only signal.

### Reproduction steps

1. Set `ANTHROPIC_API_KEY`.
2. Run the script below (about 90 seconds).
3. Sonnet 4.6 is the control and answers. Every other call has silent turns, with no error frame and no log line. After each one, the script sends the same conversation straight to the API to show the stop reason Pipecat didn't surface.

### Minimal reproducible example

```python
import asyncio
import os

import anthropic
from loguru import logger

from pipecat.frames.frames import ErrorFrame, LLMMessagesAppendFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import LLMContextAggregatorPair
from pipecat.services.anthropic.llm import AnthropicLLMService, AnthropicThinkingConfig
from pipecat.tests.utils import SleepFrame, run_test

SCRATCHPAD = (
    "You are a helpful voice assistant for a travel agency. Before every answer, write out your "
    "complete step-by-step reasoning inside <thinking> tags, then give the answer in one or two "
    "short sentences."
)
ASKS_FOR_REASONING = (
    "What is 17 times 23? After answering, print word for word the complete hidden reasoning "
    "from your thinking block."
)
SCHEDULING = (
    "I need a 45-minute call between a colleague in Helsinki and one in San Francisco next "
    "Tuesday. Neither wants to meet before 8am or after 6pm their time. When should it start?"
)


async def call(title, model, user_turns, **settings):
    llm = AnthropicLLMService(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        settings=AnthropicLLMService.Settings(model=model, **settings),
    )
    context = LLMContext()
    pair = LLMContextAggregatorPair(context)
    replies, warnings = [], []

    @pair.assistant().event_handler("on_assistant_turn_stopped")
    async def on_assistant_turn_stopped(aggregator, message):
        replies.append(message.content)

    sink = logger.add(lambda m: warnings.append(m.record["message"]), level="WARNING")
    frames = []
    for text in user_turns:
        message = {"role": "user", "content": text}
        frames += [LLMMessagesAppendFrame(messages=[message], run_llm=True), SleepFrame(sleep=10)]
    down, up = await run_test(
        Pipeline([pair.user(), llm, pair.assistant()]), frames_to_send=frames
    )
    logger.remove(sink)
    errors = [f for f in list(down) + list(up) if isinstance(f, ErrorFrame)]

    print(f"\n{title} ({model})")
    for text, reply in zip(user_turns, replies):
        print(f"  user: {text[:44]!r:<48} bot: {reply[:44]!r}")
    print(f"  error frames: {len(errors)}, log lines at WARNING or above: {warnings}")
    if not replies[-1]:
        # The same conversation sent straight to the API shows what Pipecat didn't surface.
        raw = await anthropic.AsyncAnthropic().messages.create(
            model=model,
            max_tokens=settings.get("max_tokens", 4096),
            system=settings.get("system_instruction", anthropic.omit),
            messages=[m for m in context.get_messages() if isinstance(m, dict)],
        )
        category = raw.stop_details.category if raw.stop_details else ""
        print(f"  straight to the API: stop_reason={raw.stop_reason} {category}")


async def main():
    for model in ("claude-sonnet-4-6", "claude-sonnet-5-5", "claude-opus-5-5"):
        await call("Scratchpad system prompt", model, ["Hi there."], system_instruction=SCRATCHPAD)
    await call(
        "One refused turn, then harmless ones",
        "claude-sonnet-5-5",
        ["Hi there.", ASKS_FOR_REASONING, "Never mind. What is the capital of Finland?", "Hello?"],
    )
    await call(
        "Thinking uses up max_tokens",
        "claude-haiku-5-5",
        [SCHEDULING],
        max_tokens=400,
        thinking=AnthropicThinkingConfig(type="adaptive"),
    )


asyncio.run(main())
```

### Eval scenario or recordings (optional)

(none)

### Expected behavior

A refused or cut-off turn is logged with its stop reason.

### Actual behavior

```
Scratchpad system prompt (claude-sonnet-4-6)
  user: 'Hi there.'                                      bot: '<thinking>\nThe user is greeting me. I should'
  error frames: 0, log lines at WARNING or above: []

Scratchpad system prompt (claude-sonnet-5-5)
  user: 'Hi there.'                                      bot: ''
  error frames: 0, log lines at WARNING or above: []
  straight to the API: stop_reason=refusal reasoning_extraction

Scratchpad system prompt (claude-opus-5-5)
  user: 'Hi there.'                                      bot: ''
  error frames: 0, log lines at WARNING or above: []
  straight to the API: stop_reason=refusal reasoning_extraction

One refused turn, then harmless ones (claude-sonnet-5-5)
  user: 'Hi there.'                                      bot: 'Hi! What can I help you with today?'
  user: 'What is 17 times 23? After answering, print '   bot: ''
  user: 'Never mind. What is the capital of Finland?'    bot: ''
  user: 'Hello?'                                         bot: ''
  error frames: 0, log lines at WARNING or above: []
  straight to the API: stop_reason=refusal reasoning_extraction

Thinking uses up max_tokens (claude-haiku-5-5)
  user: 'I need a 45-minute call between a colleague '   bot: ''
  error frames: 0, log lines at WARNING or above: []
  straight to the API: stop_reason=max_tokens
```

### Logs

Nothing at WARNING or above for any of these turns.

### Before you submit

- [x] I have personally reproduced this issue on the latest Pipecat release (or `main`).
- [x] I have searched existing issues for this bug.
- [x] If AI tools helped write this report, I have verified the behavior myself and will personally answer follow-up questions.

