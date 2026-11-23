You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

AutoMergingRetriever raises ValueError when a matched document has no parent (for example the root document)

**Describe the bug**

`AutoMergingRetriever.run()` and `run_async()` call `_check_valid_documents`, which requires every matched document to have a truthy `__parent_id` meta field. When the matched set includes a document without a parent, such as the root document of the hierarchy or a document from outside it, the retriever raises `ValueError: The matched leaf documents do not have the required meta field '__parent_id'` and the whole pipeline fails.

This contradicts the retriever's own merge logic: `_try_merge_level` explicitly keeps documents that have no parents ("keep docs that have no parents"). That branch is unreachable today because validation rejects those documents first.

**To Reproduce**

Uses only public APIs and an in-memory document store; no model or external service is needed.

```python
from haystack import Document
from haystack.components.preprocessors import HierarchicalDocumentSplitter
from haystack.components.retrievers.auto_merging_retriever import AutoMergingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore

text = "The sun rose early in the morning. It cast a warm glow over the trees. Birds began to sing."
doc = Document(content=text)
splitter = HierarchicalDocumentSplitter(block_sizes={10, 3}, split_overlap=0, split_by="word")
docs = splitter.run([doc])["documents"]

# one store holds every level, so a retriever can match the root chunk itself
store = InMemoryDocumentStore()
store.write_documents(docs)
leaves = [d for d in docs if not d.meta["__children_ids"]]
root = [d for d in docs if d.meta["__level"] == 0][0]

retriever = AutoMergingRetriever(store, threshold=0.5)
print(retriever.run(leaves[:2]))            # works
print(retriever.run(leaves[:2] + [root]))   # raises ValueError
```

Actual output:

```text
=== case 1: matched leaves only (baseline) ===
OK: [(2, 'The sun rose '), (2, 'early in the ')]
=== case 2: matched leaves + the root doc (one store holds every level) ===
ValueError: The matched leaf documents do not have the required meta field '__parent_id'
```

**Expected behavior**

Documents without `__parent_id` should pass through unchanged, as the existing pass-through branch in `_try_merge_level` intends, instead of failing the whole run.

**Additional context**

- In single-store setups the embedding retriever can legitimately return a parent or root chunk among the matches, so this input is realistic rather than off-contract.
- Distinct from #12943 and PR #12944: those fix merge ordering for leaves at different depths and do not touch `_check_valid_documents`.
- Proposed fix: drop the `__parent_id` truthiness requirement from `_check_valid_documents` and keep the `__level` / `__block_size` presence checks, so parentless documents reach the existing pass-through branch. If strict validation is preferred, the error should at least name the offending document. I can open a PR with tests if either direction sounds right.

**System**

- OS: Linux x86_64
- Python: 3.14.7
- Haystack: current `main` (3.3.0-rc0)
