You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

LLMMetadataExtractor fails documents whose extracted metadata contains an "error" key

**Describe the bug**

`LLMMetadataExtractor` treats any parsed metadata dict containing an `"error"` key as a failed extraction, even when `"error"` is a legitimate extracted field - including when the user declared it in `expected_keys`.

**To Reproduce**

```python
from haystack.components.extractors.llm_metadata_extractor import LLMMetadataExtractor
from haystack.components.generators.chat.mock import MockChatGenerator
from haystack.dataclasses import Document

extractor = LLMMetadataExtractor(
    prompt="Extract the error type and severity from this log: {{document.content}}",
    expected_keys=["error", "severity"],
    chat_generator=MockChatGenerator(responses=['{"error": "timeout", "severity": "high"}']),
)
result = extractor.run(documents=[Document(content="2026-09-10 ERROR timeout after 30s")])
```

**Actual behavior**

```python
result["documents"] == []
result["failed_documents"][0].meta["metadata_extraction_error"] == "timeout"  # the extracted value!
```

**Expected behavior**

The document lands in `result["documents"]` with `meta == {"error": "timeout", "severity": "high"}`.

**Root cause**

`_extract_metadata` signals parse failure by returning `{"error": <message>}`, and `_process_results` checks `if "error" in parsed_metadata`. A successful extraction whose JSON legitimately contains an `"error"` key is indistinguishable from the failure sentinel. Extracting error/severity fields from logs is a natural use of this component, so the collision is plausible in real pipelines.

**Proposed fix**

Raise an internal exception on parse failure instead of returning a sentinel dict. I have this implemented with regression tests; PR to follow.

**System:** haystack main (post-2.18), Python 3.10
