You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] SolverVBD: dihedral bending is silently off for hinges with triangles smaller than ~1 mm (absolute degeneracy threshold)

### Bug Description

`evaluate_dihedral_angle_based_bending_force_hessian` treats a hinge as degenerate and returns zero force and Hessian when ([`particle_vbd_kernels.py:716`](https://github.com/newton-physics/newton/blob/0679304388f3edfea6e7e942232724425d089cd3/newton/_src/solvers/vbd/particle_vbd_kernels.py#L716), [L736-L745](https://github.com/newton-physics/newton/blob/0679304388f3edfea6e7e942232724425d089cd3/newton/_src/solvers/vbd/particle_vbd_kernels.py#L736-L745)):

```python
eps = 1.0e-6
n1 = wp.cross(x02, x03)
n2 = wp.cross(x13, x12)
...
if n1_norm < eps or n2_norm < eps or e_norm < eps:
    return wp.vec3(0.0), wp.mat33(0.0)
```

`n1` and `n2` are not normalized: their length is twice the triangle area in m^2. The test is therefore `area < 5e-7 m^2`, an absolute size, not a shape test. On a right-triangle grid every hinge with legs below 1 mm is skipped, without a warning, so cloth meshed finer than about 1 mm has membrane forces but no bending at all, whatever `edge_ke` is. The damping term repeats the same test on the previous positions ([L825](https://github.com/newton-physics/newton/blob/0679304388f3edfea6e7e942232724425d089cd3/newton/_src/solvers/vbd/particle_vbd_kernels.py#L825)).

From the script below (main, CPU):

- a hinge folded 30 degrees gets the same force (0.5236 N for `edge_ke` 1) for legs of 10, 2, 1.2 and 1 mm, as it should (the force does not depend on the scale), and exactly 0 for legs of 0.8 and 0.5 mm;
- a strip clamped at one end, 28 x 14 cells: with 5 mm cells, raising `edge_ke` from 1e-4 to 100 lifts the tip from -132.6 to -107.8 mm after 0.2 s; with 0.5 mm cells, `edge_ke` 1e-4 and 1 give bitwise identical positions.

**Expected.** A hinge is degenerate when its triangles are degenerate in shape (height much smaller than the edge), independent of the mesh scale. Sub-millimetre meshes (fine cloth, thin films, small parts) get bending forces that scale with `edge_ke`.

**Proposed fix.** Compare the unnormalized normals with `eps` times the squared edge length, in both places:

```python
area_eps = eps * e_norm * e_norm
if e_norm < eps or n1_norm < area_eps or n2_norm < area_eps:
    return wp.vec3(0.0), wp.mat33(0.0)
```

A triangle then counts as degenerate when its height is below `1e-6` times the edge, which is what the current test does for 1 m edges. With this change the script gives 0.5236 N for every hinge size, the 0.5 mm strip's tip rises from -13.8 to -5.5 mm when `edge_ke` goes from 1e-4 to 1, and the 5 mm strip is unchanged. I can open a PR with this change and a regression test.

### Reproduction Script

```python
"""SolverVBD dihedral bending: hinges whose triangles are smaller than ~1 mm get no bending force.

usage: python repro.py [cpu|cuda:0]
1. One hinge (two right triangles with legs L sharing an edge), folded 30 degrees from its flat rest angle: bending
   force on an opposite vertex for several L. The energy is 0.5 * edge_ke * rest_length * theta^2 and d(theta)/dx
   scales with 1/L, so the force does not depend on L.
2. A strip clamped at one end, under gravity, the same mesh at two scales: tip height after 0.2 s for two
   values of edge_ke (1e-4 and a stiff value).
"""

import sys

import numpy as np
import warp as wp

import newton
from newton._src.solvers.vbd.particle_vbd_kernels import evaluate_dihedral_angle_based_bending_force_hessian

wp.config.log_level = wp.LOG_WARNING
DEVICE = sys.argv[1] if len(sys.argv) > 1 else "cpu"


@wp.kernel
def hinge_force(pos: wp.array[wp.vec3], edges: wp.array2d[wp.int32], rest_angle: wp.array[float],
                rest_length: wp.array[float], out: wp.array[wp.vec3]):
    f, h = evaluate_dihedral_angle_based_bending_force_hessian(0, 0, pos, pos, edges, rest_angle, rest_length,
                                                               1.0, 0.0, 1.0e-3)
    out[0] = f


def hinge_check():
    print("1. hinge folded 30 deg, edge_ke 1 N, force on opposite vertex 0:")
    a = np.radians(30.0)
    for L in (1.0e-2, 2.0e-3, 1.2e-3, 1.0e-3, 8.0e-4, 5.0e-4):
        # edge from x2 = (0, 0, 0) to x3 = (L, 0, 0); opposite vertices at distance L from the edge
        x = np.array([[0.0, L * np.cos(a), L * np.sin(a)], [0.0, -L, 0.0], [0.0, 0.0, 0.0], [L, 0.0, 0.0]])
        pos = wp.array(x.astype(np.float32), dtype=wp.vec3, device=DEVICE)
        edges = wp.array(np.array([[0, 1, 2, 3]], np.int32), dtype=wp.int32, device=DEVICE)
        out = wp.zeros(1, dtype=wp.vec3, device=DEVICE)
        wp.launch(hinge_force, dim=1, inputs=[pos, edges, wp.array([0.0], dtype=float, device=DEVICE),
                                              wp.array([L], dtype=float, device=DEVICE)], outputs=[out], device=DEVICE)
        print(f"   L = {L * 1e3:5.2f} mm (2 x triangle area {L * L:.2e} m^2): |f| = {np.linalg.norm(out.numpy()[0]):.4f} N")


def strip_tip(cell, edge_ke, nx=28, ny=14, seconds=0.2, dt=1.0e-3):
    b = newton.ModelBuilder()
    b.add_cloth_grid(pos=wp.vec3(0.0, 0.0, 1.0), rot=wp.quat_identity(), vel=wp.vec3(0.0, 0.0, 0.0), dim_x=nx, dim_y=ny,
                     cell_x=cell, cell_y=cell, mass=0.02 * cell * cell, fix_left=True, tri_ke=1.0e3, tri_ka=1.0e3,
                     tri_kd=0.0, edge_ke=edge_ke, edge_kd=0.0, particle_radius=0.1 * cell)
    b.color()
    m = b.finalize(device=DEVICE)
    solver = newton.solvers.SolverVBD(m, iterations=10)
    s0, s1, control = m.state(), m.state(), m.control()
    for _ in range(int(round(seconds / dt))):
        s0.clear_forces()
        solver.step(s0, s1, control, None, dt)
        s0, s1 = s1, s0
    q = s0.particle_q.numpy()
    return q[:, 2].min() - 1.0, q


def strip_check():
    print("2. strip clamped at one end (28 x 14 cells, 20 g/m^2, tri_ke 1e3), gravity, tip height after 0.2 s:")
    for cell, stiff in ((5.0e-3, 100.0), (5.0e-4, 1.0)):    # a stiff value each mesh still steps stably
        (za, qa), (zb, qb) = strip_tip(cell, 1.0e-4), strip_tip(cell, stiff)
        print(f"   cell {cell * 1e3:.1f} mm: edge_ke 1e-4: {za * 1e3:8.3f} mm, edge_ke {stiff:g}: {zb * 1e3:8.3f} mm, "
              f"identical positions: {np.array_equal(qa, qb)}")


print(f"newton {newton.__version__}, warp {wp.__version__}, device {DEVICE}")
hinge_check()
strip_check()
```

Output on `main` (06793043), CPU:

```
newton 1.8.0.dev0, warp 1.18.0, device cpu
1. hinge folded 30 deg, edge_ke 1 N, force on opposite vertex 0:
   L = 10.00 mm (2 x triangle area 1.00e-04 m^2): |f| = 0.5236 N
   L =  2.00 mm (2 x triangle area 4.00e-06 m^2): |f| = 0.5236 N
   L =  1.20 mm (2 x triangle area 1.44e-06 m^2): |f| = 0.5236 N
   L =  1.00 mm (2 x triangle area 1.00e-06 m^2): |f| = 0.5236 N
   L =  0.80 mm (2 x triangle area 6.40e-07 m^2): |f| = 0.0000 N
   L =  0.50 mm (2 x triangle area 2.50e-07 m^2): |f| = 0.0000 N
2. strip clamped at one end (28 x 14 cells, 20 g/m^2, tri_ke 1e3), gravity, tip height after 0.2 s:
   cell 5.0 mm: edge_ke 1e-4: -132.573 mm, edge_ke 100: -107.754 mm, identical positions: False
   cell 0.5 mm: edge_ke 1e-4:  -13.764 mm, edge_ke 1:  -13.764 mm, identical positions: True
```

CUDA (L4) gives the same hinge forces, and with 0.5 mm cells both `edge_ke` values again give identical positions (tip -13.630 mm).

### System Information

- Newton: main @ 06793043 (1.8.0.dev0)
- Warp: 1.18.0
- Python: 3.12.15
- OS: Ubuntu 22.04.5 LTS
- GPU: none for the run above; the CUDA run used an NVIDIA L4 (driver 580.178.04)

