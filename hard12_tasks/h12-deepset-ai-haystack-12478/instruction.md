You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

MarkdownHeaderSplitter loses the leading header when a secondary split runs on an unsplit document

**Describe the bug**

When `MarkdownHeaderSplitter` is configured with a `secondary_split` and `keep_headers=False`, the document's leading header line can be dropped from the output entirely — it appears neither in any chunk's content nor in any chunk's metadata.

`_apply_secondary_splitting` strips a leading header from each chunk:

https://github.com/deepset-ai/haystack/blob/main/haystack/components/preprocessors/markdown_header_splitter.py#L238-L244

```python
if not self.keep_headers:  # skip header extraction if keep_headers
    # extract header information
    header_match = re.match(self._header_pattern, doc.content)
    if header_match:
        content_for_splitting = doc.content[header_match.end() :]
```

For chunks produced by an actual header split this is a no-op: their content begins right after the header line (it starts with `\n`), so `re.match` never fires. The strip therefore only takes effect on the two fallback paths of `_split_text_by_markdown_headers`, which return the whole document as a single chunk with **empty** meta:

- "no headers found" (line ~146)
- "only headers with no content" (line ~208)

On those paths the header line is cut from the content, and because the meta has no `header` key to hold it, the text is simply lost. Note also that the strip matches any level 1–6 via `self._header_pattern`, ignoring `header_split_levels`.

**Expected behavior**

The header text should survive somewhere in the output — either in the chunk content or in the `header` metadata. Splitting a document should not silently discard part of it.

**To Reproduce**

Case 1 — the document's only header is at a level excluded from `header_split_levels`:

```python
from haystack import Document
from haystack.components.preprocessors import MarkdownHeaderSplitter

s = MarkdownHeaderSplitter(
    keep_headers=False, header_split_levels=[2], secondary_split="word", split_length=5
)
out = s.run(documents=[Document(content="# Title\nsome content here")])["documents"]
for d in out:
    print(repr(d.content), d.meta)
```

Actual:
```
'\nsome content here' {'source_id': '...', 'page_number': 1, 'split_id': 0, 'split_idx_start': 0}
```
`Title` is in neither the content nor the meta.

Expected: `'# Title\nsome content here'` (the document has no level-2 header, so it is returned unsplit and should be returned intact).

Case 2 — a document consisting only of headers:

```python
s = MarkdownHeaderSplitter(keep_headers=False, secondary_split="word", split_length=5)
out = s.run(documents=[Document(content="# Alpha\n# Beta")])["documents"]
for d in out:
    print(repr(d.content), d.meta)
```

Actual:
```
'\n# Beta' {'source_id': '...', 'page_number': 1, 'split_id': 0}
```
`# Alpha` is gone.

Expected: `'# Alpha\n# Beta'` — this path explicitly logs "returning original document", so the original document should come back unchanged.

**Additional context**

Chunks that really did come from a header split are unaffected and still behave correctly (header in `meta["header"]`, not in the content). The issue is limited to the unsplit-document fallbacks, where there is no metadata to preserve the header in.

This looks distinct from the previously fixed header-loss issues in this component (#11920 content before an embedded header, #12064 trailing header with no body, #11042 `parent_headers`), which all concern the header-split paths rather than the fallback returns.

**FAQ Check**
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

**System:**
- OS: macOS (Darwin 25.3.0)
- Haystack version: 3.2.0rc0 (reproduced on `main` @ 15ec337)

