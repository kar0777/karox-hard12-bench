You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

MarkdownHeaderSplitter treats headings inside longer closing fences as headers

## Problem

`MarkdownHeaderSplitter` excludes headers inside fenced code blocks only if the closing fence has exactly the same length as the opening fence. Markdown permits a closing fence of the same type with *at least* as many fence characters. With a longer valid closing fence, the splitter treats code comments as document headers and cuts the code block apart.

## Reproduction

On current `main`:

```python
from haystack import Document
from haystack.components.preprocessors import MarkdownHeaderSplitter

text = "# Intro\nBody\n````python\n# fake\n`````\n## Real\nEnd\n"
result = MarkdownHeaderSplitter().run(documents=[Document(content=text)])
print([doc.meta["header"] for doc in result["documents"]])
```

Actual: `['Intro', 'fake', 'Real']`. Expected: `['Intro', 'Real']`. I ran it twice with identical results. Replacing the five-backtick closer with a four-backtick closer gives the expected result. The same failure occurs with four opening tildes and five closing tildes.

The current `_code_block_pattern` uses a backreference to the opening fence, requiring equal lengths. The CommonMark rule is a closing fence of the same type with *at least* the opening length: https://spec.commonmark.org/0.31.2/#fenced-code-blocks .

## Suggested scope

Recognize longer closing fences when excluding code blocks from header matches, while keeping unrelated heading and secondary-split behavior unchanged. Regression tests should cover longer backtick and tilde closers, equal-length closers, and the real header after the block. This should not require a public API change. I did not find a matching open/closed issue or PR and can prepare a patch once the current Haystack PR queue clears.
