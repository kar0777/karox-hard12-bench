You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Optional nested schema param returns 422 instead of None when no fields are sent

**Describe the bug**
A schema-typed parameter with a `None` default, such as `f: Optional[F] = Query(None)`, always builds an empty nested dict for `f`, so a request that sends none of its fields is validated as `F()` instead of falling back to the default. The docs advertise `Filters | None = Query(None)` as the supported way to make a schema optional ([docs/docs/guide/query-params.md#L172](https://github.com/vitalik/django-ninja/blob/ea72a759451e4ae3e8b0fd702b489e95f9698107/docs/docs/guide/query-params.md#L172)). If `F` has a required field the request fails with 422, and if all fields are optional the handler receives `F(a=None)` instead of `None`.

Repro (Query only; I did not run Header or Form, which appear to share the same code path, unverified):
```python
from typing import Optional
from ninja import NinjaAPI, Schema, Query
from ninja.testing import TestClient

api = NinjaAPI()

class F(Schema):
    x: int

class G(Schema):
    a: Optional[int] = None

@api.get("/n")
def n(request, f: Optional[F] = Query(None)):
    return {"f": f.dict() if f else None}

@api.get("/g")
def g(request, f: Optional[G] = Query(None)):
    return {"f": f.dict() if f else None}

c = TestClient(api)
print(c.get("/n").status_code, c.get("/n").json())
print(c.get("/g").status_code, c.get("/g").json())
```
Output:
```
422 {'detail': [{'type': 'missing', 'loc': ['query', 'x'], 'msg': 'Field required'}]}
200 {'f': {'a': None}}
```
Expected: `/n` returns 200 with `f` None, `/g` returns `f` None (the declared default).

Cause: `ParamModel._map_data_path` ([ninja/params/models.py#L79-L84](https://github.com/vitalik/django-ninja/blob/ea72a759451e4ae3e8b0fd702b489e95f9698107/ninja/params/models.py#L79-L84)) runs `current.setdefault(key, {})` for every nested path before it checks `if value is not None`, so the intermediate dict exists even when nothing was sent.

Suggested fix (just a suggestion): only create intermediate dicts when the value is not None, i.e. move the `value is None` return above the `setdefault` loop, so the field default applies when nothing was sent. Note this would change the 422 error `loc` for a required schema `Query(...)` with no fields sent, from `['query', 'x']` to `['query', 'f']`, so existing tests may need updating.

**Versions (please complete the following information):**
 - Python version: 3.14
 - Django version: 6.1.1
 - Django-Ninja version: 1.7.1
 - Pydantic version: 2.13.5

