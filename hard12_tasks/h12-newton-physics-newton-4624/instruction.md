You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] SensorCamera renders fully transparent shapes (opacity 0) as opaque occluders

## Bug Description

`SensorCamera` ignores `Model.shape_opacity`. A shape with opacity `0` is rendered as an opaque surface in its RGB color. It occludes everything behind it in the color, albedo, depth, normal, and shape-index outputs. This commonly happens with MJCF helper geoms that use `rgba="... 0"` to be invisible: `import_mjcf` maps the alpha to `opacity=0.0`, and the shape keeps `ShapeFlags.VISIBLE`. Such geoms are invisible in MuJoCo's renderer and in `ViewerGL`, which draws shapes with opacity below 1 using blending. The camera, however, shows them as black slabs. In a robot-station scene loaded from MJCF, an alpha-0 collision plane for the table hid the table in 39% of a top-down camera's pixels.

In the reproduction, an alpha-0 box between the camera and a red sphere covers all 256 pixels. The center pixel reports the box (depth 1.45 m, albedo black) instead of the sphere (depth about 2.5 m, red).

Expected: shapes with opacity `0` do not appear in camera outputs. Fractional opacity is also ignored (rendered fully opaque). That would need blending or stochastic transparency in the renderer, which is out of scope here, but fully transparent shapes should at least not occlude.

### Narrowed cause

- `newton/_src/geometry/bvh.py`, `compute_enabled_shapes()` (called from `Model.bvh_build_shapes()`) selects shapes only by `shape_flags & shape_flags_mask` (default mask `ShapeFlags.VISIBLE`) and by supported type.
- `newton/_src/sensors/warp_raytrace/` (`raytrace.py`, `render.py`, `render_context.py`) never reads `Model.shape_opacity`. `Model.tri_opacity` for deformable surfaces is not read either.

One fix skips shapes with `shape_opacity <= 0` in `compute_enabled_shapes()` ([eric-heiden/newton@4df288f](https://github.com/eric-heiden/newton/commit/4df288f95cc888f759c51db59e5e36ee4d342afa)). `Model.bvh_shapes` is also the acceleration structure for `newton.intersect_ray()`, so that change also hides opacity-0 shapes from ray queries. This is consistent with the default `VISIBLE` mask, but maintainers may prefer to filter in the renderer only (for example a camera-side check in `closest_hit_shape()` and `first_hit_shape()`).

## Reproduction Script

```python
import math

import numpy as np
import warp as wp

import newton
from newton.sensors import SensorCamera

wp.config.log_level = wp.LOG_WARNING
device = "cpu"

# A red sphere and, between it and the camera, a fully transparent box
# (an MJCF geom with rgba alpha 0, imported with opacity 0).
MJCF = """
<mujoco>
  <worldbody>
    <geom name="ball" type="sphere" size="0.5" pos="0 0 0" rgba="1 0 0 1"/>
    <geom name="invisible_helper" type="box" size="1 1 0.05" pos="0 0 1.5" rgba="0 0 0 0"/>
  </worldbody>
</mujoco>
"""
builder = newton.ModelBuilder()
builder.add_mjcf(MJCF)
model = builder.finalize(device=device)
print("shape labels: ", model.shape_label)
print("shape opacity:", model.shape_opacity.numpy())
print("VISIBLE flag: ", [bool(f & newton.ShapeFlags.VISIBLE) for f in model.shape_flags.numpy()])

sensor = SensorCamera(model)
rays = sensor.utils.compute_camera_rays_pinhole(16, 16, camera_fovs=math.radians(40.0))
camera = wp.array([[wp.transform((0.0, 0.0, 3.0), wp.quat_identity())]], dtype=wp.transformf, device=device)
depth = sensor.utils.create_depth_image_output(16, 16)
shape_index = sensor.utils.create_shape_index_image_output(16, 16)
albedo = sensor.utils.create_albedo_image_output(16, 16)
sensor.update(model.state(), camera, rays, depth_image=depth, shape_index_image=shape_index, albedo_image=albedo)

a = int(albedo.numpy()[0, 0, 8, 8])
center_depth = round(float(depth.numpy()[0, 0, 8, 8]), 3)
center_shape = int(shape_index.numpy()[0, 0, 8, 8])
print("center pixel: depth [m]", center_depth, "shape", center_shape, "albedo", [(a >> s) & 0xFF for s in (0, 8, 16)])
ids = shape_index.numpy()[0, 0]
print("pixels per shape:", {label: int(np.sum(ids == i)) for i, label in enumerate(model.shape_label)})
print("expected: center depth ~2.5 m on the red ball; the transparent box covers no pixels")
```

Output on `main`:

```text
shape labels:  ['worldbody/ball', 'worldbody/invisible_helper']
shape opacity: [1. 0.]
VISIBLE flag:  [True, True]
center pixel: depth [m] 1.451 shape 1 albedo [0, 0, 0]
pixels per shape: {'worldbody/ball': 0, 'worldbody/invisible_helper': 256}
expected: center depth ~2.5 m on the red ball; the transparent box covers no pixels
```

With opacity-0 shapes excluded, the center pixel is `depth [m] 2.508 shape 0 albedo [254, 0, 0]` and the box covers 0 pixels. The same result occurs with `device = "cuda:0"`.

## System Information

- Newton: `1.7.0.dev0`, `main` at `dd2dace79fd47dd6c198f4a7a2f894c2aa47dcc4`
- Warp: `1.17.0` (CUDA toolkit 12.9, driver 595.58.03)
- MuJoCo / MuJoCo Warp: `3.14.0` / `3.14.0` (not involved; MJCF is parsed by Newton's importer)
- Python: `3.12.13`, Ubuntu 22.04
- Devices: CPU and NVIDIA RTX PRO 6000 Blackwell Server Edition (MIG 1g.24gb)

