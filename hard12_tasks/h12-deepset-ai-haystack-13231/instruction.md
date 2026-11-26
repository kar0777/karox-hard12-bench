You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

MetaFieldRanker ignores missing_meta="drop" when meta values can't be sorted

**Describe the bug**
`MetaFieldRanker` with `missing_meta="drop"` still returns documents that don't have the meta field, if the other documents have values that can't be sorted together.

**Error message**
No error. The ranker logs these warnings and then returns the document anyway:

```
... the Documents with IDs 3 don't have this meta key.
Because the parameter <missing_meta> is set to 'drop', these Documents will be removed from the list of retrieved Documents.

Tried to sort Documents with IDs 1,2, but got TypeError with the message: '<' not supported between instances of 'int' and 'str'
```

**Expected behavior**
Documents without the meta field are dropped. The example below should print `['1', '2']`.

**Additional context**
When sorting fails, `run()` returns `deduplicated_documents[:top_k]`, which includes the documents without the field:
https://github.com/deepset-ai/haystack/blob/6bd30ee0161eb222116bfdddac00856fde5907e0/haystack/components/rankers/meta_field.py#L315

This is not the case from #12952 (no document has the field), which is fixed. Here some documents have the field, but their values can't be sorted together.

**To Reproduce**

```python
from haystack import Document
from haystack.components.rankers import MetaFieldRanker

ranker = MetaFieldRanker(meta_field="rating", missing_meta="drop")
docs = [
    Document(id="1", meta={"rating": 1}),
    Document(id="2", meta={"rating": "x"}),
    Document(id="3"),
]
print([d.id for d in ranker.run(documents=docs)["documents"]])
# ['1', '2', '3']
```

**FAQ Check**
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: Windows 11
- Haystack version: main (3.4.0-rc0)

