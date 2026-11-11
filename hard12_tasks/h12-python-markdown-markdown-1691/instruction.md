You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Strong with underscores not rendered when content has a word-initial underscore (regression in 3.11.1)

Hello, after rebuilding one of my Mkdocs sites that use Python-Markdown, I noticed some bold links broke (they worked OK before):

```md
- __[:material-language-markdown-outline: Python Markdown](https://python-markdown.github.io/){:target="_blank"}__: processador de Markdown per a Python.
```

<img width="424" height="538" alt="Image" src="https://github.com/user-attachments/assets/1738261c-03cf-4570-8159-25857abf939e" />

I asked a LLM to help me figure it out, and it pointed me here.
Below, I attach what the LLM figured out.

---

## Summary

Since 3.11.1, `__strong__` text is no longer rendered as strong when it contains a single underscore at the start of a word. Depending on the content, the delimiters are either left as literal text or rendered as nested `<em>` elements with a stray `_`.

A common way to hit this is a link with `{target="_blank"}` inside strong text, because emphasis is processed while the attribute list is still plain text.

The same text using `**` still renders as strong.

## Minimal reproduction

```python
import markdown

print(markdown.markdown('__foo _bar__'))
print(markdown.markdown('__[A](u){target="_blank"}__: x', extensions=['attr_list']))
```

Output on 3.11.2 and on `master` (`0bfd8c3e`):

```html
<p>_<em>foo <em>bar</em></em></p>
<p>__<a href="u" target="_blank">A</a>__: x</p>
```

Output on 3.10.3 and 3.11.0:

```html
<p><strong>foo _bar</strong></p>
<p><strong><a href="u" target="_blank">A</a></strong>: x</p>
```

## Version comparison

Reproduced with Python 3.14. Only the `attr_list` cases have an extension enabled.

| Input | 3.10.3 | 3.11.0 | 3.11.1 | 3.11.2 | `master` |
| --- | --- | --- | --- | --- | --- |
| `__foo _bar__` | Strong | Strong | Nested `<em>` | Nested `<em>` | Nested `<em>` |
| `__a _b__ c` | Strong | Strong | Nested `<em>` | Nested `<em>` | Nested `<em>` |
| `__a "_b" c__ d` | Strong | Strong | Nested `<em>` | Nested `<em>` | Nested `<em>` |
| `__[A](u){target="_blank"}__: x` | Strong | Strong | Literal `__` | Literal `__` | Literal `__` |
| `**[A](u){target="_blank"}**: x` | Strong | Strong | Strong | Strong | Strong |

## Expected behavior

I expected the output from 3.11.0 and earlier: the outer `__` pair renders as `<strong>`, and the unmatched `_` stays as literal text.

## Context

The version comparison points to the emphasis rewrite in #1632, which first shipped in 3.11.1. I did not bisect to the individual commit.

#1630 is related, as it covers underscores in `{target="_blank"}` affecting italic text. A comment there notes that emphasis runs before attribute lists, so underscores sometimes need escaping. Escaping does work here (`{target="\_blank"}`), and so does moving the strong markers inside the link (`[__A__](u){target="_blank"}`).

However, the `__foo _bar__` case involves no attribute list, and existing documents that rendered correctly through 3.11.0 change silently on upgrade. #1657 restored earlier behavior for a similar compatibility change, so I wanted to ask whether this one is intended.

I found this in a MkDocs-style documentation site, where a list of links in the form `__[Name](url){:target="_blank"}__: description` lost its bold formatting after a dependency update.

