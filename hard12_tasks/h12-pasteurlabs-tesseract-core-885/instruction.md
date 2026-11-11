You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Runtime exports its whole sys.path as PYTHONPATH, breaking subprocesses that run a different Python

### Description

When the runtime loads `tesseract_api.py`, `load_module_from_path` (`tesseract_core/runtime/core.py`) writes the runtime's whole `sys.path` into the process environment:

```python
os.environ["PYTHONPATH"] = os.pathsep.join(sys.path)
```

Every subprocess started from `tesseract_api.py` inherits it. That includes the runtime venv's stdlib and `site-packages` directories. A child that runs the runtime's own interpreter isn't affected. But a Tesseract that shells out to a *different* Python imports the runtime's compiled packages instead of its own.

We hit this in Mosaic while wrapping DAFoam, which ships its own conda Python 3.12 with its own NumPy and petsc4py. Its driver script segfaulted on start-up inside the Tesseract, and ran fine when started from a plain shell in the same container. Removing `PYTHONPATH` from the subprocess environment fixed it.

The SDK already scrubs this variable for the same reason, in `local_client._runtime_env` and `venv_provision`, and the comments there note that importing a `tesseract_api.py` sets it. Code inside `tesseract_api.py` gets no such protection, and nothing tells the author the variable was set.

Expected: subprocesses see the environment the container was started with, plus whatever the runtime's own children need. A possible fix, which I haven't tested: export only the module directory, prepended to any existing `PYTHONPATH`. Children running the same interpreter find the venv's `site-packages` on their own. I believe that still covers the multiprocessing case from #356 / #488, but I haven't checked.

### Steps to reproduce

```yaml
# tesseract_config.yaml
name: pythonpath_repro
version: "0.0.1"
```

```python
# tesseract_api.py
import subprocess

from pydantic import BaseModel


class InputSchema(BaseModel):
    pass


class OutputSchema(BaseModel):
    child_pythonpath: str


def apply(inputs: InputSchema) -> OutputSchema:
    out = subprocess.run(
        ["sh", "-c", 'echo "$PYTHONPATH"'], capture_output=True, text=True
    ).stdout.strip()
    return OutputSchema(child_pythonpath=out)
```

```bash
$ tesseract build .
$ tesseract run pythonpath_repro apply '{"inputs": {}}'
```

### Logs

```
{"child_pythonpath":"/python-env/bin:/usr/lib/python311.zip:/usr/lib/python3.11:/usr/lib/python3.11/lib-dynload:/python-env/lib/python3.11/site-packages:/tesseract"}
```

With the DAFoam image, the foreign interpreter crashes on start-up:

```
qemu: uncaught target signal 11 (Segmentation fault) - core dumped
```

### OS

Linux (the container; observed on a macOS host)

### Tesseract version

1.15.0

