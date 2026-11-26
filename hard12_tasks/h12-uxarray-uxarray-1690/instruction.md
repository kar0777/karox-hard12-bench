You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`Grid.from_structured` does not merge coincident pole and antimeridian nodes

- `_read_structured_grid` builds its KDTree on raw `(lon, lat)` pairs, so nodes that are the same point on the sphere are never merged.
- At the pole all `nlon+1` nodes sit at `lat=90` with distinct lons; at the seam `-180.5` and `179.5` differ by exactly 360.
- Result: `n_node` is exactly `(nlon+1)*(nlat+1)`, zero merges. 899 nodes should collapse at 1 deg, 3599 at 0.25 deg.
- The mesh is topologically torn: the pole node should have valence `nlon` (360 at 1 deg, 1440 at 0.25 deg) but reports 4.
- Only affects the native `to_rectilinear` backend; YAC uses `reg_2d_new` with a cyclic flag and never enumerates nodes.
- Fix: merge in Cartesian space inside `_read_structured_grid`.
- Related to #865, which raises the same pole/antimeridian concern for duplicate nodes generally.
