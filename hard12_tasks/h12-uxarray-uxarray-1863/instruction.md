You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`_small_angle_of_2_vectors` loses accuracy for nearly parallel vectors (naive difference of products in Kahan's formula)

### Version

v2026.09.1 (main at 88815a8c)

### How did you install UXarray?

Source

### What happened?

`uxarray.grid.utils._small_angle_of_2_vectors` loses accuracy for nearly parallel vectors. It implements Kahan's angle formula for vectors of arbitrary length,

```
angle = 2 * atan2(| v|u| - u|v| |, | v|u| + u|v| |)
```

but forms each component of `v|u| - u|v|` from two separately rounded products, i.e. a naive difference of two nearly equal products. The relative error grows as eps/angle: a mean of 2.5e-12 at 1e-5 rad, 2.4e-10 at 1e-7 rad, and 2.1e-8 at 1e-9 rad (200 random pairs of different lengths per angle, against the exact angle of the float64 inputs).

The function is used by `grid/angles.py` (face node angles), `grid/point_in_face.py` (winding number), and `grid/coordinates.py` (bounding circles). It currently has no tests. Found while reviewing #1806.

### What did you expect to happen?

Kahan's formula should be accurate to a few ulps for small angles. Evaluating each component of `v|u| - u|v|` with the FMA-based `diff_of_products` (already in `uxarray/utils/computing.py`) brings the mean error down to below 1e-16 for angles down to 1e-7 rad.

### Can you provide a MCVE to repoduce the bug?

```python
import math
from fractions import Fraction

import numpy as np

from uxarray.grid.utils import _small_angle_of_2_vectors

# Two nearly parallel vectors in the xy-plane, with different lengths.
theta = 1e-9
u = np.array([3.7 * math.cos(0.4), 3.7 * math.sin(0.4), 0.0])
v = np.array([0.21 * math.cos(0.4 + theta), 0.21 * math.sin(0.4 + theta), 0.0])

# Exact angle between the float64 inputs: (u x v)_z and u . v in exact rationals.
ux, uy, vx, vy = (Fraction(float(c)) for c in (u[0], u[1], v[0], v[1]))
exact = math.atan(float((ux * vy - uy * vx) / (ux * vx + uy * vy)))

got = _small_angle_of_2_vectors(u, v)
print(f"exact    = {exact:.17e}")
print(f"computed = {got:.17e}")
print(f"relative error = {abs(got - exact) / exact:.1e}")
```

Output on main:

```
exact    = 1.00000003822873689e-09
computed = 1.00000004983169261e-09
relative error = 1.2e-08
```

