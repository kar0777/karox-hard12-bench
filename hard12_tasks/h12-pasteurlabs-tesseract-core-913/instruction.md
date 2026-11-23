You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

defaults set with `default_factory` breaks `jax_abstract_eval`

### Description

`create_abstract_eval_schema` (via `apply_function_to_model_tree`'s `default_func` hook) only converts an array field's default to a `ShapeDType` placeholder when the field uses `default=`. A field using `default_factory=` keeps its real (unconverted) default on the generated abstract model, even though the field's *type annotation* on that model is `ShapeDType`.

In `tesseract_core/runtime/schema_generation.py`:

```python
# apply_function_to_model_tree, inside _recurse_over_model_tree's BaseModel branch
if default_func is not None and field.default is not PydanticUndefined:
    new_field.default = default_func(field.annotation, field.default)
```

This only checks `field.default`, never `field.default_factory`. `create_abstract_eval_schema` passes `replace_array_default_with_shapedtype` as `default_func`:

```python
def replace_array_default_with_shapedtype(obj: Any, default: Any) -> Any:
    if not safe_issubclass(obj, PydanticArrayAnnotation):
        return default
    try:
        arr = TypeAdapter(obj).validate_python(default)
    except ValidationError:
        return default
    return ShapeDType(shape=arr.shape, dtype=str(arr.dtype))
```

For a `default_factory=`-based field, this function is never called, so `new_field` (built via `copy(field)`) keeps the original `default_factory` unchanged.

**Why it matters**

The abstract schema's whole contract is "same structure as the real schema, but every array field holds only shape/dtype, never real data" (so it's safe to validate against a tracer, serialize, compare, etc. without touching real values). A `default_factory`-based field silently breaks that contract for its own default: pydantic doesn't validate defaults by default, so nothing catches the `ShapeDType`-typed field actually holding a real array until something that assumes `ShapeDType` (e.g. code doing `.shape`/`.dtype` without checking `isinstance(x, ShapeDType)` first) hits it, or until `model_dump()`/similar inspects the value and gets a real array it doesn't expect.

Pydantic recommends `default_factory=` over `default=` for mutable or non-trivially-copyable defaults ([docs](https://docs.pydantic.dev/latest/concepts/fields/#default-values)), so this is a reasonable pattern to hit by accident, not just an edge case.

**Suggested fix**

Have the `field.default is not PydanticUndefined` check also account for `default_factory`, e.g. using `field.get_default(call_default_factory=True)` to get the effective default regardless of which mechanism declared it, before deciding whether to call `default_func`.

**Related (optional, happy to split into a separate request if preferred)**

`replace_array_default_with_shapedtype` itself — and the `TypeAdapter(obj).validate_python(default)` call inside it — is a nested closure inside `create_abstract_eval_schema`, not importable. We hit a case in tesseract-jax where we need the *real* validated default (not the `ShapeDType` placeholder) for a field omitted from a tracer-backed input, since a default is never itself a tracer and so is always safe to fully validate. We currently re-derive it with the same `TypeAdapter(field_info.annotation).validate_python(default)` call (using the cached `_type_adapter` helper, not a bare `TypeAdapter(...)`, to match the module's own performance guidance), which works but means re-deriving tesseract-core's own logic rather than calling it. If you'd find it useful to expose as a public (or at least module-level private) helper, we'd use it and get a loud `ImportError` instead of silent drift if it ever changes shape.

### Steps to reproduce

```python
import numpy as np
from pydantic import BaseModel, Field
from tesseract_core.runtime import Array, Float32
from tesseract_core.runtime.schema_generation import create_abstract_eval_schema

class InputSchema(BaseModel):
    s: Array[..., Float32] = Field(default_factory=lambda: np.float32(1.0))

class OutputSchema(BaseModel):
    y: Array[..., Float32]

AbstractInputSchema, _ = create_abstract_eval_schema(InputSchema, OutputSchema)
inst = AbstractInputSchema.model_validate({"inputs": {}})  # "s" omitted
print(inst.inputs.s, type(inst.inputs.s))
# -> 1.0 <class 'numpy.float32'>, not a ShapeDType
```

With `default=np.float32(1.0)` instead, `inst.inputs.s` is correctly `ShapeDType(shape=(), dtype='float32')`.

### Logs

```bash
1.0 <class 'numpy.float32'>, not a ShapeDType
```

### OS

Mac

### Tesseract version

1.15.0
