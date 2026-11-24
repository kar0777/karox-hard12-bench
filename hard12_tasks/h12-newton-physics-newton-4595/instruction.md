You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] add_mjcf drops spatial-tendon sites whose names contain "-"

**Version:** newton 1.6.1 (warp-lang 1.18.0, mujoco 3.12.0), CPU. The same code is on `main`: site labels keep the raw name (`site_label = f"{label_prefix}/{site_name}"`).

**What happens:** a spatial tendon loses every site whose name contains `-`. `add_mjcf` warns `Spatial tendon 'flexor' references unknown site 'm_origin', skipping element.` and then drops the tendon (`has no valid wrap elements`). The same model with `_` instead of `-` imports without warnings.

**Reproduction:**

```python
import warnings
import newton

XML = """<mujoco>
  <worldbody>
    <body name="upper">
      <geom type="capsule" fromto="0 0 0 0 0 -0.3" size="0.03"/>
      <site name="m-origin" pos="0.02 0 -0.05"/>
      <body name="lower" pos="0 0 -0.3">
        <joint name="elbow" axis="0 1 0"/>
        <geom type="capsule" fromto="0 0 0 0 0 -0.25" size="0.025"/>
        <site name="m-insertion" pos="0.02 0 -0.05"/>
      </body>
    </body>
  </worldbody>
  <tendon>
    <spatial name="flexor">
      <site site="m-origin"/>
      <site site="m-insertion"/>
    </spatial>
  </tendon>
</mujoco>"""

builder = newton.ModelBuilder()
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    builder.add_mjcf(XML)
print([str(w.message) for w in caught])  # unknown site 'm_origin', 'm_insertion'
```

**Likely cause** (from `newton/_src/utils/import_mjcf.py` in 1.6.1): the spatial-tendon parser sanitizes the referenced name (`site_name = sanitize_name(site_name)`, which turns `-` into `_`), then looks it up with `find_shape_by_name`, which compares against `builder.shape_label`. The labels keep the original name (`m-origin`), so the sanitized name never matches. The site-equality path uses `site_name_to_idx`, which is keyed by the sanitized name and would find the site.

**Impact:** MyoSuite's musculoskeletal models (elbow, hand, arm, leg, and the MuscleMimic full body and bimanual) name their muscle path sites with hyphens, so their muscle-tendon paths lose sites on import. Context: #238.
