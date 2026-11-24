You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Multipart Body str field with quotes or newlines returns 400, and backslash sequences are silently altered

**Describe the bug**
When a view mixes a `str = Body(...)` parameter with `Form`/`File` parameters (multipart), `_MultiPartBodyModel` wraps the raw form value as `f'"{data}"'` and feeds it to `json.loads` without JSON-escaping ([ninja/params/models.py#L183-L191](https://github.com/vitalik/django-ninja/blob/ea72a759451e4ae3e8b0fd702b489e95f9698107/ninja/params/models.py#L183-L191)). The wrap is skipped when the value starts or ends with a quote. As a result, any value with an inner quote, a newline, or a leading or trailing quote misbehaves: a value like `a"b` is wrapped and fails on the inner quote, `say "hi"` ends with a quote so it is not wrapped and fails `json.loads` as-is, `"quoted"` is JSON-decoded so the quotes are lost, and backslash sequences such as `a\nb` (backslash, n) are decoded into a different character.

Repro:
```python
from ninja import NinjaAPI, Body, Form
from ninja.testing import TestClient

api = NinjaAPI()

@api.post("/m")
def m(request, s: str = Body(...), f: str = Form("d")):
    return {"s": s}

c = TestClient(api)
for v in ['say "hi"', '5\'10"', '"quoted"', 'line1\nline2', 'a\\nb']:
    r = c.post("/m", data={"s": v, "f": "a"})
    print(repr(v), r.status_code, r.json())
```
Output observed on the versions below:
```
'say "hi"' 400 {'detail': 'Cannot parse request body (Expecting value: line 1 column 1 (char 0))'}
'5\'10"' 400 {'detail': 'Cannot parse request body (Extra data: line 1 column 2 (char 1))'}
'"quoted"' 200 {'s': 'quoted'}
'line1\nline2' 400 {'detail': 'Cannot parse request body (Invalid control character at: line 1 column 7 (char 6))'}
'a\\nb' 200 {'s': 'a\nb'}
```
Expected: every string is passed through unchanged. Related: #1735 fixed the empty-string IndexError in the same branch but kept the quote-wrapping.

Suggested fix (just a suggestion): for `str` annotations use the raw form value, or `json.dumps(data)`, instead of hand-quoting.

**Versions (please complete the following information):**
 - Python version: 3.14
 - Django version: 6.1.1
 - Django-Ninja version: 1.7.1
 - Pydantic version: 2.13.5

