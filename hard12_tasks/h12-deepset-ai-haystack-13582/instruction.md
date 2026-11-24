You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: DocumentJoiner in distribution_based_rank_fusion mode turns every score of a list into NaN when one score is not finite

**Describe the bug**

`DocumentJoiner` with `join_mode="distribution_based_rank_fusion"` rescales the scores of each input list with the mean and the standard deviation of that list. Both statistics are computed from the raw scores, so a single score that is `NaN` or infinite makes `mean_score`, `std_dev` and `delta_score` non-finite, and the rescaled score of *every* Document in that list becomes `NaN`.

Nothing is logged and nothing is raised, so the run looks successful: a list of four ordered scores goes in, four `NaN` scores come out.

```python
from haystack import Document
from haystack.components.joiners import DocumentJoiner

docs = [
    Document(content="a", score=0.9),
    Document(content="b", score=0.5),
    Document(content="c", score=float("nan")),   # e.g. from a custom retriever
    Document(content="d", score=0.2),
]
out = DocumentJoiner(join_mode="distribution_based_rank_fusion").run([docs])["documents"]
print("joined :", [(d.content, d.score) for d in out])
print("kept   :", [d.content for d in out if d.score >= 0.5])
```

Actual output:

```text
joined : [('a', nan), ('b', nan), ('c', nan), ('d', nan)]
kept   : []
```

**Error message**

None. The failure is silent and only shows up in whatever consumes the scores next. `inf` and `-inf` reproduce it as well.

**Expected behavior**

A score that carries no ranking information is already handled by this mode: `score=None` is treated as `0`, and there is a test pinning that behavior (`test_run_with_distribution_based_rank_fusion_join_mode_with_none_score`). A non-finite score is the same kind of unusable value, so it should be treated the same way and leave the other Documents with meaningful rescaled scores:

```text
joined : [('a', 0.7457...), ('b', 0.5491...), ('d', 0.4017...), ('c', 0.3034...)]
kept   : ['a', 'b']
```

**Additional context**

- Neither `Document` nor `Document.from_dict` validates `score`, and `json.loads` accepts the `NaN`/`Infinity` literals, so a Document that came through a dump written by another tool can already carry a non-finite score.
- A custom retriever or reranker that emits a non-finite score is the more likely source. `InMemoryEmbeddingRetriever` is not one: a zero vector scores `0.0` there.
- This is the same class of defect as #13410 (non-finite `DocumentJoiner` *weights*) and #13508 (non-finite `MetaFieldRanker` weight), both fixed by rejecting the invalid value at construction time. Scores have no constructor to validate against, and raising in `run()` would break pipelines that may currently "run", so treating the value like the missing score this mode already handles looks like the smaller change.

**To Reproduce**

Run the snippet above; swap `float("nan")` for `float("inf")` or `float("-inf")` for the other two cases.

**FAQ Check**
- [ ] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: Windows 11
- Haystack version: 3.4.1 (same expression as `main` at `d9e7e70`)

