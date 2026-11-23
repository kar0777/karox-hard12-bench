You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Bug: UxDataArray.from_xarray crashes for GEOS-CS face and node fields

### Version

Source `main` at `65e9c4a15c620865e5412c96dd8fbe2052ac788c`; Linux, Python 3.12.14, NumPy 2.5.4, xarray 2026.9.0.

### How did you install UXarray?

Source

### What happened?

`UxDataArray.from_xarray(da, uxgrid=grid)` raises `AttributeError: 'DataArray' object has no attribute 'data_vars'` for a GEOS-CS field. The equivalent `UxDataset.from_xarray(da.to_dataset(), uxgrid=grid)[da.name]` succeeds and preserves the values and Grid object.

This prevents converting an individually selected face- or node-centered field while reusing an existing GEOS-CS Grid. The same failure occurs for synthetic fields with an extra time dimension. The GEOS-CS branch in `_map_dims_to_ugrid` assumes Dataset input, although the public DataArray constructor calls it directly.

This is a separate follow-up to the DataArray observation in [#1828](https://github.com/UXARRAY/uxarray/issues/1828#issuecomment-6318355311), not an expansion of #1834. Applying #1834's exact mapping helper fixes the structured y/x and x/y DataArray cases I checked, but leaves these GEOS-CS failures unchanged. That comparison used the exact helper on current main, not a full checkout/test of every #1834 file.

The following uses only synthetic geometry and values, with no downloads. It represents six independent quadrilateral tiles for exercising the GEOS-CS format/conversion path, not a scientific global-grid validation.

The node-centered variant uses shape `(2, 6, 2, 2)` and dimensions `("time", "nf", "YCdim", "XCdim")`; its Dataset workaround maps to `(time, n_node)`, while the direct DataArray call raises the same error.

### Proposed scope / coordination

I would like to handle the GEOS-CS DataArray path, its constructor docstring, and focused synthetic regressions for face/node data, dimension permutations, name/metadata preservation and lazy data, without changing Dataset behavior or the structured-grid work in #1834. Please assign this issue to me if that scope is appropriate. No implementation or PR for this follow-up has been submitted.

AI assistance: OpenAI Codex for analysis, synthetic reproduction and drafting. The reproduction was executed locally in the isolated cloud environment; no full-suite or real GEOS production-data validation is claimed here.

### What did you expect to happen?

The DataArray constructor should preserve name, attributes, non-spatial coordinates and laziness while mapping the GEOS-CS spatial dimensions to `n_face` or `n_node` in the supplied Grid's order. The Dataset wrapper works for the coordinate-light examples below; its broader coordinate behavior is outside this report. This report concerns the direct constructor failure, not data corruption.

### Can you provide a MCVE to repoduce the bug?

```python
import numpy as np
import xarray as xr
import uxarray as ux

lon = np.array([
    [[x, x + 10], [x, x + 10]]
    for x in [-150, -90, -30, 30, 90, 150]
], dtype=float)
lat = np.tile([[-10., -10.], [10., 10.]], (6, 1, 1))
mesh = xr.Dataset({
    "corner_lons": (("nf", "YCdim", "XCdim"), lon),
    "corner_lats": (("nf", "YCdim", "XCdim"), lat),
})
grid = ux.Grid.from_dataset(mesh)
assert grid.source_grid_spec == "GEOS-CS"

da = xr.DataArray(
    np.arange(12.).reshape(2, 6, 1, 1),
    dims=("time", "nf", "Ydim", "Xdim"),
    name="signal", attrs={"units": "synthetic"},
)
workaround = ux.UxDataset.from_xarray(da.to_dataset(), uxgrid=grid)["signal"]
assert workaround.dims == ("time", "n_face")
np.testing.assert_array_equal(workaround.values, np.arange(12.).reshape(2, 6))
assert workaround.uxgrid is grid

ux.UxDataArray.from_xarray(da, uxgrid=grid)  # AttributeError: data_vars
```
