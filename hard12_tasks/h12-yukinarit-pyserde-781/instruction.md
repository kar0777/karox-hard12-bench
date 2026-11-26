You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Custom coercer API

`coerce` is a very useful feature that allows common conversion from `tuple` to `list` or `int` to `float`. However, it can also bring other problems. For example, allowing `float` to `int` conversion can sometimes introduce confusion, because when a field is defined as an integer, inputs like `3.5` will be silently converted to `3`. Another example is `str` to `bool` which can convert `"false"` to `False`.

What I'm suggesting here is a custom coerce API. For example:

```python
def integer_only(
    owner: str | None, field: str, target: type[Any], value: Any
) -> Any:
    if target is int:
        if isinstance(value, bool) or not isinstance(value, int):
            location = f"{owner}.{field}" if owner else field
            raise TypeError(f"{location} must be an integer")
    return target(value)


@serde(type_check=coerce(coercer=integer_only))
class Config:
    count: int
```

I think this is a relatively small change. I will submit a PR if you are happy with this change.
