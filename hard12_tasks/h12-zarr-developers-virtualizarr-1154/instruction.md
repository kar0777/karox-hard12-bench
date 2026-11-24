You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Sub-chunk slicing of an uncompressed ManifestArray ignores inlined chunks

### What happened

Slicing an uncompressed `ManifestArray` within a single chunk (the sub-chunk path added in #996) shifts the offset and length of each virtual chunk reference, but leaves inlined chunks untouched. The sliced array keeps the full inlined chunk bytes while its metadata describes the smaller chunk, so reading it fails:

```
ValueError: cannot reshape array of size 10 into shape (3,)
```

Inlined chunks are common for small coordinate variables, for example from kerchunk references or `HDFParser`.

### Minimal example

```python
import numpy as np
import zarr
from obspec_utils.registry import ObjectStoreRegistry

from virtualizarr.manifests import ChunkManifest, ManifestArray, ManifestGroup, ManifestStore
from virtualizarr.manifests.utils import create_v3_array_metadata

data = np.arange(10, dtype="<i4")
metadata = create_v3_array_metadata(shape=(10,), data_type=data.dtype, chunk_shape=(10,))
manifest = ChunkManifest(
    entries={"0": {"path": "", "offset": 0, "length": 40, "data": data.tobytes()}}
)
marr = ManifestArray(metadata=metadata, chunkmanifest=manifest)

sliced = marr[2:5]
print(sliced.shape)  # (3,)
print(len(sliced.manifest.dict()["0"]["data"]))  # 40, expected 12

store = ManifestStore(group=ManifestGroup(arrays={"a": sliced}), registry=ObjectStoreRegistry())
zarr.open_array(store, path="a", mode="r")[:]  # ValueError: cannot reshape array of size 10 into shape (3,)
```

### What you expected to happen

`[2 3 4]`, the same result as for a virtual chunk reference to the same bytes.

### Cause

`_shift_manifest_byte_ranges` in `virtualizarr/manifests/indexing.py` copies the inlined chunks unchanged. Inlined chunks of an uncompressed array hold raw bytes in the same layout, so they need the same `[offset_delta : offset_delta + new_length]` trim.

### Environment

VirtualiZarr `main` (cc44bae), zarr 3.4.2, xarray 2026.9.0, Python 3.12.
