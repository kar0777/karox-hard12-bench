You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Emphasis compatibility regression in 3.11.1 when punctuation precedes the closing delimiter

# Summary

After upgrading from Python-Markdown 3.11.0 to 3.11.1, emphasis is no longer rendered when its content ends with punctuation and the closing `**` is immediately followed by ordinary text.

I traced the behavior change to commit `6f825aa753d672ec2d8ec5bc7b70d14b919d2fe1` in #1632. I understand from the discussion there that the punctuation-aware delimiter rules were deliberately added. This report asks whether the resulting loss of compatibility is intended, and whether there is an acceptable way to preserve the earlier behavior.

# Minimal reproduction

```python
import markdown

print(markdown.markdown("**단어(설명)**입니다."))
```

Actual output in 3.11.1:

```html
<p>**단어(설명)**입니다.</p>
```

Expected output, matching 3.10.3 and 3.11.0:

```html
<p><strong>단어(설명)</strong>입니다.</p>
```

# Version comparison

The following results were reproduced with Python 3.14.0 using the source from each release tag and `master` at `2258b48e551d0df7b149ea9c33969bea7c7a0a2b`, without extensions.

| Input | 3.10.3 | 3.11.0 | 3.11.1 |
| --- | --- | --- | --- |
| `**단어(설명)**입니다.` | Strong | Strong | Literal |
| `**term(test)**suffix` | Strong | Strong | Literal |
| `**用語(test)**です` | Strong | Strong | Literal |
| `**术语(test)**是` | Strong | Strong | Literal |
| `**term(test)** suffix` | Strong | Strong | Strong |
| `**term**suffix` | Strong | Strong | Strong |

Here, “Strong” means the intended content is wrapped in `<strong>`, and “Literal” means the `**` markers remain in the output.

The issue is not specific to Korean or parentheses. For example:

```python
import markdown

print(markdown.markdown("**term.**suffix"))
print(markdown.markdown("**term。**suffix"))
print(markdown.markdown("**term😀**suffix"))
```

Actual output in 3.11.1:

```html
<p>**term.**suffix</p>
<p>**term。**suffix</p>
<p>**term😀**suffix</p>
```

Expected output, matching 3.11.0:

```html
<p><strong>term.</strong>suffix</p>
<p><strong>term。</strong>suffix</p>
<p><strong>term😀</strong>suffix</p>
```

# Impact

In Korean, grammatical particles and endings are normally attached directly to the preceding expression. Emphasizing a term with a parenthetical explanation therefore naturally produces input such as `**단어(설명)**입니다.`. Requiring a space at that boundary changes how the sentence is written.

Existing documents that rendered emphasis before the upgrade now display literal Markdown markers. Similar constructions can occur in other languages, as the examples above show.

# Questions

- Is the loss of emphasis in these previously supported constructions an intended compatibility change?
- Would you consider restoring the earlier behavior for these cases, or providing an opt-in compatibility setting or supported extension approach?
