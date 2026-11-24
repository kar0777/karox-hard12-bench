You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

AsciiDoc: links in block titles stay as raw `url[text]` markup

### Bug

Since #5115, a link like `https://example.com[Docs]` in an AsciiDoc paragraph becomes link text with a hyperlink. The same link in a block title (`.Title ...`) is not parsed. The title is added as text with the raw `https://example.com[Docs]` markup and no hyperlink.

### Steps to reproduce

```python
import tempfile
from pathlib import Path

from docling.document_converter import DocumentConverter

SRC = """See https://example.com[Docs]

.Caption https://example.com[Docs]
Para after title.
"""

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "t.adoc"
    p.write_text(SRC)
    doc = DocumentConverter().convert(p).document

for t in doc.texts:
    print((t.text, str(t.hyperlink) if t.hyperlink else None))
```

Output on `main` (07154cd):

```
('See', None)
('Docs', 'https://example.com/')
('Caption https://example.com[Docs]', None)
('Para after title.', None)
```

The paragraph link becomes `Docs` with the hyperlink `https://example.com/`. The block title keeps `https://example.com[Docs]` as literal text.

Expected: the title doesn't keep the raw `url[text]` markup. I'd expect `Caption Docs`, with the link kept the way paragraphs keep it. A title is a single text item, so if a link inside it can't be represented, plain `Docs` would still be better than the raw markup. I didn't find docs saying titles keep the markup; if that's intended, feel free to close this.

### Docling version

`main` @ 07154cd (docling-slim 2.145.0). The 2.145.0 release predates #5115, so links in paragraphs are not parsed there either.

### Python version

Python 3.12.16, Linux (aarch64)

### Additional context

In `docling/backend/asciidoc_backend.py`, block title text is built with `" ".join(caption_data)` and passed straight to `doc.add_text`, without the inline parsing that `_flush_text_data` now does for paragraphs. My script reaches this in `_flush_caption_as_paragraph` (line 212). The same pattern is at line 348 (title before a list), line 656 (picture caption) and line 1122 (table caption). I read those three but did not run them.

I can send a PR that runs title and caption text through the same inline parsing, with tests for a title before a paragraph, an `image::` and a `|===` table.

