You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Custom Serializer doesn't work with top-level data.

It seems that custom serializers don't work if the custom data type is at the top level.

For example, suppose I implement a custom serializer for `MyClass`, and I wrap `MyClass` inside a dataclass `MyWrapper`.

When I call `serde.to_dict(MyWrapper(MyClass(...)))`, the custom serializer for `MyClass` works as expected.
When I call `serde.to_dict(MyClass(...))`, however, the custom serializer is not used.

This is unexpected; I would expect `serde.to_dict(MyClass(...))` to invoke the custom serializer too.

In the below example, the second assertion fails.

```python
# serde_partial.py

from plum import dispatch
import serde
from typing import Any
from dataclasses import dataclass


Type = type  # You should prefer to use type[...] instead of Type[...]!


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

class MySerializer:
    @dispatch
    def serialize(self, value: MyClass) -> dict[str, Any]:
        return {'a': value.a, 'b': value.b}

class MyDeserializer:
    @dispatch
    def deserialize(self, cls: Type[MyClass], value: dict[str, Any]) -> MyClass:
        return MyClass(value['a'], value['b'])


serde.add_serializer(MySerializer())
serde.add_deserializer(MyDeserializer())

@dataclass
class MyWrapper:
    value: MyClass

# When MyClass is wrapped inside a dataclass, to_dict and from_dict work correctly
obj = MyWrapper(MyClass(1, 2))
expected = {'value': {'a': 1, 'b': 2}}
result = serde.to_dict(obj)
assert isinstance(result, dict)
assert result == expected
assert serde.from_dict(MyWrapper, result) == obj

# When MyClass is not wrapped inside a dataclass, to_dict fails to serialize it
obj = MyClass(1, 2)
expected = {'a': 1, 'b': 2}
result = serde.to_dict(obj)
assert isinstance(result, dict), f"Expected dict, got {type(result)}"  # ASSERTION FAILS
```
```text
$ python serde_partial.py
Traceback (most recent call last):
  File "/home/homestar/tmp/serde_partial.py", line 49, in <module>
    assert isinstance(result, dict), f"Expected dict, got {type(result)}"  # ASSERTION FAILS
AssertionError: Expected dict, got <class '__main__.MyClass'>
```
