You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Malformed (but base64-valid) CursorPagination cursor returns 500 instead of 422

**Describe the bug**
`Cursor.from_encoded_param` only converts base64 decode errors to ninja's `ValidationError`: https://github.com/vitalik/django-ninja/blob/40e28d4ce0e939c1d015e271547946e61b17c43a/ninja/pagination.py#L285-L301

`cls.model_validate(...)` then raises a raw `pydantic.ValidationError`. Also, `_find_position` ([L458-L467](https://github.com/vitalik/django-ninja/blob/40e28d4ce0e939c1d015e271547946e61b17c43a/ninja/pagination.py#L458-L467)) passes the raw `p` string to `queryset.filter()`, which can raise Django's `ValidationError` / `ValueError`. Neither is mapped to an HTTP error, so a real server answers 500. The existing tests only cover `cursor=invalid`, which fails at the base64 step.

Minimal repro API (model `E` with `d = DateField()`, schema `S` with `d: date`):
```python
@api.get("/c", response=List[S])
@paginate(CursorPagination, ordering=("d",), page_size=100)
def c(request):
    return E.objects.all()
```
Requests (the cursor value is the base64 of the quoted string):
```
GET /c?cursor=b64("o=abc")
  -> pydantic_core.ValidationError: 1 validation error for Cursor / o / Input should be a valid integer, unable to parse string as an integer
GET /c?cursor=b64("o=-1")      -> pydantic ValidationError (violates ge=0)
GET /c?cursor=b64("r=maybe")   -> pydantic ValidationError (not a bool)
GET /c?cursor=b64("o=100000")  -> pydantic ValidationError (violates lt=PAGINATION_MAX_OFFSET, default 100)
GET /c?cursor=b64("p=zzz")     -> django.core.exceptions.ValidationError: ['"zzz" value has an invalid date format. It must be in YYYY-MM-DD format.']
```
The `p=zzz` / Django `ValidationError` case applies when the ordering field is a `DateField`; other field types fail differently (or not at all) for a bad `p`.

I used `ninja.testing.TestClient`, which re-raises view exceptions; on a real server each of these is a 500.

Expected: 422 with `[{"cursor": "Invalid Cursor"}]`, as for `cursor=invalid`.

Suggested fix: wrap `model_validate` in `except pydantic.ValidationError as e: raise ValidationError([{"cursor": "Invalid Cursor"}]) from e`, and wrap the `_find_position` filter/evaluation (sync and async) in `except (DjangoValidationError, ValueError, TypeError)` raising the same error.

**Versions (please complete the following information):**
 - Python version: 3.13
 - Django version: 6.1.2
 - Django-Ninja version: 1.7.1
 - Pydantic version: 2.14.0

