You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Request.from_curl() doesn't decode escapes in $'...' strings, and fails on \'

### Description

#5901 (fixing #5899) made `$'...'` strings parse by turning `$'` into a plain `'`. The backslash escapes inside them are never decoded, though. Chrome's "Copy as cURL (bash)" uses `$'...'` exactly when a value contains a single quote, a newline or another special character, so these cases are common:

- `\n`, `\t`, `\r` and `\\` end up in the body as a literal backslash plus a letter.
- `\'` (Chrome's escaping for an apostrophe) leaves the quotes unbalanced after normalization, so `shlex` raises.

### Steps to Reproduce

```python
>>> from scrapy import Request
>>> Request.from_curl(r"curl https://x.io/p --data-raw $'line1\nline2'").body
b'line1\\nline2'
>>> Request.from_curl(r"""curl https://x.io/p --data-raw $'{"name":"O\'Brien"}'""")
ValueError: No closing quotation
```

### Expected behavior

The same bytes bash passes to curl: `b'line1\nline2'` and `b'{"name":"O\'Brien"}'`.

### Actual behavior

There's a literal `\n` in the body, and the second command raises `ValueError: No closing quotation`.

### Reproduces how often

Always.

### Versions

Scrapy 2.19.0, and main at 00ca2a9.

### Additional context

The [bash ANSI-C quoting rules](https://www.gnu.org/software/bash/manual/html_node/ANSI_002dC-Quoting.html) are short: `\a \b \e \E \f \n \r \t \v \\ \' \" \?`, `\nnn` (octal), `\xHH`, `\uHHHH`, `\UHHHHHHHH` and `\cX`. `_normalize_curl_command()` could decode the contents of `$'...'` and re-quote the result safely for `shlex`, instead of only dropping the `$`.

