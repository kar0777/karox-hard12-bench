You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

DocumentSplitter can exceed split_length when carrying sentence overlap

**Describe the bug**

With `split_by="word"` and `respect_sentence_boundary=True`, `DocumentSplitter` can emit a chunk longer than `split_length` even though every sentence fits on its own. It carries a sentence from the previous chunk without accounting for the size of the next sentence.

**Error message**

No exception is raised.

**Expected behavior**

The constructor documents `split_length` as the [maximum number of units per split](https://github.com/deepset-ai/haystack/blob/4b4346b6d798338d9b43e70115006494012b1756/haystack/components/preprocessors/document_splitter.py#L87). In this example, the five-word sentence could be emitted on its own because carrying `Go.` would exceed the limit. Overlap would still be kept where it fits, and a single sentence that already exceeds the limit could still stay whole under the existing behavior. Can you confirm that this is the intended priority in sentence-boundary mode?

**Additional context**

The carry is selected in `_concatenate_sentences_based_on_word_amount` by calling `_number_of_sentences_to_keep`. The helper sees the previous chunk but has no budget for the next sentence. The problem persists with the overlap equality fix from #13522.

**To Reproduce**

```python
from haystack import Document
from haystack.components.preprocessors import DocumentSplitter

text = "Blue sky. Go. We walk into the woods."
for overlap in (1, 0):
    splitter = DocumentSplitter(
        split_by="word",
        respect_sentence_boundary=True,
        split_length=5,
        split_overlap=overlap,
    )
    chunks = splitter.run([Document(content=text)])["documents"]
    print(overlap, [(len(chunk.content.split()), chunk.content) for chunk in chunks])
```

```text
1 [(3, 'Blue sky. Go. '), (6, 'Go. We walk into the woods.')]
0 [(3, 'Blue sky. Go. '), (5, 'We walk into the woods.')]
```

**FAQ Check**

- [x] Have you had a look at the [Haystack FAQ](https://docs.haystack.deepset.ai/docs/faq)?

**System**

- Ubuntu 24.04.2 LTS, x86_64
- Haystack source from `main` at `4b4346b6d798338d9b43e70115006494012b1756` (checkout `VERSION.txt` is `3.6.0-rc0`)
- Python 3.12.14 and NLTK 3.10.4 with the English Punkt data

OpenAI Codex prepared and ran this reproduction.

