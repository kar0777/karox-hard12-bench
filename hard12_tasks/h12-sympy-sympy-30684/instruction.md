You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Automatic int sympification doesn't work in newer jupyter versions?

Currently the code

```python
import sympy
from sympy.abc import*
from sympy import*
init_session(auto_int_to_Integer=True)
```

works fine in ipython. However, in `jupyter console`, it will raise the error (when run another cell)

```python
[IPKernelApp] ERROR | Exception in message handler:
Traceback (most recent call last):
  File "python3.9/site-packages/ipykernel/kernelbase.py", line 261, in dispatch_shell
    yield gen.maybe_future(handler(stream, idents, msg))
  File "python3.9/site-packages/tornado/gen.py", line 762, in run
    value = future.result()
  File "python3.9/site-packages/tornado/gen.py", line 769, in run
    yielded = self.gen.throw(*exc_info)  # type: ignore
  File "python3.9/site-packages/ipykernel/kernelbase.py", line 535, in execute_request
    reply_content = yield gen.maybe_future(
  File "python3.9/site-packages/tornado/gen.py", line 762, in run
    value = future.result()
  File "python3.9/site-packages/tornado/gen.py", line 234, in wrapper
    yielded = ctx_run(next, result)
  File "python3.9/site-packages/ipykernel/ipkernel.py", line 306, in do_execute
    if res.error_before_exec is not None:
AttributeError: 'NoneType' object has no attribute 'error_before_exec'
```

I think it's because of 

https://github.com/ipython/ipykernel/blob/b7783ddc4da43bd8f61ea5ef1d6b9e25dcabbfbd/ipykernel/zmqshell.py#L530

which occasionally returns a non-`None` value from the function.

In that case I think this line https://github.com/sympy/sympy/blob/dfef951e777dba36ad75162c8dc9402b228d11ed/sympy/interactive/session.py#L156 should be modified to return the return value of the `old_run_cell` function?
