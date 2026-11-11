You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

iWork: a date cell outside datetime's range crashes the whole Numbers conversion

A Numbers document holding one absurd date value crashes the entire conversion with an unhandled `OverflowError` instead of producing a document. `MAX_TABLE_CELLS` in the same module documents that corrupt or hostile documents are expected input for this backend, and `moment()` in `numbers_content.py` already guards this exact failure — but `format_date` and `format_duration` next to it do not.

### Reproduction (main @ 9051777)

Take `tests/data/numbers/sources/numbers_iwork09.numbers` and change one date attribute in its `index.xml` from `cell-date="276048000"` to `cell-date="1e308"` (or `"nan"`), then convert:

```python
in_doc = InputDocument(path_or_stream=evil, format=InputFormat.IWORK_NUMBERS,
                       backend=IWorkNumbersDocumentBackend, filename="evil.numbers")
in_doc._backend.convert()
```

```
OverflowError: Python int too large to convert to C int
```

With `"nan"` it is a `ValueError` from `timedelta` instead. Neither is a `DocumentLoadError`, so a pipeline converting a batch of documents dies on the one bad file.

### Where

- `numbers_xml.py` `cell_text`/`formula_text`: `float_attr` accepts any float the XML carries (`1e308`, `inf`, `nan`) and hands it to `format_date`.
- `numbers_content.py` `format_date`/`format_duration`: feed the value straight to `timedelta`, which raises `OverflowError` past ~2.7e11 seconds and `ValueError` on NaN.
- `numbers_iwa.py` `render`: `float(decoded.number)` overflows first when the cell carries a decimal128 whose exponent no double can hold (`Decimal("1E+6100")`), before the formatter is even reached.

### Expected

The affected cell comes out empty — the same "yields nothing rather than misread bytes" behavior the cell reader already follows — and every other cell survives.

PR incoming.
