You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

BOM-detected text decode failures lose encoding diagnostics

### Bug

The BOM-detection branch of `docling.utils.text_decoding.decode_text` leaks `UnicodeDecodeError`, while the explicit-encoding and fallback branches raise `DocumentLoadError` with decoding context. Markdown, CSV and AsciiDoc catch that leaked error and replace it with a generic backend initialization message containing a file hash. The encoding diagnosis is then missing from the `ConversionError` cause users normally inspect.

### Steps to reproduce

```python
import codecs
from io import BytesIO
from docling.datamodel.base_models import DocumentStream, InputFormat
from docling.document_converter import DocumentConverter
from docling.exceptions import ConversionError

raw = codecs.BOM_UTF16_LE + b"A"  # truncated UTF-16 code unit
converter = DocumentConverter(allowed_formats=[InputFormat.CSV])
try:
    converter.convert(DocumentStream(name="bad.csv", stream=BytesIO(raw)))
except ConversionError as error:
    print(error.__cause__)
```

The cause says `CsvDocumentBackend could not load document with hash ...`; it does not identify UTF-16 or the truncated data. Calling `decode_text(BytesIO(raw))` directly raises `UnicodeDecodeError` instead of `DocumentLoadError`. UTF-8 BOM followed by an invalid byte, and truncated UTF-32, have the same problem.

Expected: wrap the BOM decoder error as `DocumentLoadError` naming its detected encoding and retain the `UnicodeDecodeError` as its cause. Do not retry a fallback codec after an authoritative BOM.

I prepared a small fix with direct decoder and converter regressions for file/stream inputs. This differs from #4846/#4849, which concern successful explicit UTF-8 decoding retaining a BOM.

### Docling version

Current main: `29caea8381e885872905dc9438f10014368a2a25` (`docling-slim` 2.141.0).

### Python version

Python 3.12.8, Windows. Reproduction and tests run locally with Codex assistance.

