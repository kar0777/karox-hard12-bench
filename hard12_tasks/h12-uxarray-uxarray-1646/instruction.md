You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Claude] `calculate_face_area` returns an incorrect Jacobian

### Version

v2026.07.0

### How did you install UXarray?

Source

### What happened?

In `uxarray/grid/area.py`, `calculate_face_area` accumulates the per-quadrature-point Jacobian into a variable that shares its name with the value being accumulated. The point value overwrites the running total on every iteration, so the accumulator is destroyed before it can accumulate anything:

```python
area = 0.0      # set area to 0
jacobian = 0.0  # set jacobian to 0
...
for j in range(0, num_triangles):
    ...
    for p in range(len(dW)):
        if quadrature_rule == "gaussian":
            for q in range(len(dW)):
                dA = dG[0][p]
                dB = dG[0][q]
                jacobian = calculate_spherical_triangle_jacobian(   # <-- clobbers running total
                    node1, node2, node3, dA, dB
                )
                area += dW[p] * dW[q] * jacobian
                jacobian += jacobian                               # <-- doubles current point
        elif quadrature_rule == "triangular":
            dA = dG[p][0]
            dB = dG[p][1]
            jacobian = calculate_spherical_triangle_jacobian_barycentric(  # <-- same
                node1, node2, node3, dA, dB
            )
            area += dW[p] * jacobian
            jacobian += jacobian                                   # <-- same
...
return area, jacobian
```

Because `jacobian` is reassigned at the top of each iteration, `jacobian += jacobian` is a self-double of the *current* point rather than a running sum. The returned value is always

```
2 * (Jacobian at the final quadrature point of the final sub-triangle)
```

Every earlier quadrature point, and every sub-triangle but the last, is silently discarded. Concretely, on the default code path (`quadrature_rule="triangular"`, `order=4`, which gives 6 quadrature points per sub-triangle).

## Impact

* Affects `calculate_face_area`, `get_all_face_area_from_coords`,  `Grid._compute_face_areas`, and the public Grid.face_jacobian` property, which all surface this value.
* **Face areas are *not* affected.** `area` is incremented with the freshly computed point value *before* the self-doubling, and the variable is overwritten again at the top of the next iteration, so area results remain correct. Only the second return value is wrong.
* The failure is silent. The Jacobian is a `sqrt(...)` and so is always non-negative, which means the negative-Jacobian guard in `Grid._compute_face_areas` never trips:

  ```python
  if np.any(self._face_jacobian < 0):
      raise ValueError("Negative jacobian found. Min jacobian: {}, Max jacobian: {}"...)
  ```

  There is also no existing test asserting anything about the returned Jacobian — the area tests use `area, _ = grid._compute_face_areas()` and discard it. Any mesh-quality metric built on `face_jacobian` (the stated intent of the code that introduced it) would be built on a meaningless number.

## Suggested fix

Give the per-point value its own name so the accumulator survives the loop:

```python
node_jacobian = calculate_spherical_triangle_jacobian(node1, node2, node3, dA, dB)
area += dW[p] * dW[q] * node_jacobian
jacobian += node_jacobian
```

and likewise in the `triangular` branch. 

## Note: `Grid.face_jacobian` is separately unreachable

While tracing where the bad value surfaces, the public property turns out to be broken in its own right. `_face_jacobian` is never initialized in `Grid.__init__` — unlike the other cached attributes there (`_ball_tree`, `_kd_tree`, `_spatialhash`, `_normalized`, …) — yet the property tests it *before* anything can assign it:

```python
@property
def face_jacobian(self):
    """Declare face_jacobian as a property."""
    if self._face_jacobian is None:   # <-- AttributeError on a fresh Grid
        _ = self.face_areas
    return self._face_jacobian
```

`Grid` is a plain class with no `__getattr__` or `__slots__`, so this raises `AttributeError: 'Grid' object has no attribute '_face_jacobian'` whenever `face_jacobian` is the first of the two properties to be touched:

```python
grid = ux.open_grid(...)
grid.face_jacobian    # AttributeError
grid.face_areas       # works, and sets _face_jacobian as a side effect
grid.face_jacobian    # now returns the (incorrect) value described above
```

For HEALPix grids it raises *even after* `face_areas`, because that branch short-circuits to `_compute_healpix_face_areas` and never assigns `_face_jacobian`:

```python
if "face_areas" not in self._ds:
    if self._ds.attrs.get("source_grid_spec") == "HEALPix":
        self._ds["face_areas"] = _compute_healpix_face_areas(self._ds)   # no jacobian
    else:
        face_areas, self._face_jacobian = self._compute_face_areas()
```

This has gone unnoticed because nothing exercises the property: there are no references to `face_jacobian` anywhere in `test/`, and both notebooks that report Jacobians (`docs/user-guide/area_calc.ipynb`, `docs/user-guide/healpix.ipynb`) call `grid._compute_face_areas(...)` directly, which returns the value rather than going through the property.

The fix is a one-line `self._face_jacobian = None` in `__init__` alongside the other cached attributes, plus a decision about what `face_jacobian` should mean for HEALPix grids (raise a clear error, or compute it geometrically). Worth folding in here, since any regression test for the accumulation bug written against the public property would hit the `AttributeError` before it ever reached the wrong number.


### What did you expect to happen?

The returned `jacobian` should be the sum of the Jacobian evaluated at every quadrature point of every sub-triangle of the face — accumulated the same way `area` is, in the same loop.

### Can you provide a MCVE to repoduce the bug?

```python
import numpy as np
import uxarray as ux

x = np.array([0.02974582, 0.1534193, 0.18363692])
y = np.array([-0.74469018, -0.88744577, -0.72230586])
z = np.array([0.66674712, 0.43462917, 0.66674712])

_, jacobian = ux.grid.area.calculate_face_area(x, y, z, "triangular", 4, False)

# Independent reference: sum the Jacobian over every quadrature point
dG, dW = ux.grid.area.get_tri_quadrature_dg(4)
node1, node2, node3 = (np.array([x[i], y[i], z[i]]) for i in range(3))
terms = [
    ux.grid.area.calculate_spherical_triangle_jacobian_barycentric(
        node1, node2, node3, dG[p][0], dG[p][1]
    )
    for p in range(len(dW))
]

print("returned:", jacobian)
print("expected:", sum(terms))
print("2 * last term:", 2 * terms[-1])   # matches `returned`
```


The same discrepancy appears with `quadrature_rule="gaussian"`. It is more pronounced for faces with more than three nodes, where only the final sub-triangle contributes at all.
