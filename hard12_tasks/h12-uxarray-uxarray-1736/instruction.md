You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

IO for `fesom` not converting `n2` to `two` during `open_grid`

### Version

2026.7.1

### How did you install UXarray?

Source

### What happened?

When making a fix for #1444 in PR #1667, we noticed there were far more outliers than expected, in an attempt to clean grid files. One example was this file:

<img width="583" height="421" alt="Image" src="https://github.com/user-attachments/assets/a7f8c615-15b3-4c36-8f8b-79aac49100ba" />

In a bit less detail it looks like this:

<img width="796" height="121" alt="Image" src="https://github.com/user-attachments/assets/928ec656-c3b0-40d4-81f9-f109c27f074d" />

We didn't expect this many non-grid dimensions on the grid, and we assume that n2 is likely supposed to be converted to "two" which is a dimension we expect. We would need to resolve this before proceeding, as we don't want to delete it in our planned cleaning process, if it actually needs to be converted to "two"

### What did you expect to happen?

To see "two" as a dimension, not "n2"

### Can you provide a MCVE to repoduce the bug?

```python
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
import uxarray as ux

MESHFILES = "../../uxarray/test/meshfiles/"

# FESOM2 mesh.diag — nz, nz1, n2, N, n4
mesh_diag = ux.open_grid(MESHFILES + "ugrid/fesom/fesom.mesh.diag.nc")
mesh_diag

# --- separate cell ---

GRID_DIMS = set(ux.conventions.ugrid.DIM_NAMES)
print("  dims          :", dict(mesh_diag._ds.sizes))
print("  non-grid dims :", [d for d in mesh_diag._ds.sizes if d not in GRID_DIMS])
print("  coords        :", list(mesh_diag._ds.coords))
```
