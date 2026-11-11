You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Limit should define bound_symbols

```python
>>> Limit(x + y, y, 1).bound_symbols
Traceback (most recent call last):
  File "<python-input-6>", line 1, in <module>
    Limit(x + y, y, 1).bound_symbols
AttributeError: 'Limit' object has no attribute 'bound_symbols'
```
It behaves like it knows what the bound symbols are, however:
```python
def test_limit_bound_symbols():
    L = Limit(x + y, x, 0)
    assert L.bound_symbols == (x,)
    assert L.free_symbols == {y}

    L = Limit(x + y, x, z)
    assert L.bound_symbols == (x,)
    assert L.free_symbols == {y, z}
```

Maybe just add the following for its property:

```python
@property
def bound_symbols(self):
    return (self.args[1],)
```
