You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

4 of 5 Document*Evaluators crash with ZeroDivisionError on empty input

## 4 of 5 `Document*Evaluator`s crash with `ZeroDivisionError` on empty input

### Bug

The 5 retrieval/answer evaluators in `haystack/components/evaluators/` aggregate per-question scores into one overall score with a mean. Four of them divide by `len(ground_truth_documents)` or `len(retrieved_documents)` without first checking that the list is non-empty, so an empty input raises `ZeroDivisionError: division by zero` instead of returning a clean `0.0` mean (or raising a helpful `ValueError`).

`DocumentNDCGEvaluator` already has its own empty-input guard (`document_ndcg.py:148`) — the other four do not.

Affected evaluators (all in `haystack/components/evaluators/`):

| Evaluator | File | Aggregation line |
| --- | --- | --- |
| `DocumentMAPEvaluator` | `document_map.py` | 144: `score = sum(individual_scores) / len(ground_truth_documents)` |
| `DocumentMRREvaluator` | `document_mrr.py` | 128: same shape |
| `DocumentRecallEvaluator` | `document_recall.py` | 186: `sum(scores) / len(retrieved_documents)` |
| `AnswerExactMatchEvaluator` | `answer_exact_match.py` | 67: `sum(matches) / len(predicted_answers)` |

`DocumentNDCGEvaluator` is already correct and is the model to follow.

### Reproduction

```python
from haystack import Document
from haystack.components.evaluators import (
    DocumentMAPEvaluator, DocumentMRREvaluator, DocumentNDCGEvaluator,
    DocumentRecallEvaluator, AnswerExactMatchEvaluator,
)

for name, ev, kwargs in [
    ("DocumentMAPEvaluator",       DocumentMAPEvaluator(),       {"ground_truth_documents": [], "retrieved_documents": []}),
    ("DocumentMRREvaluator",       DocumentMRREvaluator(),       {"ground_truth_documents": [], "retrieved_documents": []}),
    ("DocumentNDCGEvaluator",      DocumentNDCGEvaluator(),      {"ground_truth_documents": [], "retrieved_documents": []}),
    ("DocumentRecallEvaluator",    DocumentRecallEvaluator(),    {"ground_truth_documents": [], "retrieved_documents": []}),
    ("AnswerExactMatchEvaluator",  AnswerExactMatchEvaluator(),  {"ground_truth_answers":    [], "predicted_answers":    []}),
]:
    try:
        print(name, ev.run(**kwargs))
    except Exception as e:
        print(f"{name}: {type(e).__name__}: {e}")
```

Output on `main` (2.31.0):

```
DocumentMAPEvaluator:       ZeroDivisionError: division by zero
DocumentMRREvaluator:       ZeroDivisionError: division by zero
DocumentNDCGEvaluator:      ValueError: ground_truth_documents and retrieved_documents must be provided.
DocumentRecallEvaluator:    ZeroDivisionError: division by zero
AnswerExactMatchEvaluator:  ZeroDivisionError: division by zero
```

The per-question case (`[[]]` — one question with no documents) returns `0.0` for the retrieval evaluators and `1.0` for `AnswerExactMatchEvaluator` (one empty list, the answer is "matching" because both are missing). Only the top-level empty case breaks.

### Why this matters

- Evaluator components are commonly run inside pipelines that iterate over a dataset. A pipeline that filters down to zero questions (e.g. all filtered out) crashes instead of returning a clean `0.0` mean.
- The inconsistency with `DocumentNDCGEvaluator` (which has the right guard) is a footgun: users add a second evaluator to a pipeline, the pipeline's first run with a non-empty subset works, and a later run with an empty subset unexpectedly crashes only on the new evaluator.
- `ZeroDivisionError` is not a useful signal for a caller that already passed the explicit shape contract ("same-length lists"). The intent is clearly a "no questions" case, not a math error.

### Proposed fix

Mirror `DocumentNDCGEvaluator.validate_inputs` in each of the four evaluators. The recommended path is to **raise `ValueError`**, for the same reason `DocumentNDCGEvaluator` does: an empty list of questions is almost certainly a data-pipeline bug (filter dropped everything, wrong input path, etc.) and surfacing it is more useful than silently returning a clean `0.0` mean that downstream dashboards will average into unrelated scores. Returning `0.0` would also create a *new* inconsistency between four evaluators and the NDCG one; raising keeps all five behaviorally identical.

For the per-question `[[]]` case the existing semantics stay as they are (the four retrieval evaluators return `0.0`; `AnswerExactMatchEvaluator` returns `1.0` because two empty answers are treated as "matching" by the answer-comparison code). Only the top-level empty case needs the new guard.

### Acceptance criteria

- All 5 evaluators handle `ground_truth_documents=[]` (and equivalent for `AnswerExactMatchEvaluator`) without `ZeroDivisionError`.
- The behavior matches `DocumentNDCGEvaluator` — `ValueError` with a clear message naming the offending argument. (See *Proposed fix* for the rationale.)
- New unit tests cover the empty case for all four evaluators that lack it today.
- The mismatch between the `len(...) == 0` check and the score aggregation line is fixed in all four files in the same PR.

### Backward compatibility

Pure bug fix. No public API change. Pipelines that today crash on empty input will either get a `ValueError` (the loud-fail option) or a clean zero mean (the silent option). Either is strictly better than the current `ZeroDivisionError`.

### Risks

Low. The aggregation is a simple mean. A test pinning the exact error type/message should be added in case the maintainer chooses the "raise" path.

