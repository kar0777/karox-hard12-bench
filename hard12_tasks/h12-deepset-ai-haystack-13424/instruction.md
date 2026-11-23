You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Title: FaithfulnessEvaluator accepts mismatched statement and score counts as evaluated results

**Describe the bug**

`FaithfulnessEvaluator` accepts model replies containing different numbers of `statements` and `statement_scores`. It averages the returned scores and marks the row as `evaluated`, even when some extracted statements have no corresponding judgment.

For example, a reply with two statements and only `[1]` as scores produces an overall faithfulness score of `1.0`. Setting `raise_on_failure=True` does not reject the incomplete judgment.

**Error message**

No exception is raised for the missing-score example. The result contains:

```python
{
    "results": [{
        "statements": ["Python was created by Guido van Rossum.", "Python was first released in 1900."],
        "statement_scores": [1],
        "status": "evaluated",
        "score": 1.0,
    }],
    "meta": None,
    "score": 1.0,
    "individual_scores": [1.0],
}
```

**Expected behavior**

A judgment with mismatched counts should be recognized as malformed before aggregation. Could this follow the existing `raise_on_failure` policy: raise a helpful error when enabled, or mark the row as `error` and exclude it from aggregation when disabled?

An unscored statement should not automatically be treated as unsupported; the evaluator does not have a judgment for it. Valid aligned replies and the existing empty-list behavior should remain unchanged.

**Additional context**

This reproduction supplies a fixed synthetic model reply through a small chat generator. It does not call an external LLM or demonstrate the frequency of this reply shape in production. Parsing and scoring are performed by the real evaluator.

The same behavior occurs with `run`, `run_async`, `Pipeline.run`, and `Pipeline.run_async`, with either value of `raise_on_failure`.

Other count mismatches are also accepted: one statement with `[1, 0]` produces `0.5`; one statement with an empty scores list produces `NaN` while still reporting `evaluated`.

Related: #7973 and #11332 discuss evaluator failure reporting. This report concerns recognizing an incomplete statement-to-score mapping, rather than adding a new status API or changing the already implemented handling of JSON parsing failures.

**To Reproduce**

Run against the source revision listed below:

```python
import json

from haystack import component
from haystack.components.evaluators import FaithfulnessEvaluator
from haystack.dataclasses import ChatMessage


@component
class IncompleteJudgment:
    @component.output_types(replies=list[ChatMessage])
    def run(self, messages: list[ChatMessage]) -> dict[str, list[ChatMessage]]:
        reply = json.dumps({
            "statements": [
                "Python was created by Guido van Rossum.",
                "Python was first released in 1900.",
            ],
            "statement_scores": [1],
        })
        return {"replies": [ChatMessage.from_assistant(reply)]}


evaluator = FaithfulnessEvaluator(
    chat_generator=IncompleteJudgment(),
    raise_on_failure=True,
    progress_bar=False,
)
result = evaluator.run(
    questions=["Who created Python and when was it first released?"],
    contexts=[["Python was created by Guido van Rossum and first released in 1991."]],
    predicted_answers=["Python was created by Guido van Rossum and first released in 1900."],
)
print(result)
```

**FAQ Check**
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: macOS 26.6.2, Apple Silicon
- Python: CPython 3.12.15
- Haystack version: 3.5.0-rc0, editable checkout of `622967d7b6a878085a72ce9fb942bab0f485ad2f`
- Environment: repository Hatch `test` environment
