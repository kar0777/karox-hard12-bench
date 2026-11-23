You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

toc + attr_list: valueless {: data-toc-label } crashes with TypeError (regression in 3.11.3)

A heading with a bare `data-toc-label` attribute crashes the toc extension:

```python
import markdown
markdown.markdown("# Hello {: data-toc-label }", extensions=["toc", "attr_list"])
```

```
  File "markdown/extensions/toc.py", line 124, in unescape
    return c.unescape(text)
  File "markdown/treeprocessors.py", line 470, in unescape
    return self.RE.sub(self._unescape, text)
TypeError: expected string or bytes-like object, got 'NoneType'
```

This works in 3.11.2 (it renders `<h1 id="hello">Hello</h1>`) and crashes in 3.11.3 and on current master.

It looks like the same root cause as #1705. Since #1501, `attr_list` stores a valueless attribute as `None`. #1705 fixed this for `id`, but `data-toc-label` is read the same way a few lines further down in `TocTreeprocessor.run()`:

```python
if 'data-toc-label' in el.attrib:
    data_toc_label = run_postprocessors(unescape(el.attrib['data-toc-label']), self.md)
```

so `unescape(None)` blows up.

I'd expect a valueless `data-toc-label` to be treated like a missing one: the heading text is used as the label and the attribute is removed, the same as #1705 did for a valueless `id`.

Versions: Markdown 3.11.3 and master (4177c1b), Python 3.14.2, Windows 11.

