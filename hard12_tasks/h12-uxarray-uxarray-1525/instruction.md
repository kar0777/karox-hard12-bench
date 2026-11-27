You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Projected (Cartesian/meter) node coordinates are silently modulo-wrapped into [-180, 180]

# Projected (Cartesian / meter) node coordinates are silently modulo-wrapped into [-180, 180]

## Summary

When a UGRID mesh uses **projected coordinates** (e.g. `standard_name = projection_x_coordinate`, `units = m`) rather than geographic lon/lat, uxarray silently rewrites the node longitudes by applying a `[-180, 180]` longitude wrap. For a mesh with x-coordinates of ~1.5e6 m this corrupts the geometry beyond recovery, and it happens with no warning or error. Latitude is left untouched, so the result is also internally inconsistent (x mangled, y preserved).

This came up loading SCHISM unstructured ocean-model output (a Lake Ontario mesh in a Great Lakes Lambert/Albers projection, coordinates in meters). The file is valid UGRID — it just isn't on a sphere.

## Minimal reproducible example

```python
import numpy as np
import uxarray as ux

# Projected coordinates in meters (not degrees)
node_x = np.array([1_500_000.0, 1_500_100.0, 1_500_100.0, 1_500_000.0])
node_y = np.array([  800_000.0,   800_000.0,   800_100.0,   800_100.0])
face_node_connectivity = np.array([[0, 1, 2], [0, 2, 3]])

uxgrid = ux.Grid.from_topology(
    node_lon=node_x,
    node_lat=node_y,
    face_node_connectivity=face_node_connectivity,
    fill_value=-1,
)

print("input  node_x  :", node_x)
print("uxgrid node_lon:", uxgrid.node_lon.values)
print("input  node_y  :", node_y)
print("uxgrid node_lat:", uxgrid.node_lat.values)
```

Output:

```
input  node_x  : [1500000. 1500100. 1500100. 1500000.]
uxgrid node_lon: [-120.  -20.  -20. -120.]      # <-- silently wrapped
input  node_y  : [800000. 800000. 800100. 800100.]
uxgrid node_lat: [800000. 800000. 800100. 800100.]   # <-- left as-is
```

The same thing happens when reading a projected UGRID file via `ux.open_grid(...)`.

## Expected vs. actual

- **Expected:** either (a) projected/Cartesian coordinates are preserved as-is, or (b) a clear warning/error is raised when coordinates don't look like degrees. Ideally projected meshes are supported as planar/Cartesian.
- **Actual:** `node_lon` is silently transformed by `(lon + 180) % 360 - 180`; `node_lat` is untouched; no warning.

## Root cause

`_set_desired_longitude_range` in `uxarray/grid/coordinates.py` applies the wrap whenever `node_lon.max() > 180`, unconditionally — it never checks units or `standard_name`, and there is no latitude equivalent (hence the x-wrapped / y-preserved asymmetry):

```python
def _set_desired_longitude_range(uxgrid):
    """Sets the longitude range to [-180, 180] for all longitude variables."""
    with xr.set_options(keep_attrs=True):
        for lon_name in ["node_lon", "edge_lon", "face_lon"]:
            if lon_name in uxgrid._ds:
                da = uxgrid._ds[lon_name]
                if da.size == 0:
                    continue
                if da.max() > 180:
                    wrapped = (uxgrid._ds[lon_name] + 180) % 360 - 180
                    wrapped.name = da.name
                    uxgrid._ds[lon_name] = wrapped
```

## Impact

Any non-geographic UGRID mesh (projected coordinate systems, idealized/Cartesian model domains, regional ocean models in meters) is silently corrupted on load. Because no error is raised, downstream results (areas, point-in-cell search, interpolation, plots) are wrong without any indication. Concretely this blocks using SCHISM (and similar) projected unstructured output with uxarray.

## Suggested fixes (in rough order of preference)

1. **Respect CF metadata.** Skip the longitude wrap when the coordinate's `standard_name` is `projection_x_coordinate`/`projection_y_coordinate` or `units` is not degrees (e.g. `m`, `meters`). More generally, treat such grids as Cartesian/planar and populate `node_x`/`node_y` rather than `node_lon`/`node_lat`.
2. **First-class projected/Cartesian support** in `from_topology` / readers — e.g. a `coordinate_system="spherical"|"cartesian"` (or `latlon=False`) flag so users can declare planar meshes explicitly.
3. **At minimum, warn instead of silently mutating** when longitudes exceed the geographic range, and fix the lon/lat asymmetry so a mesh is never left half-transformed.

## Environment

- uxarray 2026.4.1
- xarray 2026.4.0
- numpy 2.4.6
- Python 3.12.12

