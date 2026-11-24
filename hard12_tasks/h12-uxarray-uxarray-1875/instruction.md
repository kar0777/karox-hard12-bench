You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

UxDataArray.isel() on edge-centered data crashes with confusing `KeyError: No variable named '_subgrid_edge_indices'...` if connectivity isn't populated

### Version

v2026.09.1

### How did you install UXarray?

Source

### What happened?

Calling `UxDataArray.isel(n_face=...)` or `.isel(n_node=...)` on edge-centered data crashes with a very confusing error (see title). I suspect this is related to the lines in `uxarray.grid.slice._slice_face_indices` commented as "Only slice edge dimension if we have the face edge connectivity", which hide the `ds["_subgrid_edge_indices"] = xr.DataArray(edge_indices, dims=["n_edge"])` inside a check of `if "face_edge_connectivity" in ds`, and when that check gives False it silently does something else instead of crashing or raising a warning.

This problem currently only affects `UxDataArray`, not also `UxDataset`, because `UxDataset` simply ignores the command to slice by anything (see #1713) in these cases.

### What did you expect to happen?

I expected a clearer error message telling me why I can't do this, or suggesting that I should call arr.uxgrid.face_edge_connectivity to populate the connectivity and then try again, or for the connectivity to just be automatically populated at this stage because it was required for an operation I was attempting (most/all other uxarray grid vars get populated automatically as soon as they are needed…).

### Can you provide a MCVE to repoduce the bug?

```python
import uxarray as ux
arr = ux.tutorial.open_dataset('quad-hexagon-random-edge')['random_data_edge']
arr.isel(n_face=0)  # crashes
arr.isel(n_node=0)  # crashes

# but, if running the following before calling isel():
arr.uxgrid.face_edge_connectivity

# then the isel() commands do not crash:
arr.isel(n_face=0)
arr.isel(n_node=0)
```
