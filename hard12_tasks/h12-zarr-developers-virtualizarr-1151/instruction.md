You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`to_virtual_dataset` eagerly loads `loadable_variables`

**Full disclosure:** This was discovered by Claude during development using Virtualizarr to fetch National Water Model data from GCS.

It looks like variables passed as `loadable_variables` to `ManifestStore.to_virtual_dataset` are loaded eagerly instead of being kept lazy.

This is because the `isinstance(var.data, ManifestArray)` check in `_warn_about_oversized_virtual_chunks` loads the entire array, whereas `var._data` avoids the read.

The fix would be to use `var._data` instead of `var.data` in `_warn_about_oversized_virtual_chunks`

Happy to open a PR if you agree

### Reproducer

```python
import numpy as np, xarray as xr
from obspec_utils.registry import ObjectStoreRegistry
from obstore.store import from_url
from virtualizarr.manifests import ManifestStore
from virtualizarr.parsers import HDFParser

path = "/tmp/vz_repro.nc"
xr.Dataset({"data": (("x",), np.arange(1000, dtype="int32"))}).to_netcdf(
    path, engine="h5netcdf", encoding={"data": {"chunksizes": (100,)}}
)

reads = []
orig = ManifestStore.get
async def counting(self, key, *a, **kw):
    if key.split("/")[-1].isdigit():
        reads.append(key)
    return await orig(self, key, *a, **kw)
ManifestStore.get = counting

registry = ObjectStoreRegistry({"file:///tmp/": from_url("file:///tmp/")})
store = HDFParser()(url=f"file://{path}", registry=registry)

ds = store.to_virtual_dataset(loadable_variables=["data"])
_ = ds["data"][:5].values
print(f"{len(reads)} of 10 chunks read")  # 10 on main, 1 with the fix
```
