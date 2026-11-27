You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

bug: DocumentLanguageClassifier crashes with TypeError when Document has content=None

**Describe the bug**

`DocumentLanguageClassifier` crashes with a `TypeError` when a `Document` has `content=None`, even though `Document.content` is explicitly allowed to be `None` (e.g., blob-only documents). It should mark such documents as `unmatched` instead of raising.

**Error message**
No error is thrown to the user — `langdetect.detect(None)` raises a `TypeError` internally that propagates uncaught.

**To Reproduce**
```python
from haystack import Document
from haystack.components.classifiers import DocumentLanguageClassifier

classifier = DocumentLanguageClassifier()
classifier.run(documents=[Document(content=None)])
```

**Expected behavior**
The document should be classified as `unmatched` and a warning should be logged, consistent with existing behavior when language detection fails.

**Root Cause**
`_detect_language` passes `document.content` directly to `langdetect.detect()` without checking for `None` first. The existing `LangDetectException` handler does not catch `TypeError`.

**Fix**
Guard against `None` content before calling `langdetect.detect()`:
```python
if document.content is None:
    logger.warning(
        "Langdetect cannot detect the language of Document with id: {document_id}", document_id=document.id
    )
    return language
```

**Additional context**
Only affects documents with `content=None` (blob-only). Text documents are unaffected.

**FAQ Check**
- Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: any
- Haystack version: 2.30.0-rc0
- Component: `DocumentLanguageClassifier`

