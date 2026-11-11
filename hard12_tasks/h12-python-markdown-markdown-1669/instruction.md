You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Unmatched backtick runs swallow text in 3.11 (inline code)

Since 3.11, a backtick string that has no closing string of the same length
causes the text that follows it to be dropped. In 3.10.3 the backticks are
output literally and no text is lost.

Input:

```
a ``` b ````` c
```

Actual output (3.11, 3.11.1, 3.11.2 and current master `b41e0aa`):

```html
<p>a <code></code> c</p>
```

Expected output (3.10.3):

```html
<p>a ``` b ````` c</p>
```

Two more inputs that show the same behavior (input, then 3.11.2 output, then
3.10.3 output):

~~~
`a`` b
<p><code></code> b</p>
<p>`a`` b</p>
~~~

~~~
```abc`````
<p><code>c</code></p>
<p>```abc`````</p>
~~~

In each case the text after the opening backticks is lost (`b`, `a` and `ab`
above), so the rendered document no longer contains content that is in the
source.

According to the [syntax rules] a code span is opened and closed by backtick
strings of equal length; a backtick string that is not matched should be
output literally, as 3.10.3 did.

I bisected this to 7be0cff (#1618, "Fix excessive backtracking when matching
inline code blocks"). Its parent bb50627 gives the expected output for all
three inputs and 7be0cff gives the output above. The later rewrite in 8a9ae23
(#1625) did not change the result.

To reproduce, run `markdown.markdown("a ``` b ````` c")` with no extensions.

[syntax rules]: https://daringfireball.net/projects/markdown/syntax#code

AI disclosure: I used Claude Code (Anthropic) to run the comparison across
versions, to bisect the regression to a commit, and to draft the text of
this issue. I checked the inputs and outputs above myself before submitting.
