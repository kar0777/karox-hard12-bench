You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Nullable ForeignKey with depth > 0 is not Optional, so a NULL relation fails response validation

**Describe the bug**
`create_schema(Model, depth=N)` / `ModelSchema` with `Meta.depth` for a `null=True` ForeignKey produces a field whose type is the bare nested schema, with only `default=None`. The default is used only when the attribute is missing. Here the attribute is present with the value `None`, so pydantic validates `None` against the nested schema and fails. The `fields_optional` argument is also ignored on this path (`get_schema_field` returns at `ninja/orm/fields.py:155-156` before `optional` is used).

Relevant code (permalinks at 40e28d4): [`ninja/orm/fields.py:155-156`](https://github.com/vitalik/django-ninja/blob/40e28d4ce0e939c1d015e271547946e61b17c43a/ninja/orm/fields.py#L155-L156) and [`ninja/orm/fields.py:234-252`](https://github.com/vitalik/django-ninja/blob/40e28d4ce0e939c1d015e271547946e61b17c43a/ninja/orm/fields.py#L234-L252) (`get_related_field_schema` sets `default = None` when `field.null` but never wraps the type in `Optional`).

Repro:
```python
class Pub(models.Model):
    name = models.CharField(max_length=5)
class Book(models.Model):
    title = models.CharField(max_length=5)
    pub = models.ForeignKey(Pub, null=True, on_delete=models.CASCADE)

S = create_schema(Book, fields=["id", "pub"], depth=1)
S.model_validate(Book(id=1, pub=None))
```
Output:
```
ValidationError: 1 validation error for Book
pub.name
  Field required [type=missing, input_value=<DjangoGetter: None>, input_type=DjangoGetter]
```
Expected: `pub=None`. A list endpoint containing a book that has no publisher returns a 500.

Suggested fix (a suggestion only): pass `optional` into `get_related_field_schema` and return `Optional[schema]` when the default is `None` (nullable field or optional). For many-to-many, whether to wrap `List[schema]` in `Optional` only when `optional` is set is a design choice for the maintainers.

**Versions (please complete the following information):**
 - Python version: 3.14.0
 - Django version: 6.1.1
 - Django-Ninja version: 1.7.1
 - Pydantic version: 2.13.5

