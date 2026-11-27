You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Pipeline.connect silently accepts `list[T] → T` for any T and drops all but the first element at runtime

**Describe the bug**
Pipeline.connect() accepts list[T] → T connections for any type T (e.g. list[Document] → Document) without raising or warning. At runtime only the first element of the list is forwarded to the receiver; the rest are silently dropped. The inline comment at haystack/core/type_utils.py:211 says the unwrap is for str and ChatMessage only, but no code enforces that, so connecting a retriever's list[Document] to a downstream component asking for a single Document looks like it works and silently loses N−1 documents on every run.

**Error message**
No error, no warning, no log line, that's the problem. The pipeline completes successfully and returns a structurally valid result.

**Expected behavior**
Pipeline.connect("producer.docs", "consumer.doc") where producer.docs: list[Document] and consumer.doc: Document should raise PipelineConnectError at connect time (same as it does today for, say, list[Document] → str). Silently dropping list elements should never be the default for arbitrary types.

**Additional context**
Looks like a regression from PR #10629, which replaced the explicit _contains_type(inner, str|ChatMessage) gate in _get_conversion_strategy with a generic _strict_types_are_compatible(inner, receiver) check (and left the "for str and ChatMessage only" comment in place). Existing tests in test/core/test_type_utils.py:954-1013 only cover the str / ChatMessage cases so the broadened behavior slipped past CI. Same path also applies to list[T] → Optional[T] via the Union-receiver branch at L185-L190.

**To Reproduce**
```python
from typing import List
from haystack import component, Pipeline
from haystack.dataclasses import Document

@component
class Producer:
    @component.output_types(docs=List[Document])
    def run(self):
        return {"docs": [Document(content="a"), Document(content="b"), Document(content="c")]}

@component
class Consumer:
    @component.output_types(out=Document)
    def run(self, doc: Document):
        return {"out": doc}

p = Pipeline()
p.add_component("producer", Producer())
p.add_component("consumer", Consumer())
p.connect("producer.docs", "consumer.doc")  # accepted without warning
print(p.run({}))
# {'consumer': {'out': Document(... content: 'a')}}  ← 'b' and 'c' silently dropped
```

**FAQ Check**
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: macOS 26.4.1
- Haystack version: 2.31.0-rc0 (also reproduces on main @ 12d6f687d)

