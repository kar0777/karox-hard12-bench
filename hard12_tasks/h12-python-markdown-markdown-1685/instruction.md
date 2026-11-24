You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Uncaught RecursionError (DoS) on deeply nested lists; blockquotes are guarded but lists are not

### Summary

`markdown.markdown()` raises an uncaught `RecursionError` on a deeply nested list. The input is small and plausible as user-submitted content, so any service that renders untrusted Markdown (comments, wikis, issue trackers) can be crashed by it. This is the same class as CVE-2025-69534 (#1534) — an uncaught exception reached while parsing untrusted input — with a different trigger.

### Reproduce

```pycon
>>> import markdown
>>> doc = "".join("  " * i + "- x\n" for i in range(600))   # ~6 KB, 600 nested bullets
>>> markdown.markdown(doc)
Traceback (most recent call last):
  ...
  File ".../markdown/blockprocessors.py", line 411, in run
    self.parser.parseBlocks(lst[-1], [item])
  File ".../markdown/blockprocessors.py", line 197, in run
    self.parser.parseBlocks(parent[-1], [block])
  ...
RecursionError: maximum recursion depth exceeded
```

It crashes from a depth of roughly 500 on CPython's default limit. Ordered lists (`1. x`) trigger it the same way. The recursion alternates between `OListProcessor.run` and `ListIndentProcessor.run`, one frame pair per level of indentation.

### Why this looks like a gap rather than an inherent limit

The project already has a mechanism for exactly this, and already applies it to the other block type that recurses per level — blockquotes:

```python
# markdown/blockprocessors.py, BlockQuoteProcessor
def test(self, parent, block):
    return bool(self.RE.search(block)) and not util.nearing_recursion_limit()
```

With that guard, a 2000-deep blockquote renders fine instead of crashing:

```pycon
>>> len(markdown.markdown(">" * 2000))   # guarded: no crash
14861
```

`#799` (the blockquote version of this report) was fixed this way. The list processors — `ListIndentProcessor`, `OListProcessor`, `UListProcessor` — all recurse through `parseBlocks`/`parseChunk` but none calls `nearing_recursion_limit()`, so the list path still overflows.

### A note for whoever fixes it

The obvious one-line change — adding `not util.nearing_recursion_limit()` to `ListIndentProcessor.test()` — does stop the `RecursionError`, but I found it then exposes a slow degraded path: a 2000-deep indented block takes many seconds rather than rendering promptly, where the blockquote guard degrades cleanly. So the list case seems to need a little more than copying the guard verbatim, which is why I am reporting it rather than sending a patch I am not confident in. Happy to help test a fix.

### Environment

- Python-Markdown `master` (3.11.x) and 3.11.2 on PyPI
- CPython 3.12, Ubuntu 24.04

### Severity

Denial of service: a small, plausible input (a few KB of nested list markers) crashes the parser with an uncaught exception, affecting any caller that renders untrusted Markdown.

