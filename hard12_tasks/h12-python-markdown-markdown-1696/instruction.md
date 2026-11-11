You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Text lost after an unclosed *** (regression in 3.11.1)

Since 3.11.1, some emphasis sequences after an unclosed `***` drop characters from the output. 3.11 and earlier keep all the text.

```python
import markdown
markdown.markdown('***l* * **e**')
```

| version | output |
|---|---|
| 3.11 | `<p><strong><em>l</em> * </strong>e**</p>` |
| 3.11.1, 3.11.2, 3.11.3 | `<p>**<em>l</em> <strong>*</strong>**</p>` (the `e` is lost) |

The same happens across a line break (`'***l*\n* **e**'`). A case closer to real text:

```python
markdown.markdown('***Le souffle** : x\n* **Amor Fati** : rectiligne')
# 3.11.3: '<p>*<strong>Le souffle</strong> : x\n<strong>**Amor Fa</strong>** : rectiligne</p>'
```

Here `ti` is lost from "Amor Fati".

This comes from user content on a site that renders Markdown with Python-Markdown. In a sample of about 28,000 real documents, 2 fields lose text this way with 3.11.3. All the other emphasis differences we saw from 3.10.3 keep the text.

