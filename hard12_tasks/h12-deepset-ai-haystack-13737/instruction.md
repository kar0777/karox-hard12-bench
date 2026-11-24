You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

SummarizationCompactor accepts a truncated (`length`) or filtered (`content_filter`) summary and replaces the conversation with it

**Describe the bug**

`SummarizationCompactor._apply_summary` only checks that the last reply has non-empty text and that the compacted conversation is smaller. It never looks at the reply's `finish_reason`. When the summary generator stops because of its output limit (`finish_reason="length"`) or a content filter (`"content_filter"`), the partial text is wrapped in `<conversation_summary>` and `CompactionHook` uses it to replace the original messages. Facts that the summary never got to are then silently lost for the rest of the run, and the Agent still returns `exit_reason="text"`.

The existing failure path (`_report_failure`, which keeps the previous history or raises if `raise_on_failure=True`) only handles exceptions. A reply that reports failure through `finish_reason` doesn't raise, so it skips that path. The feature PR #12296 explicitly suggests setting a generation length limit on the summary generator, so a truncated summary is an expected case.

**Error message**

None. The failure is silent.

**Expected behavior**

A summary reply whose `finish_reason` is `length` or `content_filter` should be treated as a failed compaction. It should go through the existing failure policy (keep the uncompacted history, or raise when `raise_on_failure=True`). Replies without a `finish_reason` should keep today's behavior.

**Additional context**

Root cause: [`summarization.py` L437–456](https://github.com/deepset-ai/haystack/blob/d768bb8fa815f0bb1ed39056327835c952cdedf8/haystack/hooks/compaction/summarization.py#L437-L456) reads `replies[-1].text` without checking `replies[-1].meta["finish_reason"]`. Then [`hooks.py` L260–264](https://github.com/deepset-ai/haystack/blob/d768bb8fa815f0bb1ed39056327835c952cdedf8/haystack/hooks/compaction/hooks.py#L260-L264) replaces the State messages. The sync and async paths share `_apply_summary`, so both are affected.

A 4-line check before the text is used (raise into the existing failure handling for `length` / `content_filter`) fixes the repro below, and the existing `test_summarization.py` tests still pass. I'd like to open a PR with sync/async and failure-policy tests plus a release note, if that's welcome.

Related but different: #13375 (sliding window removing another strategy's summary), #12984 (token counter cleanup).

AI disclosure: I used an AI assistant to help investigate this issue and draft parts of this report. I ran the reproduction myself and verified the results.

**To Reproduce**

Fully offline. `MockChatGenerator` returns a summary with an explicit `finish_reason`; the real `Agent`, `CompactionHook`, and `SummarizationCompactor` run normally.

```python
from haystack.components.agents import Agent
from haystack.components.generators.chat import MockChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.hooks.compaction import CompactionHook, SummarizationCompactor


def run(finish_reason, summary_text):
    original = ChatMessage.from_user(
        "The required delivery reference is ORDER-7319. " + "Detailed delivery history. " * 200
    )
    history = [
        ChatMessage.from_system("Retain the delivery reference for future tasks."),
        original,
        ChatMessage.from_assistant("I have recorded the delivery details."),
        ChatMessage.from_user("Continue with the delivery task."),
    ]
    summarizer = MockChatGenerator(
        response_fn=lambda messages: ChatMessage.from_assistant(summary_text, meta={"finish_reason": finish_reason})
    )
    agent = Agent(
        chat_generator=MockChatGenerator("Ready to continue."),
        hooks={"before_llm": [CompactionHook(compactor=SummarizationCompactor(chat_generator=summarizer),
                                             context_window=1000)]},
    )
    result = agent.run(history)
    kept = any("ORDER-7319" in (m.text or "") for m in result["messages"])
    print(f"{finish_reason:<15} reference kept={kept}  exit_reason={result['exit_reason']}")


run("stop", "The delivery reference is ORDER-7319.")   # control
run("length", "The delivery reference is")              # truncated summary
run("content_filter", "The delivery reference is")      # filtered summary
```

Output:

```text
stop            reference kept=True  exit_reason=text
length          reference kept=False  exit_reason=text
content_filter  reference kept=False  exit_reason=text
```

The summarizer is called once and does receive `ORDER-7319` in its prompt. The reference is lost only because the truncated summary is accepted.

**FAQ Check**
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: macOS
- Haystack version: 3.5.0 (also `main` at d768bb8fa)
