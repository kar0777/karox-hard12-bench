You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] OpenAPI schema generates invalid `examples` format for query parameters, breaking Swagger UI

**Describe the bug**

When using Pydantic's `examples` field on query parameters, Django Ninja copies the JSON Schema array format directly to the OpenAPI Parameter Object level. However, OpenAPI 3.1.0 requires `examples` at the Parameter Object level to be a map of Example Objects, not an array. This causes Swagger UI to fail with `TypeError: i.get is not a function` when rendering the parameters.

**Reproduction**

```python
from ninja import NinjaAPI, Query, FilterSchema, Field

api = NinjaAPI()


class MyFilters(FilterSchema):
    status: str | None = Field(
        None,
        description="Filter by status",
        examples=["active", "pending", "archived"],
    )


@api.get("/items")
def list_items(request, filters: Query[MyFilters]):
    return {"status": filters.status}


# Check the generated OpenAPI schema
schema = api.get_openapi_schema()
param = schema["paths"]["/api/items"]["get"]["parameters"][0]
print(param)
```

Actual Output

```json
{
  "in": "query",
  "name": "status",
  "schema": {
    "anyOf": [{"type": "string"}, {"type": "null"}],
    "examples": ["active", "pending", "archived"],
    "title": "Status"
  },
  "required": false,
  "examples": ["active", "pending", "archived"]
}
```

The `examples` at the parameter level is an array, which is invalid per OpenAPI 3.1.0 spec.

Expected Output

```json
{
  "in": "query",
  "name": "status",
  "schema": {
    "anyOf": [{"type": "string"}, {"type": "null"}],
    "examples": ["active", "pending", "archived"],
    "title": "Status"
  },
  "required": false,
  "examples": {
    "example0": {"value": "active"},
    "example1": {"value": "pending"},
    "example2": {"value": "archived"}
  }
}
```

The `examples` inside schema can remain an array (valid JSON Schema), but at the Parameter Object level it must be a map of Example Objects.

**Root Cause**

In [`ninja/openapi/schema.py`](https://github.com/vitalik/django-ninja/blob/d5d977636652e6a024f861ca43c5c91617eaeca0/ninja/openapi/schema.py#L192-L193), the `_extract_parameters` method copies examples directly without format conversion:

```python
if "examples" in p_schema:
    param["examples"] = p_schema["examples"]
```

**Suggested Fix**

Convert the array format to the OpenAPI map format when copying to the parameter level:

```python
if "examples" in p_schema:
    examples = p_schema["examples"]
    param["examples"] = (
        {f"example{i}": {"value": v} for i, v in enumerate(examples)}
        if isinstance(examples, list)
        else examples
    )
```

**References**

- <https://spec.openapis.org/oas/v3.1.0#parameter-object> - `examples` must be `Map[string, Example Object | Reference Object]`
- <https://json-schema.org/understanding-json-schema/reference/annotations#examples> - array format is valid here

**Versions (please complete the following information):**
 - Python version: 3.13.11
 - Django version: 5.2.9
 - Django-Ninja version: 1.5.1
 - Pydantic version: 2.12.5

