You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

LLMContextSummarizer: messages_since_summary never resets and counts the injected summary message

## Problem

In `LLMContextSummarizer._should_summarize()` (`src/pipecat/processors/aggregators/llm_context_summarizer.py:232` on current main), the message-count trigger uses:

```python
messages_since_summary = len(self._context.messages) - 1
```

The `-1` is a static stand-in for "subtract the system message", not a real since-last-summary counter. Nothing in the class stores a marker of when the last summary was applied, so:

- The counter never resets after a summarization. `max_unsummarized_messages` effectively means "total context length minus one", not "messages since the last summary".
- After `_apply_summary()` the context is `[system?] + [summary] + recent`, so the injected summary message is counted as a conversation message. With a system prompt and `min_messages_after_summary=4`, the count reads 5 right after a summary even though only 4 conversation messages remain.
- When `messages[0]` is not a system message, the pre-first-summary count is under by one instead.

## Suggested fix

Track real state: record the message count (or index) when a summary is applied in `_apply_summary()`, reset it there, and compute messages-since-summary against that marker. Exclude the preserved system message and the injected summary message from the count.

## Context

Found while fixing the related token-trigger bug (system prompt counted toward `max_context_tokens`); that fix is intentionally kept separate. See the linked PR.
