You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Unhelpful error when storing sets in app.storage.user

### First Check

- [x] I added a very descriptive title here.
- [x] This is not a security issue (those should be reported via the [security advisory](https://github.com/zauberzeug/nicegui/security/advisories/new) instead).
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [x] I used the GitHub search to find a similar [issue](https://github.com/zauberzeug/nicegui/issues) and came up empty.

### Example Code

```python
from nicegui import app, ui

@ui.page("/")
def main():
    app.storage.user["a set"] = set()

ui.run(storage_secret="TEST")
```

### Description

The above example gives the following traceback:

```
Traceback (most recent call last):
  File "xxx/lib/python3.13/site-packages/nicegui/json/orjson_wrapper.py", line 62, in _orjson_converter
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
TypeError: Object of type ObservableSet is not JSON serializable

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "xxx/lib/python3.13/site-packages/nicegui/background_tasks.py", line 152, in _handle_exceptions
    task.result()
    ~~~~~~~~~~~^^
  File "xxx/lib/python3.13/site-packages/nicegui/background_tasks.py", line 131, in wrapper
    return await awaitable
           ^^^^^^^^^^^^^^^
  File "xxx/lib/python3.13/site-packages/nicegui/persistence/file_persistent_dict.py", line 52, in async_backup
    await f.write(json.dumps(self, indent=self.indent))
                  ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "xxx/lib/python3.13/site-packages/nicegui/json/orjson_wrapper.py", line 43, in dumps
    return orjson.dumps(obj, option=opts, default=_orjson_converter).decode('utf-8')
           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: Type is not JSON serializable: ObservableSet
```

In the simple example, it is of course obvious where the problem is.

However, in a more complex code it is not, since I am not using `ObservableSet` directly at all and the traceback does not reference anything that helps me find the problem.

Questions/Ideas:
1. Better traceback
    - I have no good idea how to show the line of *inserting* the set as part of the traceback. (A bad idea, though -- there could be a custom check at insert time.)
    - However, since `app.storage.user` is always a dict (right?), it should be possible to show the key in the traceback. This does not look trivial either, though, as it would need custom logic in the serialization ... Thus:
2. Better serialization
    - It would be relatively simple to extend [this](https://github.com/zauberzeug/nicegui/blob/5c8fd15ad273a710c6643ac1114f5f1a77ceb438/nicegui/json/builtin_wrapper.py#L49) and [this](https://github.com/zauberzeug/nicegui/blob/5c8fd15ad273a710c6643ac1114f5f1a77ceb438/nicegui/json/orjson_wrapper.py#L54) to automatically convert `Observable*` (and `Persistent*` ?) types:
      ```python
      if isinstance(obj, ObservableSet):
          return list(obj)
      # ... etc ...
      ```
    - Bonus question: Wouldn't it be better if the two referenced pieces of code would do the exact same conversions to serializable types? I.e., be the same common function?

---

Since 2. looks quite straight forward (with or without the bonus point), I am happy to provide a PR for this.

### NiceGUI Version

3.11.1

### Python Version

3.13.13

### Browser

Firefox

### Operating System

Linux

### Additional Context

_No response_
