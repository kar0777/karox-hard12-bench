You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

QueryExpander returns duplicate generated queries

**Describe the bug**

`QueryExpander` can return duplicate queries when the chat generator repeats an expansion. It only checks whether the original query is already present; duplicates among the generated expansions are preserved.

This is especially visible when the component feeds `MultiQueryTextRetriever` or `MultiQueryEmbeddingRetriever`: each duplicate entry triggers another retrieval for the same query, adding latency and backend load while reducing the effective number of distinct expansions.

I reproduced this on the current `main` commit `bfb7a2896a393f031ccc7669b6923a32ca27918d`.

**Error message**

No exception is raised. The output contains duplicate query strings:

```text
{'queries': ['same query', 'same query', 'other query']}
```

**Expected behavior**

The output should contain each generated query once while preserving first-seen order. The original query should also appear at most once when `include_original_query=True`.

For the reproduction below, the expected result is:

```text
{'queries': ['same query', 'other query']}
```

**Additional context**

The sync and async paths contain the same post-processing logic, so both are affected. The existing `test_run_query_deduplication` test only covers a generated expansion matching the original query, not duplicates among generated expansions.

I searched existing open and closed issues and pull requests for `QueryExpander`, `duplicate query`, and `query expansion duplicates` and did not find a report or implementation covering this case.

If the maintainers confirm this behavior should be fixed and mark it open for external contribution, I would be happy to add an order-preserving regression fix for both sync and async execution paths.

**To Reproduce**

```python
import json

from haystack.components.generators.chat import MockChatGenerator
from haystack.components.query import QueryExpander

payload = json.dumps(
    {"queries": ["same query", "same query", "other query"]}
)
expander = QueryExpander(
    chat_generator=MockChatGenerator(payload),
    n_expansions=3,
    include_original_query=False,
)

print(expander.run("topic"))
```

Run with:

```console
hatch -e test run python reproduce.py
```

The same duplicate list is returned by `await expander.run_async("topic")`.

**FAQ Check**
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: Microsoft Windows 11 Pro 10.0.26200 (build 26200)
- Python: 3.13.12
- Haystack version: `main` at `bfb7a2896a393f031ccc7669b6923a32ca27918d`
