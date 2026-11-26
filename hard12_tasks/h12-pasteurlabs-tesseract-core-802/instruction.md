You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Convert cuda_ipc inputs to framework arrays in the JAX and PyTorch recipes

### Summary

Add helpers to `tesseract_core.runtime.jax_recipes` that convert endpoint inputs to JAX arrays, without a copy where one isn't needed:

- `as_jax_array(x)` converts a single array.
- `as_jax_arrays(tree)` converts every array leaf in a pytree, such as `inputs.model_dump()`, and leaves other leaves alone.

Use `as_jax_arrays` inside the `jax_*` helpers on `inputs`, `tangent_vector` and `cotangent_vector`. Give the PyTorch template's `to_tensor` the same GPU branch.

### Why is this needed?

With `gpu_transport="cuda_ipc"`, GPU inputs reach endpoints as `IpcDeviceArray`. Neither recipe converts them to its framework's array type. The obvious `jnp.from_dlpack(x)` / `torch.from_dlpack(x)` fails for host inputs, because the runtime decodes those to read-only NumPy arrays and DLPack refuses to export them. So every Tesseract has to branch on where each input lives.

### Usage example

```python
from tesseract_core.runtime.cuda.ipc import is_gpu_array

def as_jax_array(x) -> jax.Array:
    if isinstance(x, jax.Array):
        return x
    if is_gpu_array(x):
        return jnp.from_dlpack(x)  # zero-copy
    return jnp.asarray(x)          # host input: one host-to-device copy

def as_jax_arrays(tree):
    is_array = lambda x: isinstance(x, np.ndarray | np.generic) or is_gpu_array(x)
    return jax.tree.map(lambda x: as_jax_array(x) if is_array(x) else x, tree)
```

In an endpoint written by hand:

```python
from tesseract_core.runtime.jax_recipes import as_jax_arrays

def apply(inputs: InputSchema) -> OutputSchema:
    x = as_jax_arrays(inputs.model_dump())
    return OutputSchema(c=x["a"] * 2 + x["b"])
```

Tesseracts built from `tesseract init --recipe jax` need no changes once the `jax_*` helpers call `as_jax_arrays` internally.

PyTorch template:

```python
def to_tensor(x):
    if is_gpu_array(x):
        return torch.from_dlpack(x)  # zero-copy
    if isinstance(x, np.generic | np.ndarray):
        return torch.tensor(x)
    return x
```

